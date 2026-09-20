# Module 7 Lab - Model Answer Notes

See `eda.py`. Verified findings against `shared/trades.csv`:

- **Currency anomaly:** 17 USD trades (mean ~9,655) vs. 3 GBP trades (mean ~12,642) - these
  means are not directly comparable without a currency conversion, which is exactly the anomaly
  the lab asks delegates to name explicitly.
- **Highest total value client:** Alice Chen (38,092.40). **Highest trade count:** a three-way
  tie (Alice Chen, Ben Whitfield, Chidi Nwosu, all with 3) - worth checking a delegate noticed
  these two "highest" framings don't necessarily point to the same client.
- **Highest-value equity instrument:** AAPL (67,192.40).
- **Hypothesis check:** J. Okafor's mean trade value (~12,841) is indeed the highest of the three
  advisors, R. Alvarez's is markedly lower (~2,764) - the hypothesis holds up under a first
  check, which is a reasonable outcome for this lab (it doesn't have to be confirmed to be a good
  hypothesis, it has to be *checkable*).

Key points to check in a delegate's solution:

- **The currency-mixing anomaly must be named explicitly**, not just computed and left
  uncommented - a delegate who prints the currency breakdown without saying why it matters has
  produced the numbers but missed the point.
- **"Highest total value" and "highest trade count" are computed and compared separately.** A
  delegate who assumes they're the same client without checking both has skipped a genuine step.
- **The hypothesis must be phrased as something checkable**, e.g. naming a specific `groupby`
  that would test it - "some advisors seem busier" or "AAPL is popular" are observations, not
  hypotheses, and should be sent back for rephrasing.
