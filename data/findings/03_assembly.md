# Findings — 03: Three-Number Record Assembly

*Input: 9,512 matched contracts, 12,361 matched grants (from notebook 02 checkpoints).*  
*Methodology: `notebooks/03_assembly.ipynb`*

## Confirmed

- **Three-number coverage — contracts:** 8,508/9,512 (89.4%) have ceiling, obligated, and outlays present.
- **Three-number coverage — grants:** 0/12,361 (0.0%) have all three numbers present.
- **Near-zero obligation at cancellation:** 1,105 contracts (11.6%) had obligated amount below 1% of ceiling.
- **Ceiling gap distribution by record type:**
  - contract: median gap 42.5%, 45.9% of records show >50% unexercised ceiling (n=9,397)
  - idv: median gap 91.9%, 80.9% of records show >50% unexercised ceiling (n=115)
- **DOGE savings vs actual gap (n=9,512):** Total DOGE-reported savings: $33,081,679,730. Total ceiling-minus-obligation gap: $63,727,720,596. DOGE `savings` = ceiling minus current obligations (unexercised headroom); termination costs for in-progress work are not netted.
- **Aggregate totals — contracts:** ceiling $100,556,324,772 / obligated $36,828,604,176 / outlays $19,888,447,235
- **Aggregate totals — grants:** ceiling $54,177,633,113 / obligated $35,743,476,667 / outlays $0
- **Aggregate totals — all awards:** ceiling $154,733,957,885 / obligated $72,572,080,843 / outlays $19,888,447,235

**Methodology constraints carried forward:**
- `ceiling`, `obligated`, and `outlays` are not interchangeable. Ceiling is the contractual maximum including unexercised options. Obligation is cumulative legally committed spend. Outlays are actual disbursements.
- IDV obligation data comes from child task order aggregates via `/api/v2/idvs/amounts/`. Top-level IDV obligation fields in USASpending are $0 by design and are not used.
- Grant coverage is limited to the approximately 78% of DOGE grant records with a direct USASpending link. The remaining 22% have no automated linkage path confirmed in this pipeline.
- USASpending data quality is limited for certain agencies (Agriculture, DHS, GSA, VA, Justice, Interior, OPM). Aggregate totals reflect only what USASpending returned — not total program spend.

## Open

- Audit coverage cross-reference — notebook 04 or later. Note: GAO/IG findings are not joinable to individual award IDs; any cross-reference is probabilistic at agency + program area + timeframe granularity only.
- Linkage path for grants with no `link` host (approx. 22% of DOGE grant records) — unresolved.
- Agency-level breakdown of the three-number record — not included in this summary output; available from local JSONL data.
