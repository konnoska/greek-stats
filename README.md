# Greek income / salary statistics

Build a histogram and cumulative-distribution view of Greek income from
official ELSTAT / Eurostat data, plus an interactive "what's my percentile"
web page (income, and household financial assets).

## Interactive percentile calculators

Static pages (no server, no dependencies):

- **`index.html`** — landing page with two buttons:
  - "How rich am I, Greek-wise? 🇬🇷" → `calculator/` (household income)
  - "How big is my stash, Greek-wise? 💰" → `calculator/financial-assets.html`
    (household savings & investments)
- **`calculator/index.html`** — the income calculator. A visitor enters their
  **household's net disposable income** (monthly or yearly) and **household
  size** (adults + children), clicks "Show my result", and sees what percentile
  they fall in for Greek income (2025), with a distribution chart marker.
- **`calculator/financial-assets.html`** — the savings & investments calculator.
  A visitor enters their **household's total financial assets** (savings,
  shares, funds, pensions — *not* the house), and sees their percentile for
  Greek household financial assets (2023, ECB HFCS).

Because the 2025 income distribution measures *equivalised* household income
(EU-SILC), the income calculator asks for household income and size rather than
individual gross salary. A single person just enters their own net salary and
leaves size at "1 adult".

To try it locally:

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

To publish on GitHub Pages: push this repository to GitHub, then enable
**Settings → Pages → Deploy from a branch → main / root**. `index.html` will be
served at `https://<user>.github.io/<repo>/`.

## What this produces

`scripts/income_histogram.py` reads published quantile thresholds and outputs
(to `output/`):

- `income_histogram.png` — histogram of the income distribution (share of the
  population in each income band).
- `income_cdf.png` — cumulative distribution ("X% of the population earns at
  or below €Y").
- A printed table of cumulative shares at key thresholds (e.g. €5k, €10k,
  €11.7k, €15k, €20k, €30k, €50k).

## Data source

The quantile thresholds come from **Eurostat EU-SILC** dataset
[`ilc_di01`](https://ec.europa.eu/eurostat/databrowser/view/ilc_di01) — the
same survey that ELSTAT publishes as *"Income and Living Conditions"*
(SFA10). Reference year **2025** (the latest available).

Data is cached in `data/greece_income_2025_quantiles.csv`:

| column       | meaning                                                        |
|--------------|----------------------------------------------------------------|
| `percentile` | share of the population at or below this level                 |
| `income_eur` | equivalised disposable income (EUR/year) at that percentile    |

## Important caveat: "salary" vs "income"

The **Structure of Earnings Survey (SES)** — the true *salary* distribution —
is conducted every four years (2002, 2006, 2010, 2014, 2018, **2022**, next
2026). There is no 2025 salary-distribution data, and even the SES only
publishes the mean, median, 1st and 9th deciles openly (full microdata
requires a request).

The only distribution published **annually up to 2025** is the **EU-SILC
household income** distribution, so that is what this project uses. The
measure is *equivalised disposable household income* (household disposable
income adjusted for household size, per adult-equivalent) — **not gross
individual salary**.

## Key results (Greece, 2025, equivalised disposable income)

| Statistic                     | Value / year |
|-------------------------------|--------------|
| 10th percentile               | €5,537       |
| **Median (50th percentile)**  | **€11,700**  |
| 90th percentile               | €20,796      |
| 99th percentile               | €49,279      |
| Mean (for reference only)     | €13,381      |

So: **50% of the population lives on ≤ €11,700/year**, and roughly **99% live
on ≤ €50,000/year**.

The **median is €11,700/year** (verified against two independent Eurostat
sources: `ilc_di01` 50th-percentile cut-off and `ilc_di03` MED_EI, both
returning the same value).

## Salary median (different measure, older data)

For *gross salary* (the SES survey), the **median** values are:

| Measure                                | Median (2022) |
|----------------------------------------|---------------|
| Gross annual earnings (all employees)  | €15,924       |
| Gross annual earnings — men            | €17,264       |
| Gross annual earnings — women          | €14,735       |
| Gross monthly earnings (all employees) | €1,146        |

(Source: Eurostat `earn_ses_annual` / `earn_ses_monthly`, ELSTAT `SJO47`.)

## Setup and run

```bash
python3 -m pip install --user -r requirements.txt
python3 scripts/income_histogram.py
```

Options: `--bin-width`, `--max-income`, `--thresholds`, `--output-hist`,
`--output-cdf` (see `--help`). The script resolves paths relative to the repo
root, so it can be run from anywhere.

`scripts/income_distribution.py` is a separate helper for plotting a histogram
from a CSV of *individual* incomes (e.g. if microdata is ever obtained).

## Repository layout

```
index.html                      landing page (buttons → calculators)
calculator/index.html           income percentile calculator
calculator/financial-assets.html  savings & investments calculator
scripts/                        Python: income_histogram.py, income_distribution.py
data/greece_income_2025_quantiles.csv      2025 income quantiles
data/greece_financial_assets_2023_quantiles.csv  2023 financial-assets quantiles
data/greece_networth_2023_quantiles.csv    2023 net-worth quantiles (unused)
data/raw/                       raw ELSTAT SES 2022 downloads (.xls, .pdf)
output/                         generated charts (.png)
docs/SOURCES.md                 data provenance (what came from where)
```
