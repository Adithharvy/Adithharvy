"""Show queue metrics as of a UTC cutoff, using the bundled example database."""
import argparse
from datetime import datetime
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cutoff", default="2026-10-03 00:00", help="UTC: YYYY-MM-DD HH:MM")
    args = parser.parse_args()
    try:
        cutoff = datetime.strptime(args.cutoff, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
    except ValueError:
        parser.error("Use a UTC timestamp in YYYY-MM-DD HH:MM format.")
    with sqlite3.connect(":memory:") as db:
        db.executescript((HERE / "sample.sql").read_text())
        rows = db.execute((HERE / "report.sql").read_text(), {"cutoff": cutoff})
        print(" | ".join(column[0] for column in rows.description))
        for row in rows:
            print(" | ".join("—" if value is None else str(value) for value in row))


if __name__ == "__main__":
    main()
