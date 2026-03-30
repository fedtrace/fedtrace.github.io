# FedTrace

## Problem

Federal spending is technically public but practically illegible. Awards, payments, audits, and cancellations live in separate systems with no shared key. Nobody connects them at scale — not to validate cuts, not to surface waste, not to hold programs accountable to their own stated goals. FedTrace is the infrastructure for doing that: a multi-source evidence synthesizer that reconstructs the full lifecycle of any federal expenditure and produces a structured accountability record against it.

## What this enables that nothing else does

For any federal grant, contract, or lease: what was the stated purpose, what does the payment and audit record show, and what would a reasonable auditor conclude? The methodology applies to any award — active, cancelled, renewed, or modified — across any administration and any year.

## Vision

FedTrace is accountability infrastructure, not a watchdog. The distinction is load-bearing:

- A watchdog has a target. This tool has a methodology.
- The methodology applies equally to any administration, any year, any program.
- The product is a structured evidence record. What anyone concludes from it is their business.

If any artifact — code comment, output label, notebook heading, UI copy — reads as advocacy or accusation, rewrite it. The test: could a GAO auditor sign their name to this framing?

## Lenses

Apply these on every artifact:

- `traceability` — every claim needs a source; no inference without evidence; the tool's value is that it shows its work
- `voice` — auditor register, not journalist register; "the record shows X" not "they cut X"; findings, not accusations
- `criterion` — three proxies to name and resist: (1) any single number (ceiling, obligation, cut count) standing in for the full three-number record; (2) audit findings as a proxy for waste — coverage is structurally uneven and GAO's High Risk List does not overlap with the cancelled programs; (3) "no audit findings" as a proxy for "justified" — absence of findings reflects audit coverage, not program quality

## Data Sources

| Source | What it provides | Status |
|---|---|---|
| DOGE API | Cancellations (grants, contracts, leases), payment justifications | Confirmed |
| USASpending.gov | Cumulative obligations, vendor names, stated purposes, outlays | Confirmed |
| SAM.gov Contract Awards API | Contract details, IDV/task-order hierarchy, agency, NAICS codes (replaced FPDS portal Feb 2026) | Confirmed |
| Federal Audit Clearinghouse | Single audit findings by recipient entity (program-level, not award-level) | Confirmed |
| Federal Register | Regulatory context, triggering executive orders | Tentative |
| Treasury DATA Act | Standardized payment flows across agencies | Tentative |
| OpenSecrets | Lobbying relationships, campaign finance | Tentative |
| GDELT | News coverage volume and tone around cancellations | Tentative |
| GAO / IG reports | Agency/program-level audit findings — not joinable to individual awards | Tentative |

## Data Field Semantics — Confirmed

For any federal contract, three numbers matter and must never be conflated:

| Number | What it is | Where it lives |
|---|---|---|
| **Ceiling** | Contractual maximum including all unexercised options (FPDS: Base and All Options Value) | DOGE `value`, FPDS |
| **Obligated** | Cumulative legally committed spend (sum of all obligation modifications) | USASpending `Award Amount` |
| **Outlays** | Actual payments disbursed | Treasury / USASpending `Total Outlays` |

These are not interchangeable. An accountability record without all three is incomplete. Any single number — ceiling, obligation, or outlay — can be misleading in isolation.

**IDV/task-order hierarchy:** A DOGE `piid` may resolve to an IDV (Indefinite Delivery Vehicle) record in USASpending with $0 in obligations. All actual spending flows through child task orders under that IDV, each with their own PIID. To reconstruct "was money actually flowing?", aggregate child task order obligations by `parent_award_id = IDV PIID`. Reading the IDV record's value fields alone is wrong.

**On DOGE specifically:** DOGE `savings` = ceiling minus current obligations. Unexercised headroom, not recovered money. Termination costs owed for work-in-progress are not netted.

