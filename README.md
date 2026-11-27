# Nigeria Inflation & Cost-of-Living Pulse

An exploratory data analysis of Nigeria's inflation trends, comparing headline, food and core inflation while investigating consumer price categories and cost-of-living pressures.

---

## Research question

How has inflation in Nigeria evolved from 2019 to the latest available period, how have food and core inflation contributed to the trend in headline inflation, and which consumer price categories have been the major drivers of inflationary pressure?

## Aim

To analyse the trend and composition of inflation in Nigeria from 2019 to the latest available period using monthly Consumer Price Index (CPI) data from the National Bureau of Statistics (NBS), with particular emphasis on the relative behaviour of headline, food and core inflation, and identifying consumer price categories contributing most significantly to inflationary pressure.

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
│   └── raw/                 # Unmodified NBS CPI source files, grouped by year
├── notebooks/
│   └── inflation_analysis.ipynb   # added during analysis
├── src/                     # reusable helper scripts, if needed
├── reports/
│   ├── memo.md
│   └── figures/
└── notes/
    └── concepts.md          # running glossary of concepts covered
```

## Data

Monthly CPI publications from Nigeria's National Bureau of Statistics (NBS), stored unmodified in `data/raw/` and grouped by year. See [`data/README.md`](data/README.md) for details, source attribution and handling rules.

## Setup

```powershell
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> Notebook, results and memo will be added as the analysis progresses.

## Attribution and licence

Source: National Bureau of Statistics (NBS), Nigeria — CPI publications. Confirm the exact licence/attribution requirements from the NBS source pages before publication and record them in `data/README.md`.
