# Working State — FedTrace

*Last updated: 2026-03-31*

## What was accomplished this session

### Notebooks completed

| Notebook | Status | Key output |
|---|---|---|
| 04 | Done | All three USASpending API paths confirmed dead ends for grant outlays |
| 05 | Done | Grant outlays recovered via bulk archive; $23.5B across 8,389 grants |
| 06 | Written, not yet run | Combined per-award JSONL: contracts + grants unified schema |

### Grant outlay data (notebook 05) — confirmed findings
- **Archive URL format**: `https://files.usaspending.gov/award_data_archive/FY{YEAR}_All_Assistance_Full_20260306.zip` and `FY(All)_All_Assistance_Delta_20260306.zip`
- Delta file (FY(All)) + FY2026–FY2024 full files: **0 matches** for the 1,201 remaining FAINs — delta is incremental, not cumulative. Cancelled grants with no post-2023 USASpending activity don't appear.
- FY2023–FY2020 full files: matched the remaining FAINs
- Final: 12,351 matched / 10 permanently unmatched
- Three-number completeness: **67.9%** (8,389/12,361)
- Aggregates: ceiling $54.2B / obligated $35.7B / outlays $23.5B
- Median ceiling gap: **0.0%** (grants fully obligated at cancellation — contrast contracts: 42.5%)
- Median outlay rate: **64.6%**, 37.4% of grants >80% disbursed

### Combined record (notebook 06) — written, not yet run
- Notebook at `notebooks/06_combined.ipynb`
- Loads: `02_contracts_matched.jsonl`, `02_idv_amounts.jsonl`, `02_grants.jsonl`, `05_grant_outlays.jsonl`
- Per-award schema: `award_id`, `award_type`, `agency`, `recipient`, `description`, `period_start`, `period_end`, `ceiling`, `obligated`, `outlays`, `ceiling_gap`, `obligation_outlay_gap`, `ceiling_gap_pct`, `outlay_rate`, `three_number_complete`, `doge_savings`, `outlay_source`
- Publishes: `data/raw/06_awards.jsonl` (per-award), `data/outputs/06_combined.json`, `data/findings/06_combined.md`
- **Next step**: run in Colab (cells 1–4 setup, then straight through; ~5 min, no API calls)

## Current numbers (confirmed, across both award types)

| | Ceiling | Obligated | Outlays | Three-number complete |
|---|---|---|---|---|
| Contracts/IDVs (9,512) | $100.6B | $36.8B | $19.9B | 89.4% |
| Grants (12,361) | $54.2B | $35.7B | $23.5B | 67.9% |
| **All (21,873)** | **~$154.8B** | **~$72.6B** | **~$43.4B** | — (nb06 will compute) |

## What's next (priority order)

### 1. Run notebook 06 (immediate)
Open in Colab, run straight through. No downloads, no API calls — just joins existing checkpoints. Produces `06_awards.jsonl` which is the input for everything downstream.

### 2. Notebook 07: GenAI layer
Given a per-award record from `06_awards.jsonl`, produce a plain-language auditor summary. Structure:
- Load a batch of records from `06_awards.jsonl`
- For each, call Claude API with a structured prompt: "given this financial record, what does the record show?"
- Output: per-award `summary` field in auditor register (not advocacy)
- Applies the `voice` lens hard: "the record shows X" not "they cut X"

### 3. Pipeline data gaps (lower priority, can defer)
- 22% of DOGE grants with no USASpending link (3,510 records) — no FAIN, no outlay path
- Contracts where obligated > ceiling (negative ceiling gap) — count and flag

## Architecture decisions still open
- ML stack: naive baseline → classical ML → deep learning (rubric defined, not started)
- Frontend framework (deferred until pipeline confirmed)
- Whether primary output is per-award records, aggregate patterns, or both

## Key technical facts to remember

**Archive files:**
- Known-good date: `20260306` (in `ARCHIVE_DATE` constant in nb05)
- URL format: `https://files.usaspending.gov/award_data_archive/FY{YEAR}_All_Assistance_Full_20260306.zip`
- Delta file: `FY(All)_All_Assistance_Delta_20260306.zip` (0.60 GB) — incremental only, not full history
- Per-agency files also exist: `FY{YEAR}_{AGENCY_CODE}_Assistance_Full_{DATE}.zip`

**Column names (confirmed):**
- FAIN: `award_id_fain`
- Outlay (cumulative): `total_outlayed_amount_for_overall_award` — use max() per FAIN, not sum()
- Obligation (cumulative): `total_obligated_amount` — use max() per FAIN

**Contract resolution logic (used in nb03 and nb06):**
- ceiling = DOGE `value`
- obligated = `Award Amount` (contracts) or `child_award_total_obligation` (IDVs)
- outlays = `Total Outlays` (contracts) or `child_award_total_outlay` (IDVs)
- IDV amounts joined on `generated_internal_id` from `02_idv_amounts.jsonl`

**Colab session notes:**
- nb02 checkpoints are NOT committed to GitHub — they live only in Colab `/content/` across sessions
- If starting fresh Colab session: run nb02 again (resumable from checkpoint) before nb06
- nb05 grant outlays checkpoint (`05_grant_outlays.jsonl`) IS committed to GitHub
