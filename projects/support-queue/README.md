# Support queue analysis

Which queue needs attention at the start of 3 October? This SQL exercise uses eight fictional support tickets. It reconstructs a queue snapshot from timestamps, including tickets that are closed today but were open at the reporting cutoff.

## Run

From this directory, use Python 3 with SQLite 3.38 or newer. The report builds its sample database in memory.

```sh
python report.py
python report.py --cutoff "2026-10-03 12:00"
```

## Results at 2026-10-03 00:00 UTC

| Queue | Received | Open | Oldest open (hours) | Mean resolution (hours) |
| --- | ---: | ---: | ---: | ---: |
| Payments | 3 | 2 | 36 | 6 |
| Accounts | 3 | 1 | 18 | 13 |
| Mobile | 1 | 0 | — | 1 |

Payments has the oldest unresolved ticket even though its completed ticket took only six hours. Reporting both measures exposes delays that a closed-ticket average can hide.

[Sample data](sample.sql) · [SQL query](report.sql) · [Python runner](report.py)

A ticket opened exactly at the cutoff counts as received. A ticket resolved exactly at the cutoff counts as closed. The average excludes unresolved tickets. A dash indicates no matching tickets for that metric. All timestamps are UTC.
