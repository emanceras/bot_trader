"""Offline checks of the acquisition gate; no network or market rows."""

import unittest
from types import SimpleNamespace

from kraken_acquire import checked_headers


class AcquisitionGateTests(unittest.TestCase):
    def response(self, **changes):
        values = {
            "status": 200,
            "url": "https://example.invalid/allowed.zip",
            "headers": {
                "Content-Length": "123",
                "ETag": '"fixture"',
                "Content-Type": "application/zip",
            },
        }
        values.update(changes)
        return SimpleNamespace(**values)

    def check(self, response):
        return checked_headers(response, "https://example.invalid/allowed.zip", 123, '"fixture"')

    def test_expected_identity_is_accepted(self):
        self.assertEqual(self.check(self.response())["Content-Length"], "123")

    def test_status_or_redirect_is_rejected(self):
        for changes in ({"status": 206}, {"url": "https://example.invalid/other.zip"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.check(self.response(**changes))

    def test_identity_size_and_encoding_changes_are_rejected(self):
        for field, value in (
            ("Content-Length", "124"),
            ("Content-Length", None),
            ("ETag", '"other"'),
            ("Content-Type", "text/html"),
            ("Content-Encoding", "gzip"),
        ):
            response = self.response()
            response.headers[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.check(response)


if __name__ == "__main__":
    unittest.main()
