"""Freeze D-050 code, exact diffs and separate diagnostics before execution."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil

from engine_fixtures import base, command, event


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    root = Path('/workspace/technical-admission/E/correction')
    target = root / 'l2'
    target.mkdir(exist_ok=False)
    previous = here.parents[1] / 'docs/phase-iv/technical-results/E-recovery/corrected/nautilus_worker.py'
    shutil.copy2(previous, target / 'nautilus_worker.before.py')
    names = ['nautilus_worker.py', 'l2_reference.py', 'evaluate_nautilus.py', 'engine_fixtures.py', 'correction_guard.py', 'freeze_correction.py']
    for name in names:
        shutil.copy2(here / name, target / name)
    (target / 'exact.diff').write_text(''.join(difflib.unified_diff(previous.read_text().splitlines(True),
        (here / 'nautilus_worker.py').read_text().splitlines(True), fromfile='a3ec18f/nautilus_worker.py', tofile='D050-l2/nautilus_worker.py')))
    initial = event(100, 'book_snapshot', bids=[['99.00','5.00']], asks=[['100.00','1.00'],['101.00','2.00'],['102.00','1.00']])
    cases = []
    for replenish in (False, True):
        name = 'D6-replenish' if replenish else 'D6-cancel'
        events = [initial]
        commands = [command(110, name+'-buy', 'market', side='BUY', quantity='6.00', tif='GTC')]
        if replenish:
            events.append(event(300, 'book_snapshot', bids=[['102.00','5.00']], asks=[['103.00','2.00']]))
        else:
            commands.append(command(350, name+'-cancel', 'cancel', target=name+'-buy'))
        f = base(name, events, commands)
        f['diagnostic_expectations'] = {
            'native_fills_only':True, 'initial_depth_quantity':'4.00', 'initial_levels':initial['asks'],
            'no_execution_above_available_depth_before_refresh':True,
            'remainder_states_are_observations_not_automatic_defects':['PARTIALLY_FILLED','CANCELED','REJECTED','FILLED'],
            'accounting': 'original independent per-fill Decimal equations; no injected fills',
            'final_reservations_on_terminal_orders': 'must be zero to admit reservation lifecycle',
            'later_fill': 'only possible at/after offset300 with new depth103@2' if replenish else 'no additional book observation; inspect native state before/after explicit cancel',
        }
        cases.append(f)
    bundle = {'schema':'D050-depth-diagnostics-v1','cases':cases,'original_order4_diagnostic':'Original E3-L2 depth-market is the4-versus4 case; do not duplicate it'}
    (target / 'diagnostics.json').write_text(json.dumps(bundle,indent=2)+'\n')
    (root / 'observations').mkdir()
    (root / 'evaluations').mkdir()
    manifest = {'recorded_utc':datetime.now(timezone.utc).isoformat(),'authority':'D-050',
        'prior_worker_sha256':sha(previous),'sources':{n:sha(target/n) for n in names},
        'diagnostics_sha256':sha(target/'diagnostics.json'),
        'original_bundle_sha256':sha(root.parent/'fixtures/engine-cases.json'),
        'correction':'QuoteTick reference from top levels of same snapshot after its deltas at identical event/availability timestamps; risk remains enabled',
        'reason':'Prior depth-only cache caused MARKET_PRICE_UNAVAILABLE in native pre-trade risk before market submission',
        'order':'original E3-L2, D6-cancel, E4 boundary+fill consolidation; D6-replenish only if resources and evidence justify',
        'regressions':'independent accounting, unchanged source ordering, quantities/fees/cancel, trace quote provenance and risk enabled',
        'no_custom_fill_model':True,'one_L2_correction_only':True}
    (target/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest))


if __name__=='__main__':main()
