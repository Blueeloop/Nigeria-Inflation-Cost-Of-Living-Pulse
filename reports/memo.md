# Analytical memo: Nigeria inflation and cost-of-living pulse

## Purpose

This memo explains what the cleaned CPI data shows about inflation in Nigeria: how far it rose, how it has eased, and which categories have mattered most. It uses only the publications in `data/raw/` and the derived files in `data/processed/`.

## Data and method

- The headline, food and core series cover January 2019 to October 2026.
- Rates for 2019–2023 come from old-base year-end publications. Rates for 2024–2026 come from the latest new-base publication. Index levels were not mixed across the 2024 rebase, and overlapping inflation rates were checked before the series were joined.
- The 13 CPI divisions come from `Table2` of the latest publication. Overlapping aggregates were left out of the category analysis.
- Category inflation rates were calculated from division index levels.
- Estimated contribution is `(weight / 100) × category YoY rate`. The contribution analysis covers January–October 2026, when all 13 divisions have YoY values.
- The estimated contributions came close to headline inflation, with an average absolute gap of 0.03 percentage points.

## Key findings

### 1. Headline inflation climbed sharply, then eased

Headline inflation averaged 11.39% in 2019 and 33.18% in 2024. It peaked at 34.80% in December 2024, then eased to 14.06% by October 2026.

In 2026, it stayed in a much narrower range, from 14.06% in October to 15.93% in May. That is well below the 2024 peak, though still above the 2019 average.

### 2. Food prices stayed under the most pressure

Food inflation averaged 13.73% in 2019 and 39.10% in 2024. It peaked at 40.87% in June 2024. By October 2026, it was still 19.13%, or 5.07 percentage points above headline inflation.

Across the whole period, food inflation sat 2.57 percentage points above headline inflation on average. Food was therefore a steady source of cost-of-living pressure.

### 3. Core inflation rose too, but stayed below headline

Core inflation averaged 9.77% in 2019 and 27.06% in 2024. It peaked at 29.28% in December 2024 and had fallen to 10.78% by October 2026.

Across the whole period, core inflation averaged 2.53 percentage points below headline inflation. The gap lines up with food being the stronger part of the headline measure.

### 4. High inflation rates only tell part of the story

In October 2026, the highest YoY division rates were:

- Restaurants and accommodation services: 18.73%
- Food and non-alcoholic beverages: 18.64%
- Housing, water, electricity, gas and other fuels: 14.97%
- Personal care, social protection and miscellaneous goods and services: 12.26%
- Transport: 11.48%

The contribution ranking is different because basket weight matters:

- Food and non-alcoholic beverages: 7.46 percentage points
- Restaurants and accommodation services: 2.42 percentage points
- Housing, water, electricity, gas and other fuels: 1.26 percentage points
- Transport: 1.22 percentage points
- Health: 0.58 percentage points

Food and non-alcoholic beverages carries a 40.02% weight, so its high inflation rate makes it the largest contributor by a wide margin. Restaurants and accommodation services has a smaller weight of 12.92%, but still adds a lot because its rate is high.

### 5. Food took up more of the remaining pressure in 2026

From January to October 2026, the estimated total contribution eased from 15.12 to 14.08 percentage points. Most major non-food contributions fell over this period: housing from 1.90 to 1.26, transport from 1.87 to 1.22, and health from 1.84 to 0.58 percentage points.

Food moved the other way, rising from 3.10 to 7.46 percentage points. The headline rate came down, but food made up a larger share of what was left.

## Objectives achieved

| # | Objective | Status | Evidence |
|---|---|---|---|
| 1 | Examine the historical trend of headline inflation | Done | Annual average headline inflation rose from 11.39% in 2019 to 33.18% in 2024, peaked at 34.80% in December 2024 and eased to 14.06% in October 2026. |
| 2 | Compare food, core and headline inflation | Done | Food averaged 2.57 percentage points above headline across the full period; core averaged 2.53 percentage points below. In October 2026, food was 19.13%, headline 14.06% and core 10.78%. |
| 3 | Analyse MoM and YoY inflation | Done | MoM and YoY rates were calculated in `data/processed/monthly_inflation.csv`; visual analysis focused on YoY because it is clearer for the long-run trend. |
| 4 | Identify high-rate categories and major contributors | Done | In October 2026, restaurants and accommodation services had the highest YoY rate at 18.73%, followed by food at 18.64%. The largest estimated contributions were food at 7.46 percentage points and restaurants at 2.42 percentage points. |
| 5 | Investigate changes around significant economic events without unsupported causal claims | Partial | The 2024 CPI rebase is documented and no causal event claims were made. A formal event study was not conducted. |
| 6 | Communicate findings using visualisations and a concise memo | Done | This memo and five saved figures in `reports/figures/` present the results. |

## What this means for households

The headline rate improved by October 2026, but that does not mean every cost category eased equally. Food inflation was still well above headline inflation and became the largest estimated contributor during 2026.

For households, the better headline number came with continued pressure in food, which is the biggest item in the CPI basket. Slower inflation also means prices were rising more slowly, not falling.

## Limitations

- The CPI was rebased in 2024, so index levels from different bases were not combined. Only inflation rates were used across the break.
- Weights come from the latest publication. That gives a consistent approximation, not an official decomposition for every earlier month.
- Insurance and financial services starts in January 2025, so its YoY rate only begins in January 2026. Full 13-division contribution analysis is therefore limited to 2026.
- This is a description of patterns in the CPI data. It does not establish causes or tie changes to specific events.
- NBS attribution and licence details still need to be confirmed before publication.

## Conclusion

The data shows a sharp rise in inflation through 2024, followed by easing into 2026. Food inflation has been the most persistent component and became the largest estimated contributor in the latest month. The category analysis also shows why both inflation rates and basket weights matter.

## Source and reproducibility

The source files are unmodified in `data/raw/`. The cleaning, validation, analysis and charts are reproducible in [`notebooks/inflation_analysis.ipynb`](../notebooks/inflation_analysis.ipynb). Dataset definitions and handling rules are documented in [`data/README.md`](../data/README.md).
