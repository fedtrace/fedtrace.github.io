# Findings — 02: Full-Scale Data Fetch

*Dataset: 9,634 single-PIID contracts, 12,377 directly-linked grants.*  
*Methodology: `notebooks/02_fetch.ipynb`*

## Confirmed

- **Contract match rate at scale:** 9,512/9,634 (98.7%) resolved via two-pass USASpending lookup.
  - As direct contracts: 9,397
  - As IDVs: 115
- **Agency match gap — at scale:**
  - Administrative Office of the U.S. Courts: 1.0 unmatched / 0.0 matched (100.0%)
  - Peace Corps: 11.0 unmatched / 0.0 matched (100.0%)
  - USAID: 1.0 unmatched / 0.0 matched (100.0%)
  - United States Trade and Development Agency: 1.0 unmatched / 0.0 matched (100.0%)
  - Pension Benefit Guaranty Corporation: 2.0 unmatched / 0.0 matched (100.0%)
  - Intelligence Community Management Account (ICMA): 1.0 unmatched / 0.0 matched (100.0%)
  - Institute of Museum And Library Services: 11.0 unmatched / 2.0 matched (84.6%)
  - Railroad Retirement Board: 5.0 unmatched / 1.0 matched (83.3%)
  - Government Accountability Office: 2.0 unmatched / 1.0 matched (66.7%)
  - Executive Office of the President: 4.0 unmatched / 2.0 matched (66.7%)
- **Grant fetch:** 12,360/12,377 (99.9%) directly-linked grants fetched.

## Open

- Three-number record assembly and aggregate findings — notebook 03.
- Linkage path for grants with no `link` host — not addressed in this notebook.