**Three-number record — at-scale findings (notebook 03).** Across 9,512 matched contracts: ceiling $100.6B / obligated $36.8B / outlays $19.9B. Three-number completeness (all three present): 89.4%. Ceiling-to-obligation gap: contracts median 42.5%, IDVs median 91.9% — IDV pattern confirmed at scale. Near-zero obligation (<1% of ceiling) at cancellation: 11.6% of contracts (1,105 records). DOGE-reported savings total $33.1B; ceiling-minus-obligation gap computes to $63.7B — the discrepancy is under investigation (likely: obligations changed between DOGE publication and USASpending fetch, or DOGE `value` field differs from FPDS ceiling in some records). Negative mean gap (contracts: -403.7%, IDVs: -167.7%) indicates a subset of records where obligated > ceiling — driven by contract modifications that added obligations beyond the original award value; these are not excluded from aggregates but should be flagged in any per-award output.

**Grant outlays not returned by USASpending award endpoint.** The `/api/v2/awards/{id}/` endpoint returns `total_outlays: null` for assistance awards. Confirmed: the field exists in the response but the value is genuinely null — not a field name mismatch. Across 12,361 matched grants: ceiling $54.2B / obligated $35.7B / outlays: not available. Two candidate paths: (1) `/api/v2/awards/funding/{award_id}/` returns federal account-level funding breakdowns including `gross_outlay_amount` — award_id already present in grants JSONL, so this is testable without re-fetch; (2) USASpending bulk download (Assistance_PrimeTransactions) contains transaction-level outlay data but requires a local join. Three-number completeness for grants: 0% until resolved.

Sources: FPDS Data Dictionary V1.5 (field definitions); GovTribe contract hierarchy documentation (IDV/task-order structure).

## Methodology Constraints — Confirmed

These limit what the tool can claim. State them in any output that touches these areas.

**GAO/IG findings are not joinable to individual awards.** Reports are organized by agency and program area, not by PIID or FAIN. There is no public database that returns "audit findings for award #X." The cross-reference is probabilistic at best: agency + program area + timeframe. Any claim linking a specific cancellation to a prior audit finding must be sourced to the report directly, not inferred from a join.

**Audit coverage is structurally uneven.** Social service grants go through Single Audits (high finding rate by design). Defense contracts go through DCAA audits with different criteria and thresholds. A cross-reference that uses audit findings as a "prior waste" signal will systematically over-flag social programs and under-flag defense programs — not because of actual waste differences, but because of audit coverage differences. State this limitation whenever audit findings are used.

**GAO's High Risk List (2025) does not overlap with primary DOGE targets.** GAO flags DoD acquisition, Medicare/Medicaid, and federal IT. DOGE primarily targeted USAID, CFPB, and programs at USDA, HHS, and State — none on the GAO list. A cross-reference between cancellations and audit records will mostly show cancelled programs with clean audit records. The non-overlap is a finding about the relationship between the two lists, not evidence that the cuts were wrong or right.

**USASpending data quality is limited.** The empirical confirmation is in notebooks 01 and 02. Any analysis must acknowledge these gaps rather than treat USASpending as ground truth. Do not cite unverified external accuracy estimates as findings.

**USASpending PIID match gap — at-scale finding (notebook 02).** Full two-pass lookup across 9,634 unique single-PIID contracts: 9,512 matched (98.7%). Unmatched records concentrated in small independent agencies — Peace Corps (100% unmatched, 11 records), Institute of Museum and Library Services (84.6%), Railroad Retirement Board (83.3%), Executive Office of the President (66.7%), Treasury (48.5%). The stratified sample in notebook 01 showed lower apparent match rates because it oversampled agencies with known data quality gaps (Agriculture, DHS, GSA, VA, Justice, Interior, OPM). The at-scale result does not vindicate those agencies — it reflects sampling, not improved data quality at those agencies.

**Duplicate PIIDs in DOGE contract data (notebook 02).** 13,440 raw DOGE contract rows contain 3,773 duplicate PIID entries, yielding 9,634 unique single-PIID contracts. Cause unconfirmed. Deduplication keeps the last occurrence for metadata lookup.

