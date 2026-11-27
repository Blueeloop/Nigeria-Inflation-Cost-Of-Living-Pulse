# Data directory

## Raw data (`raw/`)

The downloaded NBS CPI source files live here, grouped into year folders (`CPI 2019` … `CPI 2026`).

Handling:

- Files in `raw/` are kept unmodified to preserve the source record.
- Cleaning and transformation happen in the notebook or in `src/clean_cpi.py`, with outputs saved under `data/processed/`.
- File names and coverage were checked during inspection because not every month has its own standalone file.

## Source

National Bureau of Statistics (NBS), Nigeria — monthly CPI / inflation publications.

**Attribution and licence:** to be confirmed from the NBS source pages and recorded here before the repository is published. This file will be updated with source links and the required citation.

## Derived data

### `processed/monthly_inflation.csv`

Clean monthly headline, food and core inflation series from January 2019 to October 2026.

Created by `notebooks/inflation_analysis.ipynb`. The file contains 94 monthly rows and the following fields:

- `date`
- `headline_index`, `headline_mom`, `headline_yoy`
- `food_index`, `food_mom`, `food_yoy`
- `core_index`, `core_mom`, `core_yoy`
- `index_base`
- `source_file`

Cleaning decisions:

- 2019–2023 rates come from year-end old-base workbooks.
- 2024–2026 rates come from `CPI 2026/cpi_1New_October2026.xlsx`, which contains a complete new-base back series.
- Core inflation for 2019–2023 is calculated from the core CPI index in `Table2`.
- `index_base` records whether each row uses the November 2009 = 100 or 2024 = 100 base.
- Dates were standardised to the first day of each month and sorted chronologically.
- Validation confirmed no duplicate months, no missing months and no missing inflation-rate values.

### `processed/cpi_divisions.csv`

Clean long-format CPI division series from January 2023 to October 2026.

Created by `notebooks/inflation_analysis.ipynb`. The file contains one row per division and month, with these fields:

- `date`
- `category`
- `weight`
- `index`
- `mom`
- `yoy`
- `index_base`
- `source_file`

Cleaning decisions:

- The 13 CPI divisions in `Table2` are used; overlapping aggregates are excluded.
- Division names are standardised, and calculated rate fields are named `mom` and `yoy`.
- `mom` and `yoy` are calculated from index levels within each division.
- `weight` is the CPI basket weight recorded in `Table2`.
- `index_base` is `2024 = 100` for every row.
- Insurance and financial services starts in January 2025, so its `yoy` values start in January 2026.
- Validation confirmed 13 divisions, 574 rows, no duplicate category-months and no missing index values.

### `processed/category_contributions.csv`

Estimated category contributions to headline inflation from January 2026 to October 2026.

Contribution is calculated as `(weight / 100) × category YoY rate`. Only months where all 13 divisions have YoY values are included. The sum of contributions was checked against headline YoY; the mean absolute gap was below 0.05 percentage points.

Fields:

- `date`
- `category`
- `weight`
- `yoy`
- `contribution`
- `index_base`
- `source_file`
