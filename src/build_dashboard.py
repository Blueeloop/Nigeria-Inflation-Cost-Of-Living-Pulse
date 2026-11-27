from __future__ import annotations

from html import escape
from pathlib import Path
from shutil import copy2
from string import Template

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
DASHBOARD = ROOT / "dashboard"
DOCS = ROOT / "docs"

CHARTS = [
    "inflation_trends.png",
    "category_yoy_latest.png",
    "key_category_trends.png",
    "weighted_contribution_latest.png",
    "contribution_reconciliation.png",
]

STYLES = """* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Segoe UI, Arial, sans-serif;
  color: #dbe7f3;
  background: #0b1725;
}
.dashboard { max-width: 1240px; margin: 0 auto; padding: 28px 24px 40px; }
.hero {
  background: linear-gradient(135deg, #102b43, #0d2135);
  border: 1px solid #1e3a55;
  border-radius: 16px;
  padding: 28px 32px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}
.eyebrow {
  font-size: 11px;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: #9fb4c9;
  font-weight: 700;
}
.hero h1 { margin: 8px 0 7px; font-size: clamp(24px, 3vw, 34px); line-height: 1.15; color: #f4f8fc; }
.hero p { margin: 0; color: #9fb4c9; font-size: 14px; }
.period { text-align: right; min-width: 170px; }
.period span { display: block; font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: #9fb4c9; }
.period strong { display: block; margin-top: 6px; font-size: 20px; color: #f4f8fc; }
.kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin: 20px 0;
}
.kpi, .panel {
  background: #11243a;
  border: 1px solid #213b56;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, .22);
}
.panel { padding: 22px; }
.kpi .label { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: #9fb4c9; font-weight: 800; }
.kpi .value { margin-top: 8px; font-size: 30px; font-weight: 800; color: #f4f8fc; line-height: 1; }
.kpi .meta { display: block; margin-top: 8px; color: #9fb4c9; font-size: 12px; }
.panel h2 { margin: 0; font-size: 18px; color: #f4f8fc; }
.kicker { margin: 5px 0 16px; color: #9fb4c9; font-size: 12px; }
.summary { margin-bottom: 18px; border-left: 4px solid #5aa9e6; }
.summary p { margin: 10px 0 0; font-size: 14px; line-height: 1.65; color: #c6d5e4; }
.main-grid, .chart-grid { display: grid; gap: 18px; }
.main-grid { grid-template-columns: minmax(0, 1.65fr) minmax(320px, 1fr); align-items: stretch; }
.chart-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 18px; }
.chart img {
  display: block;
  width: 100%;
  max-height: 360px;
  object-fit: contain;
  background: #fff;
  border: 1px solid #2b425b;
  border-radius: 10px;
}
.primary .chart img { max-height: 430px; }
table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
th {
  text-align: left;
  font-size: 10px;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: #9fb4c9;
  padding: 0 8px 8px 0;
  border-bottom: 1px solid #2b425b;
}
td { padding: 9px 8px 9px 0; border-bottom: 1px solid #213b56; vertical-align: top; }
.num { text-align: right; white-space: nowrap; }
.strong { font-weight: 800; color: #f4f8fc; }
footer {
  margin-top: 20px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  color: #9fb4c9;
  font-size: 11px;
}
@media (max-width: 980px) {
  .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .main-grid, .chart-grid { grid-template-columns: 1fr; }
}
@media (max-width: 620px) {
  .dashboard { padding: 16px 12px 28px; }
  .hero { align-items: flex-start; flex-direction: column; padding: 22px; }
  .period { text-align: left; }
  .kpis { grid-template-columns: 1fr; }
  .panel { padding: 18px; }
}
"""


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def build_objectives_chart() -> None:
    objectives = [
        "Trend analysis",
        "Food/core comparison",
        "MoM and YoY analysis",
        "Category drivers",
        "Context and rebase review",
        "Communication",
    ]

    fig, ax = plt.subplots(figsize=(12, 4.8), dpi=160)
    fig.patch.set_facecolor("#11243a")
    ax.set_facecolor("#11243a")

    bars = ax.barh(objectives, [100] * len(objectives), color="#2f6f9f", height=0.55)
    ax.invert_yaxis()
    ax.set_yticks(range(len(objectives)))
    ax.set_xlim(0, 112)
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    ax.set_title(
        "6 of 6 objectives complete",
        color="#f4f8fc",
        fontsize=14,
        fontweight="bold",
        pad=14,
        loc="center",
    )
    ax.set_yticklabels(objectives, color="#dbe7f3", fontsize=10)

    for spine in ax.spines.values():
        spine.set_visible(False)

    for bar in bars:
        ax.text(
            101,
            bar.get_y() + bar.get_height() / 2,
            "Complete",
            va="center",
            ha="left",
            color="#f4f8fc",
            fontsize=9,
            fontweight="bold",
        )

    fig.tight_layout()
    fig.savefig(FIGURES / "objectives_achieved.png", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    DASHBOARD.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    (DASHBOARD / "dashboard.css").write_text(STYLES, encoding="utf-8")
    (DOCS / "dashboard.css").write_text(STYLES, encoding="utf-8")

    monthly = pd.read_csv(PROCESSED / "monthly_inflation.csv", parse_dates=["date"]).sort_values("date")
    contrib = pd.read_csv(PROCESSED / "category_contributions.csv", parse_dates=["date"])

    latest = monthly.iloc[-1]
    period_start = monthly["date"].iloc[0].strftime("%B %Y")
    month = latest["date"].strftime("%B %Y")
    headline = float(latest["headline_yoy"])
    mom = float(latest["headline_mom"])
    food = float(latest["food_yoy"])
    core = float(latest["core_yoy"])

    peak_row = monthly.loc[monthly["headline_yoy"].idxmax()]
    peak_month = peak_row["date"].strftime("%B %Y")
    peak_value = float(peak_row["headline_yoy"])

    latest_date = contrib["date"].max()
    latest_contrib = contrib[contrib["date"] == latest_date].copy()
    top = latest_contrib.sort_values("contribution", ascending=False).head(5)
    food_row = latest_contrib[
        latest_contrib["category"] == "Food and non-alcoholic beverages"
    ].iloc[0]
    food_contrib = float(food_row["contribution"])
    food_share = food_contrib / headline * 100 if headline else 0.0

    rows = []
    for row in top.itertuples():
        rows.append(
            "<tr><td>{name}</td><td class='num'>{yoy}%</td>"
            "<td class='num strong'>{contribution} pp</td></tr>".format(
                name=escape(row.category),
                yoy=fmt(row.yoy),
                contribution=fmt(row.contribution),
            )
        )

    summary = (
        f"Headline inflation eased to {fmt(headline)}% in {month} after peaking at "
        f"{fmt(peak_value)}% in {peak_month}. Food remained the main source of pressure, "
        f"contributing {fmt(food_contrib)} percentage points, or {fmt(food_share, 1)}% "
        f"of the headline rate."
    )

    build_objectives_chart()

    for chart in CHARTS:
        copy2(FIGURES / chart, DASHBOARD / chart)
        copy2(FIGURES / chart, DOCS / chart)

    html = Template(
        """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nigeria Inflation &amp; Cost-of-Living Pulse — Dashboard</title>
<link rel="stylesheet" href="dashboard.css">
</head>
<body>
<div class="dashboard">
  <header class="hero">
    <div>
      <div class="eyebrow">Inflation monitor</div>
      <h1>Nigeria Inflation &amp; Cost-of-Living Pulse</h1>
      <p>National CPI dashboard · $period</p>
    </div>
    <div class="period">
      <span>Latest observation</span>
      <strong>$month</strong>
    </div>
  </header>

  <section class="kpis">
    <div class="kpi">
      <div class="label">Headline inflation</div>
      <div class="value">$headline%</div>
      <span class="meta">Year-on-year</span>
    </div>
    <div class="kpi">
      <div class="label">Monthly change</div>
      <div class="value">$mom%</div>
      <span class="meta">Month-on-month</span>
    </div>
    <div class="kpi">
      <div class="label">Food inflation</div>
      <div class="value">$food%</div>
      <span class="meta">Year-on-year</span>
    </div>
    <div class="kpi">
      <div class="label">Core inflation</div>
      <div class="value">$core%</div>
      <span class="meta">Year-on-year</span>
    </div>
  </section>

  <section class="panel summary">
    <h2>Executive summary</h2>
    <p>$summary</p>
  </section>

  <div class="main-grid">
    <section class="panel primary">
      <h2>Inflation trend</h2>
      <p class="kicker">Headline, food and core inflation over the full study period</p>
      <div class="chart"><img src="inflation_trends.png" alt="Headline, food and core inflation trend"></div>
    </section>

    <section class="panel">
      <h2>Latest category drivers</h2>
      <p class="kicker">Top five contributors to headline inflation · $month</p>
      <table>
        <thead>
          <tr><th>Category</th><th class="num">Rate</th><th class="num">Impact</th></tr>
        </thead>
        <tbody>$rows</tbody>
      </table>
    </section>
  </div>

  <div class="chart-grid">
    <section class="panel">
      <h2>Latest category rates</h2>
      <p class="kicker">Year-on-year inflation by CPI division</p>
      <div class="chart"><img src="category_yoy_latest.png" alt="Latest CPI division inflation rates"></div>
    </section>

    <section class="panel">
      <h2>Selected category trends</h2>
      <p class="kicker">How major divisions changed through 2026</p>
      <div class="chart"><img src="key_category_trends.png" alt="Selected CPI division trends"></div>
    </section>

    <section class="panel">
      <h2>Latest contributions</h2>
      <p class="kicker">Estimated contribution by CPI division · $month</p>
      <div class="chart"><img src="weighted_contribution_latest.png" alt="Estimated category contributions"></div>
    </section>

    <section class="panel">
      <h2>Contribution reconciliation</h2>
      <p class="kicker">Estimated total contribution compared with headline inflation</p>
      <div class="chart"><img src="contribution_reconciliation.png" alt="Contribution reconciliation"></div>
    </section>
  </div>

  <footer>
    <span>Source: National Bureau of Statistics (NBS), Nigeria.</span>
    <span>Analysis notes and method are documented in the project README.</span>
  </footer>
</div>
</body>
</html>
"""
    ).substitute(
        period=escape(f"{period_start} – {month}"),
        month=escape(month),
        headline=fmt(headline),
        mom=fmt(mom),
        food=fmt(food),
        core=fmt(core),
        summary=escape(summary),
        rows="".join(rows),
    )

    (DASHBOARD / "index.html").write_text(html, encoding="utf-8")
    (DOCS / "dashboard.html").write_text(html, encoding="utf-8")
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print("Wrote dashboard/index.html, docs/dashboard.html and docs/index.html")


if __name__ == "__main__":
    main()