**IDV child obligation field is `child_award_total_obligation`.** The `/api/v2/idvs/amounts/{generated_internal_id}/` endpoint does not return `obligated_amount`. The correct fields are `child_award_total_obligation` (obligations) and `child_award_total_outlay` (outlays). The `generated_internal_id` from USASpending search results is the correct key for this endpoint.

**Grant linkage path:** DOGE `link` field (78% populated) → extract `generated_unique_award_id` → `GET /api/v2/awards/{id}/`. For the remaining 22%: USASpending bulk download (`Assistance_PrimeTransactions`) + local join on normalized recipient name + agency code + amount tolerance + fiscal year.

## Notebook Design

The infrastructure is organized around inquiry. Data responds to questions; it does not answer them. Conclusions drawn from partial evidence are provisional and must be marked as such — the same finding may read differently as coverage expands.

Each notebook has four parts:

**Driving questions** — the motivating inquiry, in auditor register: specific, falsifiable. Questions are the compass, not the deliverable. Updated as understanding deepens, never closed prematurely.

**What the record shows** — findings produced by this run. Stable once written. State what the data showed, not what it implies. "The record shows X" not "X is true."

**Current interpretation** — what the findings suggest given current evidence. Explicitly provisional. Label it as such. The same numbers may support a different interpretation when coverage improves or a methodology gap is closed.

**What the record shows — and what remains open** — a structured section at the end of each notebook separating: (1) confirmed findings, (2) partial findings with provisional interpretation, (3) open questions with no evidence yet. This is the handoff document for the next notebook. Update it each run.

**Published output** (JSON) — the evidence record. Contains findings, not interpretations. Distinct from the driving questions and from any conclusions a reader might draw.

The notebook is the investigation. The driving questions are the compass. The published JSON is the record.

## Open Decisions

**Data pipeline — unresolved:**
- Grant linkage for 22% with no `link` host (3,510 records) — identify alternative path (USASpending bulk `Assistance_PrimeTransactions` join, SAM.gov, or document as unresolvable gap)
- Grant outlay data — `total_outlays` is null for all assistance awards from `/api/v2/awards/{id}/` (confirmed: field exists, value is genuinely null). Candidate path: `POST /api/v2/awards/funding/` returns per-federal-account rows with `gross_outlay_amount`; summing these rows yields award-level outlays. Notebook 04 probes and fetches this. Fallback if endpoint is also null: USASpending bulk download `Assistance_PrimeTransactions`.
- Contracts where obligated > ceiling (negative ceiling gap) — identify count and cause; likely contract modifications; flag in per-award output

**Architecture:**
- ML stack and three-model structure (rubric: naive baseline → classical ML → deep learning)
- Ablation experiment design
- GenAI layer (plain-language explanation of spending patterns)
- Frontend framework
- Whether the primary output is per-award accountability records, aggregate patterns, or both
- Whether recommender component is contract similarity or something else

**Operations:**
- Pipeline agent: eventually schedule the validated notebook pipeline to auto-publish to the site
- Public collaboration: whether to open issues/PRs, and under what anonymity model (contributors must understand the identity hard rule before any public artifact is created)

## What Not to Build Yet

- A dashboard (visualization comes after data pipeline works)
- A general federal spending explorer (the accountability angle is the product — stay anchored to it)
- Anything requiring non-public data

## Authorship

```bash
git config user.name "Claude"
git config user.email "noreply@anthropic.com"
```

Set at repo level. Verify before first commit on any new machine. No co-author lines in commit messages.

## Identity — Hard Rule

No identifying information about any human contributor in any project artifact: code, comments, commit messages, issues, PRs, documentation. This rule is permanent and non-negotiable.

- No real names, handles, affiliations, or institutional associations
- No personal API keys or tokens ever committed — use environment variables
- No co-author lines in commit messages
