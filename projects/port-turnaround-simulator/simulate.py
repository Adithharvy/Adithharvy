"""Generate paired synthetic port scenarios and the interactive HTML report."""
import argparse
import itertools
import json
import math
import random
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent


def arrivals(seed, count=90, mean_gap=8.5):
    rng = random.Random(seed)
    hour = 0.0
    vessels = []
    for _ in range(count):
        hour += rng.expovariate(1 / mean_gap)
        vessels.append((hour, rng.randint(210, 720)))
    return vessels


def simulate(vessels, berths, cranes):
    """FCFS, one crane per vessel. Resources are occupied continuously until service ends."""
    berth_free = [0.0] * berths
    crane_free = [0.0] * cranes
    for vessel, (arrival, moves) in enumerate(vessels, 1):
        berth = min(range(berths), key=berth_free.__getitem__)
        crane = min(range(cranes), key=crane_free.__getitem__)
        start = max(arrival, berth_free[berth], crane_free[crane])
        departure = start + 1.25 + moves / 32
        berth_free[berth] = crane_free[crane] = departure
        yield vessel, arrival, start, departure, berth, crane


def compare():
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE calls (seed INTEGER, vessel INTEGER, arrival REAL, start REAL, departure REAL, berth INTEGER, crane INTEGER)')
        comparisons = []
        scenarios = list(itertools.product((2, 3, 4), repeat=2))
        for demand, gap in [('Normal', 8.5), ('Surge', 6.2)]:
            for berths, cranes in scenarios:
                db.execute('DELETE FROM calls')
                for seed in range(38, 62):
                    db.executemany('INSERT INTO calls VALUES (?,?,?,?,?,?,?)',
                                   ((seed, *call) for call in simulate(arrivals(seed, mean_gap=gap), berths, cranes)))
                n, average, turnaround, delayed = db.execute(
                    'SELECT count(*), avg(start-arrival), avg(departure-arrival), avg(start-arrival > 12) FROM calls'
                ).fetchone()
                tail = db.execute('SELECT start-arrival AS wait FROM calls ORDER BY wait LIMIT 1 OFFSET ?',
                                  (math.ceil(.95 * n) - 1,)).fetchone()[0]
                busy, hours = db.execute(
                    'SELECT sum(busy), sum(observed) FROM (SELECT sum(departure-start) busy, max(departure)-min(arrival) observed FROM calls GROUP BY seed)'
                ).fetchone()
                calls = db.execute(
                    'SELECT vessel, round(arrival,1), round(start,1), round(departure,1), berth+1, crane+1 FROM calls WHERE seed=38 LIMIT 12'
                ).fetchall()
                comparisons.append(dict(demand=demand, berths=berths, cranes=cranes, n=n,
                                        average=round(average, 1), p95=round(tail, 1), turnaround=round(turnaround, 1),
                                        delayed=round(100*delayed, 1), berth_use=round(100*busy/(hours*berths), 1),
                                        crane_use=round(100*busy/(hours*cranes), 1), calls=calls))
    return comparisons


def check():
    calls = list(simulate([(0, 32), (0, 32), (0, 32)], 2, 1))
    assert [row[2] for row in calls] == [0, 2.25, 4.5]
    for berths, cranes in itertools.product((2, 3, 4), repeat=2):
        available = [{}, {}]
        for _, arrival, start, depart, berth, crane in simulate(arrivals(38), berths, cranes):
            assert depart > start >= arrival
            for calendar, resource in zip(available, (berth, crane)):
                assert start >= calendar.get(resource, 0)
                calendar[resource] = depart
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.verify:
        check()
    rows = compare()
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        template = (HERE / 'template.html').read_text(encoding='utf-8')
        (HERE / 'demo.html').write_text(template.replace('__DATA__', json.dumps(rows)), encoding='utf-8')
        print('Generated demo.html from 24 paired trials per scenario')


if __name__ == '__main__':
    main()
