# Nigeria Inflation & Cost-of-Living Pulse

This repo tracks headline, food and core inflation in Nigeria and looks at which consumer categories have mattered most for cost-of-living pressure.

---

## Research question

How have headline, food and core inflation changed from 2019 to the latest available month, and which CPI categories have mattered most?

## Aim

To use monthly Consumer Price Index (CPI) data from the National Bureau of Statistics (NBS) to describe Nigeria's inflation trend and composition from 2019 to the latest available month, with attention to food and core inflation and the categories behind headline pressure.

## Objectives

1. Examine the historical trend of headline inflation and identify periods of acceleration, deceleration and significant changes.
2. Compare food inflation, core inflation and headline inflation.
3. Analyse month-on-month (MoM) and year-on-year (YoY) inflation.
4. Identify consumer price categories with the highest inflation rates and, where possible, the largest contributions to headline inflation.
5. Investigate inflationary changes around significant economic events without making unsupported causal claims.
6. Communicate findings using visualisations and a concise analytical memo.

---

## Project structure

```text
nigeria-inflation-cost-of-living-pulse/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── raw/                 # Unmodified NBS CPI source files, grouped by year
│   └── processed/           # Cleaned CSV datasets
├── notebooks/
│   └── inflation_analysis.ipynb
├── src/
│   ├── clean_cpi.py
│   └── generate_figures.py
├── reports/
│   ├── memo.md              # written interpretation
│   └── figures/             # generated charts
└── notes/
    └── dataset_inspection.md
```

## Data

Monthly CPI publications from Nigeria's National Bureau of Statistics (NBS), stored unmodified in `data/raw/` and grouped by year. See [`data/README.md`](data/README.md) for details, source attribution and handling rules.

## Setup

```powershell
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The notebook contains the full walkthrough. The scripts run the same cleaning and figure-generation steps:

```powershell
py -3 src/clean_cpi.py
py -3 src/generate_figures.py
```

## Memo

Read the [analytical memo](reports/memo.md) for the interpretation of the cleaned CPI data.

## Visualisations

- [Headline, food and core inflation trend](reports/figures/inflation_trends.png)
- [Latest CPI division YoY inflation](reports/figures/category_yoy_latest.png)
- [Selected CPI division trends](reports/figures/key_category_trends.png)
- [Latest estimated category contributions](reports/figures/weighted_contribution_latest.png)
- [Contribution reconciliation](reports/figures/contribution_reconciliation.png)

## Attribution and licence

Source: National Bureau of Statistics (NBS), Nigeria — CPI publications. Confirm the exact licence/attribution requirements from the NBS source pages before publication and record them in `data/README.md`.
