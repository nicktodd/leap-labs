# PaySprint Notifications API — 30-Day Downtime Log

**Service Level Objective (SLO):** 99.9% availability, measured over a rolling 30-day window.

**Recorded downtime per day (minutes):**

| Day | Downtime (min) | Notes |
|---|---|---|
| 1 | 0.5 | Brief blip, self-resolved |
| 2 | 0 | |
| 3 | 1.0 | |
| 4 | 0 | |
| 5 | 0.5 | |
| 6 | 0 | |
| 7 | 0 | |
| 8 | 2.0 | Third-party SMS provider timeout |
| 9 | 0 | |
| 10 | 0.5 | |
| 11 | 0 | |
| 12 | 1.0 | |
| 13 | 0 | |
| 14 | 0.5 | |
| 15 | 0 | |
| 16 | 0 | |
| 17 | 35.0 | Bad deploy, rolled back, root cause: missing config value in production |
| 18 | 0 | |
| 19 | 0.5 | |
| 20 | 0 | |
| 21 | 1.0 | |
| 22 | 0 | |
| 23 | 0.5 | |
| 24 | 0 | |
| 25 | 0 | |
| 26 | 2.0 | |
| 27 | 0 | |
| 28 | 0.5 | |
| 29 | 0 | |
| 30 | 6.0 | Database failover took longer than expected |

**Total minutes in the 30-day window:** 43,200 (30 x 24 x 60)
