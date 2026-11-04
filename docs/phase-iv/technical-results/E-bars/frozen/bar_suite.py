"""Finite grouped D-052 invocations; disclose every native child/context."""
import argparse
from decimal import Decimal, ROUND_HALF_EVEN
import hashlib
import json
from pathlib import Path
import subprocess
import time

from bar_fixtures import ticks, available, closed_eligible, DURATION


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--group',required=True);parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();root=args.root;frozen=Path(__file__).parent
    bundle=json.loads((frozen/'cases.json').read_text());out=root/args.group;out.mkdir(exist_ok=False)
    records=[];checks=[]
    def check(name,ok,detail=None):checks.append({'name':name,'passed':bool(ok),'detail':detail})
    for cid in bundle['groups'][args.group]:
        path=out/cid;path.mkdir();command=['/workspace/technical-admission/E/recovery/venv/bin/python',str(frozen/'bar_worker.py'),
            '--bundle',str(frozen/'cases.json'),'--case',cid,'--output',str(path/'observations.json')]
        started=time.monotonic()
        with (path/'native.log').open('x') as log:
            try:code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=90,check=False).returncode
            except subprocess.TimeoutExpired:code='timeout'
        record={'case_id':cid,'command':command,'exit_code':code,'wall_seconds':time.monotonic()-started}
        (path/'invocation.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
        if code!=0 or not (path/'observations.json').exists():
            check(cid+':native_worker_completed',False,record);continue
        observed=json.loads((path/'observations.json').read_text());case=observed['configuration']
        check(cid+':callbacks_no_errors',not observed['callback_errors'],observed['callback_errors'])
        usd,inventory=Decimal('1000'),Decimal(0)
        for f in observed['fills']:
            qty,price,fee=(Decimal(f[k]) for k in ('quantity','price','fee'))
            check(cid+':native_fee:'+f['fill_id'],fee==(qty*price*Decimal(case[f['liquidity_role']+'_fee'])).quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN))
            usd-=qty*price+fee;inventory+=qty
        check(cid+':native_accounting',usd==Decimal(observed['balances']['USD']) and inventory==Decimal(observed['balances']['SYN']))
        check(cid+':free_plus_reserved',all(Decimal(observed['free'][c])+Decimal(observed['reserved'][c])==Decimal(v) for c,v in observed['balances'].items()))
        check(cid+':position',sum(Decimal(p['quantity'])*(1 if p['side']=='LONG' else -1) for p in observed['positions'])==inventory)
        if case['mode']=='native':
            bars=[t for t in observed['trace'] if t['kind']=='bar_callback']
            check(cid+':decision_only_after_confirmed_available',bool(observed['decision']) and observed['decision']['at']>=case['bars'][0]['available_ns'])
            record['observed_fills']=observed['fills']
            record['same_N_close_price_observed']=any(Decimal(f['price'])==Decimal('100.50') for f in observed['fills'])
            record['native_outcome_observational_not_causal_admission']=True
        elif case['mode']=='timestamp':
            bars=[t for t in observed['trace'] if t['kind']=='bar_callback']
            source=case['bars'][0]
            check(cid+':native_receipt_equals_supplied_init',len(bars)==1 and bars[0]['at']==source['ts_init'],bars)
            record['receipt_before_true_close']=bool(bars) and bars[0]['at']<source['close_ns']
            check(cid+':negative_or_corrected_control',record['receipt_before_true_close']==case['negative_control'])
            check(cid+':event_and_init_exact',bool(bars) and bars[0]['bar']['ts_event']==source['ts_event'] and bars[0]['bar']['ts_init']==source['ts_init'])
        else:
            expected_count=0 if cid=='late-decision-false' else 1
            check(cid+':expected_native_fill_count',len(observed['fills'])==expected_count)
            if observed['fills']:
                f=observed['fills'][0];oracle=bundle['causal_oracle'];late=cid=='late-decision-true'
                check(cid+':declared_synthetic_price',Decimal(f['price'])==Decimal(oracle['late_price'] if late else oracle['base_price']))
                check(cid+':eligible_fill_time',f['at']==(oracle['late_fill_at'] if late else oracle['base_fill_at']))
                submit=next(t for t in observed['trace'] if t['kind']=='submit_intent')
                check(cid+':no_retroactive_market_event',submit['source_event_ns']>=observed['decision']['ready_at'] and f['at']>=submit['source_available_ns'] and f['at']>=submit['at'])
            early=[t for t in observed['trace'] if t['at']<=bundle['invariance_cutoff_ns']]
            record['early_prefix_digest']=digest(early)
            if args.group=='invariance':
                previous=json.loads((root/'causal/causal-base/observations.json').read_text())
                baseline=[t for t in previous['trace'] if t['at']<=bundle['invariance_cutoff_ns']]
                check(cid+':prefix_decision_execution_invariance',early==baseline,{'actual_digest':digest(early),'baseline_digest':digest(baseline)})
    if args.group=='timestamps':
        def rejects(fn):
            try:fn()
            except ValueError:return True
            return False
        for unit,raw,expected in [('s',1,1_000_000_000),('ms',1,1_000_000),('us',1,1000),('ns',123,123)]:check('units:'+unit,ticks(raw,unit)==expected)
        for name,fn in [('float',lambda:ticks(1.0,'ns')),('bool',lambda:ticks(True,'ns')),('unknown',lambda:ticks(1,'ticks')),('overflow',lambda:ticks(2**64,'ns')),('negative',lambda:ticks(-1,'ns')),('ns_to_us_loss',lambda:ticks(1001,'ns','us'))]:check('reject:'+name,rejects(fn))
        check('exact_narrowing',ticks(2000,'ns','us')==2)
        check('opening_and_closing_labels_same_availability',available(100,'open',60)==available(160,'close',60)==160)
        selections=json.loads((frozen/'R-selection.json').read_text())['selections']
        for selected in selections:
            for row in selected['rows']:
                event,expected=row['event'],row['expected'];ident=selected['journal_id']+':'+event['id']+':'+str(row['original_index'])
                if selected['journal_id']=='R1':check(ident,closed_eligible(event['receive_ns'],event['event_ns'],event['available_ns'])==(expected['decision']=='OBSERVE'))
                elif selected['journal_id']=='R2':check(ident,ticks(event['event_tick'],event['time_unit'])==expected['event_ns'])
                elif selected['journal_id']=='R3':
                    closed=event['op']=='close_bar';end=event['data'].get('end_ns',event['event_ns'])
                    check(ident,closed_eligible(event['receive_ns'],end,event['available_ns'],closed)==(expected['state']['latest_complete_bar'] is not None))
                else:
                    # Original R7 correction is unavailable at the earlier prefix.
                    check(ident,closed_eligible(10,event['event_ns'],event['available_ns'])==(event['id']=='p1'))
    result={'group':args.group,'native_child_invocations':len(records),'records':records,'checks':checks,
            'passed_component_checks':all(c['passed'] for c in checks),
            'native_adverse_outcomes_are_not_suppressed':True,'financial_admission':False,
            'scope':'One grouped technical invocation; every native child above is explicit. R selected predicates only, not R suite repeated.'}
    with (out/'summary.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'group':args.group,'native_children':len(records),'checks':len(checks),'failed':[c for c in checks if not c['passed']]}))
    raise SystemExit(0 if result['passed_component_checks'] else 1)


if __name__=='__main__':main()
