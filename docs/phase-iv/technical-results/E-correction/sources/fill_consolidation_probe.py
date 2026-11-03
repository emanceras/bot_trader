"""Finite D-050 supervisor probe; synthetic duplicate rows never enter engine."""
from copy import deepcopy
from decimal import Decimal
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from command_boundary import FillBoundary


def cash(fills):
    usd, inventory, fees = Decimal('1000.00'), Decimal(0), Decimal(0)
    for f in fills:
        q,p,fee=(Decimal(f[k]) for k in ['quantity','price','fee'])
        direction=1 if f['side']=='BUY' else -1
        usd-=direction*q*p+fee
        inventory+=direction*q
        fees+=fee
    return {'USD':str(usd),'SYN':str(inventory),'fees_USD':str(fees)}


def main():
    root=Path('/workspace/technical-admission/E/correction')
    out=root/'fill-consolidation'
    out.mkdir(exist_ok=False)
    observed=json.loads((root/'observations/E4-idempotency.json').read_text())
    # Independent, declared synthetic supervisor input. These are not native
    # engine fills and do not fill the missing second execution in original E4.
    invented=[{'venue':'SUPERVISOR-ONLY','fill_id':f'synthetic-{i}',
        'command_id':'synthetic-order','side':'BUY','quantity':'3.00','price':'100.00',
        'fee':'0.60','fee_currency':'USD','origin':'hand-authored supervisor-only synthetic record'} for i in (1,2)]
    protocol={'recorded_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'boundary_sha256':hashlib.sha256(Path(__file__).with_name('command_boundary.py').read_bytes()).hexdigest(),
        'native_observation_sha256':hashlib.sha256((root/'observations/E4-idempotency.json').read_bytes()).hexdigest(),
        'synthetic_inputs':invented,
        'synthetic_expected':{'USD':'398.80','SYN':'6.00','fees_USD':'1.20'},
        'criteria':['Known fill identity redelivery produces no second ledger effect',
                    'Equal-value different identities remain distinct',
                    'Conflicting same identity is rejected atomically',
                    'Actual native effects reconcile to observed cash/inventory/order/position/reserve',
                    'No native engine execution, no amendment of original E4 expected6'],
        'freeze':'written before supervisor probe outcomes'}
    (out/'protocol-before-execution.json').write_text(json.dumps(protocol,indent=2)+'\n')
    checks=[]
    def check(name,condition): checks.append({'name':name,'passed':bool(condition)})
    native=FillBoundary()
    for f in observed['fills']:
        check('native:first_delivery:'+f['fill_id'],native.accept(f))
        check('native:redelivery_suppressed:'+f['fill_id'],not native.accept(f))
    actual=cash(native.fills.values())
    check('native:cash_matches',Decimal(actual['USD'])==Decimal(observed['balances']['USD']))
    check('native:inventory_matches',Decimal(actual['SYN'])==Decimal(observed['balances']['SYN']))
    check('native:position_matches',sum(Decimal(p['quantity'])*(1 if p['side']=='LONG' else -1) for p in observed['positions'])==Decimal(actual['SYN']))
    first=next(o for o in observed['orders'] if o['id']=='shared-first')
    check('native:order_fill_history_matches_actual',Decimal(first['filled'])==sum(Decimal(f['quantity']) for f in native.fills.values()))
    check('native:open_limit_reservation_matches_remainder',first['status']=='PARTIALLY_FILLED' and Decimal(observed['reserved']['USD'])==Decimal(first['remaining'])*100)
    check('native:free_plus_reserved',Decimal(observed['free']['USD'])+Decimal(observed['reserved']['USD'])==Decimal(observed['balances']['USD']))
    check('native:no_extra_USDT_conversion',Decimal(observed['balances']['USDT'])==40)
    synthetic=FillBoundary()
    for f in invented:
        check('synthetic:first_distinct_id:'+f['fill_id'],synthetic.accept(f))
        check('synthetic:duplicate_ignored:'+f['fill_id'],not synthetic.accept(f))
    check('synthetic:equal_values_both_preserved',len(synthetic.fills)==2)
    theoretical=cash(synthetic.fills.values())
    check('synthetic:hand_calculated_totals',all(Decimal(theoretical[k])==Decimal(protocol['synthetic_expected'][k]) for k in theoretical))
    corrupt=deepcopy(invented[0]);corrupt['quantity']='4.00'
    rejected=False
    try:synthetic.accept(corrupt)
    except ValueError:rejected=True
    check('synthetic:conflict_rejected',rejected)
    check('synthetic:conflict_no_accounting_effect',cash(synthetic.fills.values())==theoretical)
    result={'checks':checks,'passed':all(c['passed'] for c in checks),
        'actual_native_reconciled':actual,'invented_supervisor_only_totals':theoretical,
        'original_E4_still_fails_required_second_native_fill':True,
        'new_native_execution':False,'native_duplicate_fill_protection_proved':False,
        'origin':'FillBoundary supervisor only; original engine/case outputs unchanged'}
    with (out/'result.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result))
    raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':main()
