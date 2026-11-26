# Port Turnaround Simulator

A browser demo for comparing berth and crane capacity at a fictional container terminal. It uses synthetic vessel calls throughout.

## Run

With Python 3.11 or later, run `python simulate.py --verify` in this directory. Open the generated `demo.html` in a browser. No packages or server are needed. `python simulate.py --json` prints the results and an example event log. Use normal or surge demand, then change berths and cranes. The table compares all nine capacity options under that demand.

## Results

Normal demand, 2,160 calls per configuration across 24 paired trials.

| Berths | Cranes | 95th-percentile wait |
| ---: | ---: | ---: |
| 2 | 2 | 79.9 h |
| 3 | 2 | 79.9 h |
| 2 | 3 | 79.9 h |
| 3 | 3 | 14.2 h |

In these trials, adding only one resource leaves the other one saturated enough to preserve the original waiting times. Adding both drops the pooled 95th-percentile wait by 65.7 hours. Under surge demand the corresponding 2/2 and 3/3 waits are 199.7 and 37.0 hours.

## How it works

Each call draws an exponential interarrival time and a uniformly distributed workload of 210–720 moves. Seeds 38–61 are reused for each scenario. A vessel requests one berth and one crane together, stays until all work finishes and starts strictly in arrival order. Service takes 1.25 hours plus workload divided by 32 moves/hour. SQLite calculates waits, turnaround, the share waiting over 12 hours, and utilization. The 95th percentile is the nearest-rank statistic over the pooled calls. Each trial starts empty and ends after the last call departs.

The model omits tides, shifts, crane sharing, breakdowns and heterogeneous berths. The figures compare simulated capacity only. They do not predict throughput or justify an investment at a real port.

## Interview explanation

Hold the arrival sequence constant, change capacity, and inspect the tail of the waiting-time distribution. Walk through a single vessel in the event log to explain why adding one resource can leave the bottleneck in place.

This is an AI-assisted portfolio prototype prepared for Adith Harvy. Code is available under the [MIT License](./LICENSE). All example inputs are generated in the source.
