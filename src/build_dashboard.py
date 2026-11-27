from __future__ import annotations

from html import escape
from pathlib import Path
from shutil import copy2
from string import Template

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
DOCS = ROOT / "docs"

CHARTS = [
    "inflation_trends.png",
    "category_yoy_latest.png",
    "key_category_trends.png",
    "weighted_contribution_latest.png",
    "contribution_reconciliation.png",
]


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}"


def main() -> None:
    DOCS.mkdir(exist_ok=True)

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
    food_gap = float((monthly["food_yoy"] - monthly["headline_yoy"]).mean())
    core_gap = float((monthly["core_yoy"] - monthly["headline_yoy"]).mean())

    latest_date = contrib["date"].max()
    latest_contrib = contrib[contrib["date"] == latest_date].copy()
    top = latest_contrib.sort_values("contribution", ascending=False).head(5)
    top_rate = latest_contrib.sort_values("yoy", ascending=False).iloc[0]
    food_row = latest_contrib[
        latest_contrib["category"] == "Food and non-alcoholic beverages"
    ].iloc[0]
    food_contrib = float(food_row["contribution"])
    food_share = food_contrib / headline * 100 if headline else 0.0

    first_date = contrib["date"].min()
    first_contrib = contrib[contrib["date"] == first_date].set_index("category")["contribution"]
    final_contrib = latest_contrib.set_index("category")["contribution"]
    changes = (final_contrib - first_contrib).dropna().sort_values()
    rise_category = changes.index[-1]
    rise_value = float(changes.iloc[-1])
    fall_category = changes.index[0]
    fall_value = abs(float(changes.iloc[0]))

    monthly_indexed = monthly.set_index("date")
    contribution_totals = contrib.groupby("date")["contribution"].sum()
    reconciliation_gap = float(
        (contribution_totals - monthly_indexed["headline_yoy"]).abs().dropna().mean()
    )

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
    trend_note = (
        f"Food averaged {fmt(food_gap)} percentage points above headline across the period, "
        f"while core averaged {fmt(abs(core_gap))} percentage points below it. "
        f"The latest headline rate was {fmt(headline)}%."
    )
    rates_note = (
        f"The highest year-on-year division rate in {month} was {top_rate['category']} at "
        f"{fmt(float(top_rate['yoy']))}%. Food and non-alcoholic beverages recorded "
        f"{fmt(float(food_row['yoy']))}%."
    )
    drivers_note = (
        "Contribution combines each division's inflation rate with its CPI basket weight, "
        "so large-weight categories can matter more than high-rate but smaller categories."
    )
    selected_trends_note = (
        f"Between {first_date.strftime('%B %Y')} and {month}, {rise_category} recorded the "
        f"largest increase in estimated contribution ({fmt(rise_value)} percentage points), "
        f"while {fall_category} recorded the largest decline ({fmt(fall_value)} percentage points)."
    )
    contributions_note = (
        f"Food and non-alcoholic beverages contributed {fmt(food_contrib)} percentage points "
        f"in {month}, or {fmt(food_share, 1)}% of the headline rate."
    )
    reconciliation_note = (
        "The weighted category contributions track headline inflation closely, with an "
        f"average absolute gap of {fmt(reconciliation_gap)} percentage points."
    )

    for chart in CHARTS:
        copy2(FIGURES / chart, DOCS / chart)

    html = Template(
        """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nigeria Inflation &amp; Cost-of-Living Pulse — Dashboard</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Segoe UI, Arial, sans-serif;
  color: #17324d;
  background: #f4f7fb;
}
.dashboard { max-width: 1240px; margin: 0 auto; padding: 28px 24px 40px; }
.hero {
  background: #12324f;
  color: #fff;
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
  color: #a8c4dc;
  font-weight: 700;
}
.hero h1 { margin: 8px 0 7px; font-size: clamp(24px, 3vw, 34px); line-height: 1.15; }
.hero p { margin: 0; color: #c7d8e8; font-size: 14px; }
.period { text-align: right; min-width: 170px; }
.period span { display: block; font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: #a8c4dc; }
.period strong { display: block; margin-top: 6px; font-size: 20px; }
.kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin: 20px 0;
}
.kpi {
  background: #fff;
  border: 1px solid #dbe5ef;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 8px 22px rgba(18, 50, 79, .06);
}
.kpi .label { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: #678096; font-weight: 800; }
.kpi .value { margin-top: 8px; font-size: 30px; font-weight: 800; color: #12324f; line-height: 1; }
.kpi .meta { display: block; margin-top: 8px; color: #71879c; font-size: 12px; }
.panel {
  background: #fff;
  border: 1px solid #dbe5ef;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 8px 22px rgba(18, 50, 79, .05);
}
.panel h2 { margin: 0; font-size: 18px; color: #12324f; }
.kicker { margin: 5px 0 16px; color: #71879c; font-size: 12px; }
.summary { margin-bottom: 18px; border-left: 4px solid #2f6f9f; }
.summary p { margin: 10px 0 0; font-size: 14px; line-height: 1.65; color: #405970; }
.main-grid, .chart-grid { display: grid; gap: 18px; }
.main-grid { grid-template-columns: minmax(0, 1.65fr) minmax(320px, 1fr); align-items: stretch; }
.chart-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 18px; }
.chart img {
  display: block;
  width: 100%;
  max-height: 360px;
  object-fit: contain;
  background: #fff;
  border: 1px solid #edf1f6;
  border-radius: 10px;
}
.primary .chart img { max-height: 430px; }
.writeup {
  margin-top: 16px;
  padding: 13px 15px;
  border-left: 3px solid #2f6f9f;
  background: #f6f9fc;
  color: #405970;
  font-size: 12.5px;
  line-height: 1.6;
  border-radius: 0 8px 8px 0;
}
.writeup strong { color: #12324f; }
table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
th {
  text-align: left;
  font-size: 10px;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: #71879c;
  padding: 0 8px 8px 0;
  border-bottom: 1px solid #dbe5ef;
}
td { padding: 9px 8px 9px 0; border-bottom: 1px solid #edf1f6; vertical-align: top; }
.num { text-align: right; white-space: nowrap; }
.strong { font-weight: 800; color: #12324f; }
footer {
  margin-top: 20px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  color: #71879c;
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
</style>
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
      <div class="writeup"><strong>Reading note.</strong> $trend_note</div>
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
      <div class="writeup"><strong>Reading note.</strong> $drivers_note</div>
    </section>
  </div>

  <div class="chart-grid">
    <section class="panel">
      <h2>Latest category rates</h2>
      <p class="kicker">Year-on-year inflation by CPI division</p>
      <div class="chart"><img src="category_yoy_latest.png" alt="Latest CPI division inflation rates"></div>
      <div class="writeup"><strong>Reading note.</strong> $rates_note</div>
    </section>

    <section class="panel">
      <h2>Selected category trends</h2>
      <p class="kicker">How major divisions changed through 2026</p>
      <div class="chart"><img src="key_category_trends.png" alt="Selected CPI division trends"></div>
      <div class="writeup"><strong>Reading note.</strong> $selected_trends_note</div>
    </section>

    <section class="panel">
      <h2>Latest contributions</h2>
      <p class="kicker">Estimated contribution by CPI division · $month</p>
      <div class="chart"><img src="weighted_contribution_latest.png" alt="Estimated category contributions"></div>
      <div class="writeup"><strong>Reading note.</strong> $contributions_note</div>
    </section>

    <section class="panel">
      <h2>Contribution reconciliation</h2>
      <p class="kicker">Estimated total contribution compared with headline inflation</p>
      <div class="chart"><img src="contribution_reconciliation.png" alt="Contribution reconciliation"></div>
      <div class="writeup"><strong>Reading note.</strong> $reconciliation_note</div>
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
        trend_note=escape(trend_note),
        drivers_note=escape(drivers_note),
        rows="".join(rows),
        rates_note=escape(rates_note),
        selected_trends_note=escape(selected_trends_note),
        contributions_note=escape(contributions_note),
        reconciliation_note=escape(reconciliation_note),
    )

    (DOCS / "dashboard.html").write_text(html, encoding="utf-8")
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print("Wrote docs/dashboard.html and docs/index.html")


if __name__ == "__main__":
    main()
