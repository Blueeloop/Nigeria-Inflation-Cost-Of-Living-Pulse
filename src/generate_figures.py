from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
FIGURES_DIR = PROJECT_DIR / "reports" / "figures"

SELECTED_CATEGORIES = [
    "Food and non-alcoholic beverages",
    "Restaurants and accommodation services",
    "Housing, water, electricity, gas and other fuels",
    "Transport",
]


def load_data():
    monthly = pd.read_csv(PROCESSED_DIR / "monthly_inflation.csv", parse_dates=["date"])
    divisions = pd.read_csv(PROCESSED_DIR / "cpi_divisions.csv", parse_dates=["date"])
    contributions = pd.read_csv(PROCESSED_DIR / "category_contributions.csv", parse_dates=["date"])
    return monthly.set_index("date"), divisions, contributions


def build_reconciliation(monthly, contributions):
    estimated = (
        contributions.groupby("date")["contribution"]
        .sum()
        .rename("estimated_headline_yoy")
        .reset_index()
    )
    reconciliation = estimated.merge(
        monthly.reset_index()[["date", "headline_yoy"]],
        on="date",
    )
    reconciliation["difference"] = (
        reconciliation["estimated_headline_yoy"] - reconciliation["headline_yoy"]
    )
    return reconciliation


def save_trend_chart(monthly):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly.index, monthly["headline_yoy"], label="Headline", linewidth=2)
    ax.plot(monthly.index, monthly["food_yoy"], label="Food", linewidth=2)
    ax.plot(monthly.index, monthly["core_yoy"], label="Core", linewidth=2)
    ax.axvline(pd.Timestamp("2024-01-01"), color="gray", linestyle="--", linewidth=1)
    ax.text(pd.Timestamp("2024-01-01"), ax.get_ylim()[1], " 2024 rebase", color="gray", va="top")
    ax.set_title("Nigeria annual inflation rate")
    ax.set_ylabel("YoY inflation (%)")
    ax.set_xlabel("Month")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "inflation_trends.png", dpi=160)
    plt.close(fig)


def save_latest_division_chart(divisions):
    snapshot_date = divisions["date"].max()
    snapshot = divisions[divisions["date"] == snapshot_date].sort_values("yoy")

    fig, ax = plt.subplots(figsize=(11, 8))
    ax.barh(snapshot["category"], snapshot["yoy"], color="#4C78A8")
    ax.set_title(f"CPI division YoY inflation - {snapshot_date:%B %Y}")
    ax.set_xlabel("YoY inflation (%)")
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "category_yoy_latest.png", dpi=160)
    plt.close(fig)


def save_key_category_chart(divisions):
    key_series = divisions[divisions["category"].isin(SELECTED_CATEGORIES)]

    fig, ax = plt.subplots(figsize=(12, 6))
    for category, group in key_series.groupby("category"):
        ax.plot(group["date"], group["yoy"], label=category, linewidth=1.8)
    ax.set_title("YoY inflation for selected CPI divisions")
    ax.set_ylabel("YoY inflation (%)")
    ax.set_xlabel("Month")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "key_category_trends.png", dpi=160)
    plt.close(fig)


def save_contribution_charts(contributions, reconciliation):
    latest_date = contributions["date"].max()
    latest = contributions[contributions["date"] == latest_date].sort_values("contribution")

    fig, ax = plt.subplots(figsize=(11, 8))
    ax.barh(latest["category"], latest["contribution"], color="#59A14F")
    ax.set_title(f"Estimated contribution to headline inflation - {latest_date:%B %Y}")
    ax.set_xlabel("Contribution (percentage points)")
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "weighted_contribution_latest.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(reconciliation["date"], reconciliation["headline_yoy"], label="Headline YoY", linewidth=2)
    ax.plot(
        reconciliation["date"],
        reconciliation["estimated_headline_yoy"],
        label="Sum of category contributions",
        linewidth=2,
    )
    ax.set_title("Contribution reconciliation")
    ax.set_ylabel("Annual inflation (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "contribution_reconciliation.png", dpi=160)
    plt.close(fig)


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    monthly, divisions, contributions = load_data()
    reconciliation = build_reconciliation(monthly, contributions)

    save_trend_chart(monthly)
    save_latest_division_chart(divisions)
    save_key_category_chart(divisions)
    save_contribution_charts(contributions, reconciliation)

    print("Mean absolute gap:", round(reconciliation["difference"].abs().mean(), 3))
    for path in sorted(FIGURES_DIR.glob("*.png")):
        print(f"Saved: {path.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
