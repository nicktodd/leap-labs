# Module 5 Lab — Observations

## Ordering Guarantee Confirmed

Producer output:
```
Sent: key=ACC-001 partition=1 offset=0 value=SETTLED,AAPL,100
Sent: key=ACC-002 partition=0 offset=0 value=SETTLED,VOD.L,500
Sent: key=ACC-001 partition=1 offset=1 value=SETTLED,GILT10,2000
Sent: key=ACC-003 partition=1 offset=2 value=SETTLED,CORPB1,1000
Sent: key=ACC-002 partition=0 offset=1 value=SETTLED,AAPL,50
```

Consumer output:
```
partition=1 offset=0 key=ACC-001 value=SETTLED,AAPL,100
partition=1 offset=1 key=ACC-001 value=SETTLED,GILT10,2000
partition=1 offset=2 key=ACC-003 value=SETTLED,CORPB1,1000
partition=0 offset=0 key=ACC-002 value=SETTLED,VOD.L,500
partition=0 offset=1 key=ACC-002 value=SETTLED,AAPL,50
```

**ACC-001's events** (offsets 0 and 1 in partition 1) arrive in production order: AAPL then GILT10.
**ACC-002's events** (offsets 0 and 1 in partition 0) arrive in production order: VOD.L then AAPL.

This is exactly the per-account ordering guarantee reasoned about in Module 4:
- Both ACC-001 events land in partition 1 (same key → same partition).
- Both ACC-002 events land in partition 0 (same key → same partition).
- Within each partition, offsets are monotonically increasing, so the consumer reads them in the order the producer sent them.
