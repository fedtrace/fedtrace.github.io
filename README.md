# FedTrace

For any federal grant, contract, or lease: what was the stated purpose, what does the payment and audit record show, and what would a reasonable auditor conclude?

A methodology, not a watchdog. The record applies equally to any administration, any year, any program.

## Notebooks

| # | Notebook | Run |
|---|----------|-----|
| 01 | Reconstruct the financial record for cancelled federal awards — ceiling, obligated, outlays across public data sources | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fedtrace/fedtrace.github.io/blob/main/notebooks/01_data_sources.ipynb) |
| 02 | Full-scale fetch — pull raw API responses for all 13,440 contracts and 15,887 grants into resumable JSONL checkpoints | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fedtrace/fedtrace.github.io/blob/main/notebooks/02_fetch.ipynb) |
| 03 | Assemble the three-number record — join IDV child amounts, compute ceiling / obligated / outlays for every matched award | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fedtrace/fedtrace.github.io/blob/main/notebooks/03_assembly.ipynb) |
| 04 | Grant outlays investigation — probe three USASpending API endpoints; all confirmed dead ends for cancelled assistance awards | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fedtrace/fedtrace.github.io/blob/main/notebooks/04_grant_outlays.ipynb) |
| 05 | Grant outlays via bulk download — stream-parse `Assistance_PrimeTransactions` files, filter to matched FAINs, assemble grant three-number record | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fedtrace/fedtrace.github.io/blob/main/notebooks/05_grant_outlays_bulk.ipynb) |
| 06 | Combined accountability record — unified per-award schema joining contracts and grants; ceiling / obligated / outlays across all 21,873 cancelled awards | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fedtrace/fedtrace.github.io/blob/main/notebooks/06_combined.ipynb) |

## Setup

Add a `GITHUB_TOKEN_FEDTRACE` secret in Colab (key icon → left sidebar) before running any notebook that publishes results. Fine-grained PAT, resource owner `fedtrace`, Contents: Read + Write.
