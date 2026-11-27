from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

OLD_BASE_SOURCES = {
    2019: "CPI 2019/cpi_1NewDec2019.xlsx",
    2020: "CPI 2020/cpi_1NewDECEMBER2020.xls",
    2021: "CPI 2021/cpi_1NewDEC2021.xlsx",
    2022: "CPI 2022/cpi_1NewDEC2022.xlsx",
    2023: "CPI 2023/cpi_1NewDECEMBER2023.xlsx",
}
LATEST_SOURCE = "CPI 2026/cpi_1New_October2026.xlsx"

CATEGORY_COLUMNS = {
    14: "Food and non-alcoholic beverages",
    15: "Alcoholic beverages, tobacco and narcotics",
    16: "Clothing and footwear",
    17: "Housing, water, electricity, gas and other fuels",
    18: "Furnishings, household equipment and routine household maintenance",
    19: "Health",
    20: "Transport",
    21: "Information and communication",
    22: "Recreation, sport and culture",
    23: "Education services",
    24: "Restaurants and accommodation services",
    25: "Insurance and financial services",
    26: "Personal care, social protection and miscellaneous goods and services",
}

MONTH_NAMES = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "febuary": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sept": 9,
    "sep": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}


def numeric(series):
    return pd.to_numeric(series, errors="coerce")


def month_number(value):
    if pd.isna(value):
        return None
    text = str(value).lower()
    for name, number in MONTH_NAMES.items():
        if name in text:
            return number
    return None


def calendar_dates(raw, year_col, month_col):
    year = None
    previous_month = None
    dates = []
    for _, row in raw.iterrows():
        raw_year = row[year_col]
        explicit_year = pd.notna(raw_year) and str(raw_year).strip().isdigit()
        if explicit_year:
            year = int(raw_year)
        month = month_number(row[month_col])
        if not explicit_year and year is not None and previous_month == 12 and month == 1:
            year += 1
        dates.append(pd.Timestamp(year=year, month=month, day=1) if year and month else pd.NaT)
        if month:
            previous_month = month
    return pd.Series(dates)


def require_sources():
    for relative_path in [*OLD_BASE_SOURCES.values(), LATEST_SOURCE]:
        path = RAW_DIR / relative_path
        if not path.exists():
            raise FileNotFoundError(path)


def build_old_monthly():
    frames = []
    for year, relative_path in OLD_BASE_SOURCES.items():
        path = RAW_DIR / relative_path
        table1 = pd.read_excel(path, sheet_name="Table1", header=None)
        table2 = pd.read_excel(path, sheet_name="Table2", header=None)

        dates1 = pd.to_datetime(calendar_dates(table1, 0, 1), errors="coerce")
        rates = pd.DataFrame(
            {
                "date": dates1,
                "headline_index": numeric(table1[2]),
                "headline_mom": numeric(table1[4]),
                "headline_yoy": numeric(table1[5]),
                "food_index": numeric(table1[12]),
                "food_mom": numeric(table1[14]),
                "food_yoy": numeric(table1[15]),
            }
        )
        rates = rates[rates["date"].dt.year == year]

        dates2 = pd.to_datetime(calendar_dates(table2, 0, 1), errors="coerce")
        core_index = numeric(table2[4])
        core = pd.DataFrame(
            {
                "date": dates2,
                "core_index": core_index,
                "core_mom": core_index.pct_change(1, fill_method=None) * 100,
                "core_yoy": core_index.pct_change(12, fill_method=None) * 100,
            }
        )
        core = core[core["date"].dt.year == year]

        frame = rates.merge(core, on="date", how="left")
        frame["index_base"] = "November 2009 = 100"
        frame["source_file"] = relative_path
        frames.append(frame)

    return pd.concat(frames, ignore_index=True).sort_values("date").reset_index(drop=True)


def build_new_monthly():
    path = RAW_DIR / LATEST_SOURCE
    table = pd.read_excel(path, sheet_name="Table1", header=None)
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(table[22], errors="coerce"),
            "headline_index": numeric(table[2]),
            "headline_mom": numeric(table[4]),
            "headline_yoy": numeric(table[5]),
            "food_index": numeric(table[12]),
            "food_mom": numeric(table[14]),
            "food_yoy": numeric(table[15]),
            "core_index": numeric(table[17]),
            "core_mom": numeric(table[19]),
            "core_yoy": numeric(table[20]),
        }
    )
    frame = frame[frame["date"] >= "2024-01-01"].copy()
    frame["index_base"] = "2024 = 100"
    frame["source_file"] = LATEST_SOURCE
    return frame.sort_values("date").reset_index(drop=True)


