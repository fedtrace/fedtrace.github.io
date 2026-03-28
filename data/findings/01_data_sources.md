# Findings — 01: Data Source Exploration

*Dataset: 13,440 cancelled contracts, 15,887 cancelled grants.*
*Sample: 116 contracts, 53 matched (45.7%).*
*Methodology: `notebooks/01_data_sources.ipynb`*

## Confirmed

- **Grant direct lookup:** 12,377/12,377 USASpending-linked grants yield extractable award IDs; 10/10 direct `/api/v2/awards/{id}/` lookups succeeded. Covers 78% of cancelled grants.
- **Three-number record reconstructable** for matched awards (ceiling / obligated / outlays). Outlay data present for 90.6% of matched records.
- **Ceiling-to-obligated gap:** median 41.4% for direct contracts; 92.8% for IDVs. IDVs carry large ceiling headroom by design — framework vehicles that obligate through task orders.
- **Savings field vs obligated amount:** for 28.3% of matched records, the savings field value exceeds the USASpending obligated amount. These fields measure different things — savings = ceiling minus current obligations; Award Amount / `child_award_total_obligation` = cumulative committed spend. Structurally expected for IDVs and large-option contracts.
- **USASpending match gap is structural**, not a join methodology issue. Gap concentrated in: Agriculture (10 unmatched), DHS (8), GSA (8), VA (6), Justice (4), Interior (4), OPM (3). Known data quality degradation at these agencies.
- **IDV child amounts:** correct fields are `child_award_total_obligation` and `child_award_total_outlay` from `/api/v2/idvs/amounts/{generated_internal_id}/`.

## Open

- Linkage path for 3,510 grants (22%) with no host in the `link` field. Candidates: USASpending bulk `Assistance_PrimeTransactions` join, SAM.gov cross-reference, or document as unresolvable gap.
