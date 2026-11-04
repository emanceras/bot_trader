"""Frozen D-052 finite bar cases and exact temporal adapter primitives."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json

T0 = 1_700_000_000_000_000_000
SECOND = 1_000_000_000
DURATION = 60 * SECOND
T1, T2 = T0+DURATION, T0+2*DURATION


def ticks(value, unit, target='ns'):
    factors={'s':SECOND,'ms':1_000_000,'us':1000,'ns':1}
    if type(value) is not int or unit not in factors or target not in factors:
        raise ValueError('Unsupported timestamp representation')
    ns=value*factors[unit]
    if not 0 <= ns < 2**64 or ns % factors[target]:
        raise ValueError('Timestamp range or exact precision not preserved')
    return ns//factors[target]


def available(label, convention, duration):
    value=ticks(label,'ns')
    if type(duration) is not int or duration <= 0 or convention not in ('open','close'):
        raise ValueError('Unsupported interval or label convention')
    return ticks(value+duration if convention=='open' else value,'ns')


def closed_eligible(now, close_ns, availability_ns, confirmed=True):
    for value in (now,close_ns,availability_ns):ticks(value,'ns')
    if type(confirmed) is not bool:raise ValueError('Unknown close status')
    return confirmed and now>=close_ns and now>=availability_ns


def base(name, mode='native'):
    return {'id':name,'mode':mode,'bar_execution':mode=='native','adaptive':False,'latency_ns':0,
        'decision_processing_ns':0,'quantity':'1.00','maker_fee':'0.001','taker_fee':'0.002',
        'initial_cash':{'USD':'1000.00','SYN':'0.00'},
        'bars':[
            {'id':'N','open':'100.00','high':'101.00','low':'99.00','close':'100.50','volume':'100.00',
             'open_ns':T0,'close_ns':T1,'ts_event':T1,'ts_init':T1,'available_ns':T1,'label':'close'},
            {'id':'N+1','open':'110.00','high':'125.00','low':'108.00','close':'112.00','volume':'100.00',
             'open_ns':T1,'close_ns':T2,'ts_event':T2,'ts_init':T2,'available_ns':T2,'label':'close'}],
        'quotes':[], 'signal_rule':'after confirmed eligible N close, hold one BUY intention; no strategy fitting',
        'execution_policy':{'version':'D052-OHLC-synthetic-v1','spread_usd':'0.10','additional_slippage_usd':'0.00',
            'visible_quantity_assumption':'2.00','max_order_quantity':'1.00','max_quote_age_ns':1_000_000,
            'synthetic_quote_not_observed':True,'eligible_rule':'decision exists; quote event>=decision time; quote availability>=decision time; no retroactive cached quote',
            'unfilled_rule':'cancel any remaining market quantity on next available supervisor turn; confirmation required; no automatic retry',
            'scope':'technical values only, not empirical spread/latency/capacity or financial policy approval'}}


def causal(name):
    f=base(name,'causal')
    f['quotes']=[{'id':'opening-N+1','mid':'110.00','event_ns':T1,'available_ns':T1+1_000_000,
                  'origin':'synthetic quote derived solely from N+1 opening110.00; no high/low/close information'}]
    return f


def bundle():
    cases=[]
    groups={}
    for latency,group in [(0,'native-zero'),(1_000_000,'native-latency')]:
        ids=[]
        for adaptive in (False,True):
            f=base(f'{group}-adaptive-{str(adaptive).lower()}')
            f.update(latency_ns=latency,adaptive=adaptive)
            cases.append(f);ids.append(f['id'])
        groups[group]=ids
    ids=[]
    for label,corrected,precision in [('open',False,0),('open',True,0),('close',True,0),('open',True,123)]:
        f=base(f'timestamp-{label}-{corrected}-{precision}','timestamp')
        f['bars']=f['bars'][:1]
        b=f['bars'][0];b['open_ns']+=precision;b['close_ns']+=precision
        b['label']=label;b['ts_event']=b['open_ns'] if label=='open' else b['close_ns']
        b['ts_init']=available(b['ts_event'],label,DURATION) if corrected else b['ts_event']
        b['available_ns']=b['close_ns']
        f['negative_control']=not corrected
        cases.append(f);ids.append(f['id'])
    groups['timestamps']=ids
    f=causal('causal-base');cases.append(f);groups['causal']=[f['id']]
    ids=[]
    for field,value in [('high','135.00'),('low','106.00'),('close','113.00'),('revision','99.75')]:
        f=causal('invariance-'+field)
        if field=='revision':
            b=deepcopy(f['bars'][0]);b.update(id='N-revision',close=value,ts_init=T1+30_000_000,available_ns=T1+30_000_000,revision_of='N')
            f['bars'].append(b)
        else:f['bars'][1][field]=value
        cases.append(f);ids.append(f['id'])
    groups['invariance']=ids
    ids=[]
    for later in (True,False):
        f=causal('late-decision-'+str(later).lower())
        f['bars'][0]['available_ns']=f['bars'][0]['ts_init']=T1+10_000_000
        if later:f['quotes'].append({'id':'later-independent-event','mid':'111.00','event_ns':T1+20_000_000,'available_ns':T1+21_000_000,
                                    'origin':'independently declared synthetic later market event; not future OHLC'})
        cases.append(f);ids.append(f['id'])
    groups['late-decision']=ids
    return {'schema':'D052-bars-v1','engine':'2.0.0rc7','python':'3.13.16-standard','groups':groups,'cases':cases,
        'invariance_cutoff_ns':T1+25_000_000,
        'native_outcomes':'observational; do not predict which OHLC level latency/adaptive selects',
        'timestamp_oracle':'negative delivered at opening is adverse configuration; corrected delivered at close, +123ns retained exactly; close label not shifted twice',
        'causal_oracle':{'base_price':'110.05','base_fill_at':T1+1_000_000,'late_price':'111.05','late_fill_at':T1+21_000_000,
                         'late_without_new_event_fills':0,'quantity':'1.00','invariance':'early decision/order/fill prefix identical to base'},
        'native_contexts_initial':sum(len(v) for v in groups.values()),
        'no_new_financial_hypothesis':True}


def freeze(root):
    target=root/'frozen';target.mkdir(exist_ok=False)
    here=Path(__file__).resolve().parent
    names=['bar_fixtures.py','bar_worker.py','bar_suite.py','bar_guard.py','nautilus_worker.py']
    for name in names:(target/name).write_bytes((here/name).read_bytes())
    (target/'cases.json').write_text(json.dumps(bundle(),indent=2)+'\n')
    source=here/'fixtures/temporal_journals.json'
    r=json.loads(source.read_text())
    (target/'R-source-shape.json').write_text(json.dumps({'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'selected_ids':['R1','R2','R3','R7'],'reuse':'availability, exact unit/precision, closed-bar revision and future-prefix constraints; source snippets separately preserved'},indent=2)+'\n')
    (target/'R-selection.json').write_bytes(Path('/tmp/bar-r-selection.json').read_bytes())
    manifest={'state':'before first native execution','sources':{n:hashlib.sha256((target/n).read_bytes()).hexdigest() for n in names},
              'bundle_sha256':hashlib.sha256((target/'cases.json').read_bytes()).hexdigest(),
              'groups':bundle()['groups'],'max_guarded_test_invocations':8,'one_repair_cycle_within8':True,
              'native_latency_uses_message_queue':True,'no_intermediate_native_market_clock_events':True,
              'terminal_drain':'InstrumentStatus.NONE one second after last available event; declared and common'}
    (target/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest))


if __name__=='__main__':freeze(Path('/workspace/technical-admission/E/bars'))
