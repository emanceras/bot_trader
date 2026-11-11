from pathlib import Path

from bot_trader.application import build_services
from bot_trader.core.contracts import Principal
from bot_trader.core.settings import Settings
from bot_trader.persistence import Database, migrate

ROOT = Path(__file__).resolve().parents[1]


def test_original_hypotheses_are_preserved_versioned_and_not_validated(tmp_path):
    settings = Settings(repository_root=ROOT, data_dir=tmp_path / "state")
    db = Database(settings)
    migrate(db)
    services = build_services(settings)
    admin = Principal(id="admin", role="admin")
    source = ROOT / "HYPOTHESES.md"
    original = source.read_text()
    records = services.hypotheses.import_file(source, admin)
    assert [record.id for record in records] == [f"H-{n:02d}" for n in range(25)]
    for record in records:
        assert record.body["verbatim"] in original
        assert record.body["financial_validation"] is False
        assert record.body["status"] == "proposed_not_validated"
        assert record.version == 1
    assert all(record.version == 1 for record in services.hypotheses.import_file(source, admin))
    revised = tmp_path / "HYPOTHESES.md"
    revised.write_text(original + "\nMetadata-only test revision.\n")
    assert all(record.version == 2 for record in services.hypotheses.import_file(revised, admin))
    assert services.hypotheses.get("H-24", admin, 1).body == records[-1].body
    assert source.read_text() == original
    services.database.close()
    db.close()
