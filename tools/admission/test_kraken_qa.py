"""Small synthetic regression checks for the external structural audit only."""

import io
import unittest
from decimal import Decimal
from zipfile import ZIP_DEFLATED, ZipFile

from kraken_qa import (
    ARCHIVE_SHA256, START, aggregate_trade, edge_records, stream_member, validate_records,
    verify_inventory_identity,
)


class AuditChecks(unittest.TestCase):
    def test_acquired_identity_is_bound(self):
        verify_inventory_identity("ohlcvt", {"sha256": ARCHIVE_SHA256["ohlcvt"]})
        with self.assertRaises(ValueError):
            verify_inventory_identity("ohlcvt", {"sha256": "0" * 64})

    def test_edges_remove_overlap_and_header(self):
        data = b"a,b\n1,2\n3,4\n"
        self.assertEqual(edge_records(data, data, len(data), 2, True),
                         [(0, ["1", "2"]), (1, ["3", "4"])])

    def test_stream_counts_last_record_without_newline(self):
        container = io.BytesIO()
        with ZipFile(container, "w", ZIP_DEFLATED) as archive:
            archive.writestr("rows.csv", "header\nfirst\nlast")
        with ZipFile(container) as archive:
            facts, _, _ = stream_member(archive, "rows.csv")
        self.assertEqual(facts["physical_lines"], 3)
        self.assertTrue(facts["crc_verified"])

    def test_metadata_absence_is_not_declared_delisting_or_duplicate(self):
        row = [str(START), "10", "1", "", "", "", ""]
        result = validate_records([(0, row), (1, row)], "trades", None)
        self.assertFalse(result["errors"])
        self.assertEqual(result["notes"]["metadata_and_trade_id_absent"], 2)
        self.assertEqual(result["notes"]["repeated_time_price_quantity_candidate"], 1)

    def test_duplicate_id_and_time_regression_are_detected(self):
        rows = [(0, [str(START + 1), "10", "1", "b", "l", "", "9"]),
                (1, [str(START), "10", "1", "s", "l", "", "9"])]
        errors = validate_records(rows, "trades", None)["errors"]
        self.assertEqual(errors["timestamp_regression_in_sample"], 1)
        self.assertEqual(errors["duplicate_trade_id_in_sample"], 1)

    def test_exact_notional_is_not_close_times_volume(self):
        bucket = {}
        aggregate_trade(bucket, Decimal(START), Decimal("10"), Decimal("0.1"))
        aggregate_trade(bucket, Decimal(START + 1), Decimal("11"), Decimal("0.2"))
        self.assertEqual(bucket["exact_quote_notional"], Decimal("3.2"))
        self.assertEqual(bucket["volume"], Decimal("0.3"))
        self.assertNotEqual(bucket["close"] * bucket["volume"], bucket["exact_quote_notional"])


if __name__ == "__main__":
    unittest.main()
