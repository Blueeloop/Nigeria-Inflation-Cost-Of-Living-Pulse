# Dataset inspection notes

## Scope

Inspected all files in `data/raw/` without modifying them. The analysis period of interest is 2019 to the latest month available in the workbooks.

## File inventory

- 91 NBS CPI files: 87 `.xlsx` and 4 `.xls`.
- Files are grouped into `CPI 2019` through `CPI 2026`.
- Month coverage by filename:
  - 2019–2023: all 12 months in each year.
  - 2024: January–October; November and December files are absent.
  - 2025: February–December; January file is absent.
  - 2026: January–October.
- No duplicate month by filename and no exact duplicate files by file hash.
- Latest month present: October 2026.

## Workbook structure

All 91 workbooks opened successfully. Five distinct sheet-name patterns were found, mainly:

- `Table1`, `Table2`, `Table3`, `Table4`, `Table-5`
- Some 2026 workbooks also contain `Table1 (2)`, `Table2 (2)`, `Table3 (2)`, `Table3 (3)`, and `Table4 (2)`.
- Two workbooks contain contribution sheets: `Contr-M`, `Contr-Y`, and `Contr-12MA`.

Main table meanings:

- `Table1`: composite CPI index and inflation rates for all items, food, and non-food/core-style aggregates.
- `Table2`: composite CPI index levels and weights by consumer category.
- `Table3`: urban CPI.
- `Table4`: rural CPI.
- `Table-5`: state-level CPI.

## CPI base and rebasing

- Older workbooks use **November 2009 = 100** as the CPI base, with old weights summing to 1000.
- They also reference a legacy **September 1985 = 100** series.
- From the 2025 workbooks, NBS uses a new base, **Year 2024 = 100**, with weights summing to 100.
- This is a structural break in the index series. Index levels from the old and new bases must not be mixed without rebasing or using published back series.
- The October 2026 workbook `Table1` contains a new-base back series from January 2023 to October 2026.

## Inflation measures available

`Table1` contains monthly index, 12-month average index, month-on-month change, year-on-year change, and 12-month average change.

Column positions change across layouts:

- 2019–2023 old layout:
  - headline YoY: column 5
  - food YoY: column 15
  - core is not explicitly labelled in `Table1`; core index is in `Table2`, column 4.
- 2024 old-layout reports:
  - headline YoY: column 5
  - food YoY: column 10
  - core YoY: column 15
- 2025–2026 new-base reports:
  - headline YoY: column 5
  - food YoY: column 15
  - core YoY: column 20

`Table2` contains category index levels and weights, so category inflation rates can be calculated from index levels where consecutive-year values are available.

## Data quality checks

- No exact duplicate files.
- No duplicate months by filename.
- The October 2026 `Table1` has 46 monthly rows, January 2023 to October 2026, with no missing or duplicate months.
- In that workbook, YoY rates are missing for all 2023 months. This is expected because the new-base back series starts in January 2023, so there is no January–December 2022 comparison in the new-base table.
- Year-end files for 2019–2023 each contain 12 months with no missing headline or food YoY values.
- Core index values in `Table2` are complete for all 12 months in each year from 2019 to 2023.
- Overlap checks:
  - 2024 October report vs October 2026 report: headline, food and core YoY agree to floating-point precision.
  - December 2025 report vs October 2026 report: 2024–2025 headline, food and core YoY agree exactly.
- Structural inconsistencies to handle during cleaning:
  - sheet names and table dimensions vary;
  - column positions change when NBS changes the layout;
  - 2024 October `Table1` omits an explicit year label for 2024 rows, so year must be inferred carefully;
  - base-year change from November 2009 = 100 to 2024 = 100;
  - missing standalone files for 2024 November–December and 2025 January, although these months appear in the latest workbook's new-base back series.

## Contribution data

Only two workbooks contain contribution sheets:

- `CPI 2023/cpi_1NewNOVEMBER2023.xlsx`
- `CPI 2024/cpi_1NewAPR2024.xlsx`

These provide contribution to month-on-month, year-on-year and 12-month average inflation for selected categories. They are useful evidence for understanding contribution, but they do not form a continuous monthly contribution series.

## Concepts to keep in mind

- **CPI index vs inflation rate:** an index is a price-level number relative to a base period; an inflation rate is the percentage change in that index.
- **MoM vs YoY:** MoM compares with the previous month; YoY compares with the same month one year earlier.
- **Headline, food and core:** headline is all items; food tracks food prices; core here is all items less farm produce and energy in the new layout.
- **Inflation rate vs contribution:** a category can have a high inflation rate but a small contribution if it has a small weight.
- **Weights:** category weights determine how much each category influences the aggregate index.
- **Slowing inflation vs falling prices:** slower inflation means prices are rising more slowly, not necessarily falling.
- **Volatility:** the degree of variation in a series over time.
- **Correlation vs causation:** co-movement does not prove that one series caused another.
- **Structural break/rebasing:** a methodology change can alter index levels, so historical comparisons need care.

## Cleaning approach used

- Use year-end old-base workbooks for 2019–2023 headline, food and core rates.
- Use the October 2026 workbook's new-base back series for 2024–2026 headline, food and core rates.
- Calculate core inflation for 2019–2023 from the `Table2` core index, using YoY percentage change.
- Use the latest `Table2` division index levels and weights for the 2023–2026 category series.
- Treat the 2024 rebasing as a structural break and document it in the analysis.
- Estimate category contributions only for months where all 13 divisions have YoY values.