def build_monthly():
    frame = pd.concat([build_old_monthly(), build_new_monthly()], ignore_index=True)
    return frame.drop_duplicates(subset="date", keep="last").sort_values("date").set_index("date")


def validate_monthly(monthly):
    expected_dates = pd.date_range("2019-01-01", "2026-10-01", freq="MS")
    rate_columns = [
        "headline_mom",
        "headline_yoy",
        "food_mom",
        "food_yoy",
        "core_mom",
        "core_yoy",
    ]
    validation = {
        "rows": len(monthly),
        "first_month": monthly.index.min().strftime("%Y-%m"),
        "last_month": monthly.index.max().strftime("%Y-%m"),
        "duplicate_dates": int(monthly.index.duplicated().sum()),
        "missing_months": [date.strftime("%Y-%m") for date in expected_dates.difference(monthly.index)],
        "extra_months": [date.strftime("%Y-%m") for date in monthly.index.difference(expected_dates)],
        "missing_rate_values": monthly[rate_columns].isna().sum().to_dict(),
    }

    if validation["rows"] != 94:
        raise ValueError("Expected 94 monthly rows")
    if validation["duplicate_dates"] != 0:
        raise ValueError("Duplicate dates found")
    if validation["missing_months"] or validation["extra_months"]:
        raise ValueError("Monthly coverage is incomplete")
    if sum(validation["missing_rate_values"].values()) != 0:
        raise ValueError("Missing inflation rates found")
    return validation


def build_divisions():
    path = RAW_DIR / LATEST_SOURCE
    table = pd.read_excel(path, sheet_name="Table2", header=None)
    dates = pd.to_datetime(table[30], errors="coerce")

    parts = []
    for column, name in CATEGORY_COLUMNS.items():
        part = pd.DataFrame(
            {
                "date": dates,
                "category": name,
                "weight": numeric(table.iloc[2, column]),
                "index": numeric(table[column]),
            }
        )
        parts.append(part.dropna(subset=["date", "index"]))

    divisions = pd.concat(parts, ignore_index=True)
    divisions = divisions.sort_values(["category", "date"]).reset_index(drop=True)
    divisions["mom"] = divisions.groupby("category")["index"].pct_change(1, fill_method=None) * 100
    divisions["yoy"] = divisions.groupby("category")["index"].pct_change(12, fill_method=None) * 100
    divisions["index_base"] = "2024 = 100"
    divisions["source_file"] = LATEST_SOURCE
    return divisions


def validate_divisions(divisions):
    validation = {
        "categories": divisions["category"].nunique(),
        "rows": len(divisions),
        "duplicate_category_months": int(divisions.duplicated(["category", "date"]).sum()),
        "missing_index_values": int(divisions["index"].isna().sum()),
        "missing_yoy_values": int(divisions["yoy"].isna().sum()),
        "weight_sum": round(divisions.groupby("category")["weight"].first().sum(), 2),
    }

    if validation["categories"] != 13:
        raise ValueError("Expected 13 CPI divisions")
    if validation["duplicate_category_months"] != 0:
        raise ValueError("Duplicate category-month rows found")
    if validation["missing_index_values"] != 0:
        raise ValueError("Missing category index values found")
    if validation["missing_yoy_values"] != 156:
        raise ValueError("Unexpected number of missing YoY values")
    return validation


def build_contributions(divisions):
    counts = divisions.dropna(subset=["yoy"]).groupby("date")["category"].nunique()
    complete_dates = counts[counts == len(CATEGORY_COLUMNS)].index
    contributions = divisions[divisions["date"].isin(complete_dates)].copy()
    contributions["contribution"] = contributions["weight"] / 100 * contributions["yoy"]
    return contributions[
        ["date", "category", "weight", "yoy", "contribution", "index_base", "source_file"]
    ]


def main():
    require_sources()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    monthly = build_monthly()
    validate_monthly(monthly)
    monthly.reset_index().to_csv(PROCESSED_DIR / "monthly_inflation.csv", index=False)

    divisions = build_divisions()
    validate_divisions(divisions)
    divisions.to_csv(PROCESSED_DIR / "cpi_divisions.csv", index=False)

    contributions = build_contributions(divisions)
    contributions.to_csv(PROCESSED_DIR / "category_contributions.csv", index=False)

    for name in ["monthly_inflation.csv", "cpi_divisions.csv", "category_contributions.csv"]:
        print(f"Saved: {(PROCESSED_DIR / name).relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
