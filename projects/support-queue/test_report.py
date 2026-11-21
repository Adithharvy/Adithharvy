"""Run with python -m unittest discover -s projects/support-queue from the repo root."""
import sqlite3
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class QueueSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript((HERE / "sample.sql").read_text())
        self.query = (HERE / "report.sql").read_text()

    def snapshot(self, cutoff):
        rows = self.db.execute(self.query, {"cutoff": cutoff})
        return {queue: tuple(metrics) for queue, *metrics in rows}

    def test_before_first_arrival(self):
        self.assertEqual(self.snapshot("2026-10-01 07:59"), {})

    def test_arrival_at_cutoff(self):
        self.assertEqual(self.snapshot("2026-10-01 08:00"), {"Accounts": (1, 1, 0.0, None)})

    def test_resolution_at_cutoff(self):
        before = self.snapshot("2026-10-03 11:59")["Payments"]
        after = self.snapshot("2026-10-03 12:00")["Payments"]
        self.assertEqual(before[1], 2)
        self.assertEqual(after, (3, 1, 48.0, 12.0))

    def test_queue_with_no_open_tickets(self):
        self.assertEqual(self.snapshot("2026-10-03 00:00")["Mobile"], (1, 0, None, 1.0))
