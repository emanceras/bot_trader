"""One finite supervisor regression invocation; no engine or fill injection."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import argparse

from command_boundary import CommandBoundary, FillBoundary
from engine_fixtures import check_accounting
from evaluate_nautilus import evaluate
from l2_reference import derive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    fixtures = {f['case_id']:f for f in json.loads((root.parent/'fixtures/engine-cases.json').read_text())['functional']}
    observations = {name:json.loads((root/'observations'/f'{name}.json').read_text()) for name in ['E3-L2','D6-cancel','E4-idempotency']}
    checks = []

    def check(name, condition, detail=None):
        checks.append({'name':name,'passed':bool(condition),'detail':detail})

    def rejected(function):
        try: function()
        except ValueError: return True
        return False

    for name in ['E3-L2','E4-idempotency']:
        result = evaluate(fixtures[name], observations[name])
        check(name+':frozen_component_oracle', not result['problems'], result)
    e3 = observations['E3-L2']
    quotes = e3['derived_reference_quotes']
    expected = [derive(e) for e in fixtures['E3-L2']['events'] if e['kind']=='book_snapshot']
    check('L2:reference_provenance_and_values', quotes==expected)
    observed_quotes = [t['quote'] for t in e3['trace'] if t['kind']=='native_quote_callback']
    check('L2:one_reference_per_original_snapshot', len(observed_quotes)==len(expected))
    check('L2:terminal_reserves_zero', all(Decimal(v)==0 for v in e3['reserved'].values()))
    level_fixture=fixtures['E3-L2']['events'][0]
    bad=deepcopy(level_fixture);bad['bids']=[]
    check('L2:empty_side_rejected_without_fallback',rejected(lambda:derive(bad)))
    bad_time=deepcopy(level_fixture);bad_time['available_ns']=float(bad_time['available_ns'])
    check('L2:inexact_timestamp_rejected',rejected(lambda:derive(bad_time)))

    d6=observations['D6-cancel']
    diag=next(f for f in json.loads((root/'l2/diagnostics.json').read_text())['cases'] if f['case_id']=='D6-cancel')
    check('D6:independent_accounting',not check_accounting(diag,d6))
    before=next(s for s in d6['snapshots'] if s['source']=='before:D6-cancel-cancel')
    check('D6:partial_quantity_preserved_before_cancel',before['orders'][0]['status']=='PARTIALLY_FILLED' and Decimal(before['orders'][0]['filled'])==4 and Decimal(before['orders'][0]['remaining'])==2)
    check('D6:explicit_cancel_preserves_fills',d6['orders'][0]['status']=='CANCELED' and Decimal(d6['orders'][0]['filled'])==4)
    check('D6:terminal_reserves_zero',all(Decimal(v)==0 for v in d6['reserved'].values()))
    check('D6:remaining_cash_reservation_recorded_not_assumed',True,{'before_cancel':before['reserved'],'after_cancel':d6['reserved'],'note':'Zero before and after means no native release occurred; no guarantee of funding reserved for open market remainder'})

    e4=observations['E4-idempotency']
    first=next(o for o in e4['orders'] if o['id']=='shared-first')
    check('E4:first_native_order_history_preserved',first['status']=='FILLED' and Decimal(first['filled'])==6)
    check('E4:first_native_submit_once',sum(e['type']=='OrderSubmitted' and e.get('client_order_id')=='shared-first' for e in e4['native_events'])==1)
    check('E4:duplicate_suppression_is_supervisor',sum(t['kind']=='supervisor_duplicate_suppressed' for t in e4['trace'])==1)
    suppressed=next(i for i,s in enumerate(e4['snapshots']) if s['source']=='after-suppressed:shared-first')
    before,after=e4['snapshots'][suppressed-1],e4['snapshots'][suppressed]
    check('E4:duplicate_no_snapshot_effect',all(before[k]==after[k] for k in ['orders','positions','balances','free','reserved']))
    check('E4:terminal_reserves_zero',all(Decimal(v)==0 for v in e4['reserved'].values()))
    check('E4:equal_values_distinct_fill_ids_retained',len(e4['fills'])==2 and len({f['fill_id'] for f in e4['fills']})==2 and all(Decimal(f['quantity'])==3 and Decimal(f['price'])==100 for f in e4['fills']))

    ledger=FillBoundary()
    for fill in e4['fills']:
        check('fill:first_delivery:'+fill['fill_id'],ledger.accept(fill))
        check('fill:repeated_delivery_suppressed:'+fill['fill_id'],not ledger.accept(fill))
    consolidated=deepcopy(e4);consolidated['fills']=list(ledger.fills.values())
    check('fill:consolidated_fee_cash_inventory_equations',not check_accounting(fixtures['E4-idempotency'],consolidated))
    conflict=deepcopy(e4['fills'][0]);conflict['fee']='999.00'
    check('fill:conflicting_same_identity_rejected',rejected(lambda:ledger.accept(conflict)))
    check('fill:conflict_has_no_effect',list(ledger.fills.values())==e4['fills'])

    command=fixtures['E4-idempotency']['commands'][0]
    pending=CommandBoundary(fixtures['E4-idempotency']['account_id'])
    check('command:new_identity_admitted',pending.begin(command)[0])
    original=deepcopy(pending.entries)
    check('command:pending_duplicate_blocked',not pending.begin(command)[0] and pending.entries==original)
    restored_pending=CommandBoundary.reconstruct(pending.events)
    check('command:reconstructed_pending_is_blocked',not restored_pending.begin(command)[0] and restored_pending.entries==original)
    pending.dispatched(command['command_id'], 'synthetic submission exception; effect unknown')
    check('command:dispatch_exception_not_labeled_success',pending.entries[command['command_id']]['dispatch_state']=='DISPATCH_ERROR_UNKNOWN' and not pending.begin(command)[0])
    journal=[json.loads(line) for line in (root/'journals/E4-idempotency/requests.jsonl').read_text().splitlines()]
    restored=CommandBoundary.reconstruct(journal)
    check('command:actual_durable_journal_reconstructs',restored.entries==e4['command_boundary']['entries'])
    original=deepcopy(restored.entries)
    check('command:completed_duplicate_preserves_actual_native_result',not restored.begin(command)[0] and restored.entries==original and restored.entries['shared-first']['native_order']==first)
    conflict_command=deepcopy(command);conflict_command['quantity']='7.00'
    check('command:conflicting_payload_rejected',rejected(lambda:restored.begin(conflict_command)))
    check('command:conflict_has_no_state_effect',restored.entries==original)
    check('command:missing_journal_sequence_rejected',rejected(lambda:CommandBoundary.reconstruct(journal[1:])))
    result={'checks':checks,'passed':all(c['passed'] for c in checks),
        'native_engine_executed_in_this_invocation':False,
        'artificial_fill_injection_into_engine':False,
        'origin':'supervisor-only redelivery/consolidation and readonly native observations',
        'limits':['No exchange recovery or E1 full parity','Reconstruction protects stored request identity; does not restore native positions or authorize resumption','Checks do not establish general historical market realism'],
        'consolidated_actual_fills':list(ledger.fills.values())}
    with (root/'evaluations/boundary-regressions.json').open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'failed':[c for c in checks if not c['passed']]}))
    raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':main()
