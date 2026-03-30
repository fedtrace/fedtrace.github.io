# Findings — 05: Grant Outlays via Bulk Download

*Input: 12,361 matched grants (from notebook 02 checkpoint).*  
*Methodology: `notebooks/05_grant_outlays_bulk.ipynb`*

## Confirmed

- **Outlay source:** `total_outlayed_amount_for_overall_award` field from USASpending `Assistance_PrimeTransactions` bulk download files, aggregated per FAIN.
- **Three-number coverage — grants:** 8,389/12,361 (67.9%).
- **Aggregate totals — grants:**
  - ceiling:   $54,177,633,113
  - obligated: $35,743,476,667
  - outlays: $23,484,487,826 (median outlay rate 64.6%, 37.4% of grants >80% disbursed)
- **Ceiling gap:** median 0.0%, 15.0% of grants had >50% unobligated at cancellation

**Methodology constraints:**
- `total_outlayed_amount_for_overall_award` is a cumulative field: each transaction row carries the running total for the award as of that transaction date. The record uses max() across all transactions for a given FAIN — equivalent to the most recent value. Outlay data availability is contingent on the award appearing in the downloaded archive fiscal years.
- Grant coverage is limited to ~78% of DOGE grant records with a direct USASpending link.

## Open

- Unmatched FAINs after bulk download: 10 — these grants have no outlay data via any tested path.
- Linkage path for 22% of DOGE grants with no USASpending link — unresolved.
