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

    monthly = pd.read_csv(PROCESSED / "monthly_inflation.csv", parse_dates=["date"])
    contrib = pd.read_csv(PROCESSED / "category_contributions.csv", parse_dates=["date"])

    latest = monthly.sort_values("date").iloc[-1]
    month = latest["date"].strftime("%B %Y")
    headline = float(latest["headline_yoy"])
    mom = float(latest["headline_mom"])
    food = float(latest["food_yoy"])
    core = float(latest["core_yoy"])

    latest_date = contrib["date"].max()
    top = (
        contrib[contrib["date"] == latest_date]
        .sort_values("contribution", ascending=False)
        .head(5)
    )

    rows = []
    for row in top.itertuples():
        rows.append(
            "<tr><td>{name}</td><td class='num'>{yoy}</td>"
            "<td class='num strong'>{contribution}</td></tr>".format(
                name=escape(row.category),
                yoy=fmt(row.yoy),
                contribution=fmt(row.contribution),
            )
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
  color: #172b45;
  background: linear-gradient(135deg, #eaf2ff, #f2ecff 50%, #e8f8f4);
}
.dashboard { max-width: 1200px; margin: 0 auto; padding: 24px; }
.card {
  background: rgba(255,255,255,.82);
  border: 1px solid rgba(255,255,255,.95);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 12px 30px rgba(40,70,110,.12);
  margin-bottom: 16px;
}
.header { display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
h1 { margin: 0; font-size: 26px; }
.subtitle { margin-top: 6px; color: #61758d; }
.pill { padding: 8px 14px; border-radius: 999px; background: white; font-weight: 700; }
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi .label { font-size: 11px; text-transform: uppercase; color: #6c7f94; font-weight: 800; }
.kpi .value { font-size: 28px; font-weight: 800; margin-top: 5px; }
.kpi .sub { font-size: 11px; color: #71849a; margin-top: 5px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
h2 { margin: 0 0 12px; font-size: 17px; }
img { width: 100%; height: auto; border-radius: 12px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; font-size: 11px; text-transform: uppercase; color: #6c7f94; }
td { padding: 8px 4px; border-bottom: 1px solid #dfe8f2; }
.num { text-align: right; white-space: nowrap; }
.strong { font-weight: 800; color: #123f61; }
.note { font-size: 13px; color: #52677f; line-height: 1.5; }
@media (max-width: 800px) {
  .kpis, .grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div class="dashboard">
  <header class="card header">
    <div>
      <h1>Nigeria Inflation &amp; Cost-of-Living Pulse</h1>
      <div class="subtitle">Static dashboard built from cleaned NBS CPI data</div>
    </div>
    <div class="pill">Latest month · $month</div>
  </header>

  <section class="kpis">
    <div class="card kpi">
      <div class="label">Headline YoY</div>
      <div class="value">$headline%</div>
      <div class="sub">All-items inflation</div>
    </div>
    <div class="card kpi">
      <div class="label">Headline MoM</div>
      <div class="value">$mom%</div>
      <div class="sub">Current monthly pressure</div>
    </div>
    <div class="card kpi">
      <div class="label">Food YoY</div>
      <div class="value">$food%</div>
      <div class="sub">NBS Food index</div>
    </div>
    <div class="card kpi">
      <div class="label">Core YoY</div>
      <div class="value">$core%</div>
      <div class="sub">Less farm produce and energy</div>
    </div>
  </section>

  <section class="card">
    <h2>Latest estimated category contributions</h2>
    <table>
      <thead>
        <tr><th>Category</th><th class="num">YoY</th><th class="num">Contribution</th></tr>
      </thead>
      <tbody>$rows</tbody>
    </table>
    <p class="note">Contribution combines the category inflation rate with its CPI basket weight.</p>
  </section>

  <section class="grid">
    <div class="card"><h2>Inflation trend</h2><img src="inflation_trends.png" alt="Inflation trend"></div>
    <div class="card"><h2>Latest category rates</h2><img src="category_yoy_latest.png" alt="Latest category rates"></div>
    <div class="card"><h2>Selected category trends</h2><img src="key_category_trends.png" alt="Selected category trends"></div>
    <div class="card"><h2>Latest contributions</h2><img src="weighted_contribution_latest.png" alt="Latest contributions"></div>
    <div class="card"><h2>Contribution reconciliation</h2><img src="contribution_reconciliation.png" alt="Contribution reconciliation"></div>
  </section>
</div>
</body>
</html>
"""
    ).substitute(
        month=escape(month),
        headline=fmt(headline),
        mom=fmt(mom),
        food=fmt(food),
        core=fmt(core),
        rows="".join(rows),
    )

    (DOCS / "dashboard.html").write_text(html, encoding="utf-8")
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print("Wrote docs/dashboard.html and docs/index.html")


if __name__ == "__main__":
    main()
