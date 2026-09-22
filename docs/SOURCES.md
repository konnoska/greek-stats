# Data Sources

This file documents exactly where every number used in this project comes from,
so each value can be traced back to and re-verified against its source.

Last verified: 2026-09-22.

---

## 1. Income distribution (the histogram) — 2025

### What it is
The quantile thresholds of **equivalised disposable income** in Greece. These
are the income levels at each percentile of the population (e.g. the 50th
percentile is the median).

### Where it comes from
- **Publisher:** Eurostat
- **Survey:** EU-SILC (Statistics on Income and Living Conditions)
- **Dataset:** `ilc_di01` — "Distribution of income by quantiles"
- **Same survey at ELSTAT:** "Income and Living Conditions (EU-SILC)", code `SFA10`

### Exact source (human page)
https://ec.europa.eu/eurostat/databrowser/view/ilc_di01

### Exact query used (API)
```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_di01
  ?format=JSON
  &geo=EL
  &freq=A
  &unit=EUR
  &statinfo=TC
  &time=2025
```

### Filters applied
| Filter  | Value  | Meaning                              |
|---------|--------|--------------------------------------|
| geo     | EL     | Greece                               |
| freq    | A      | Annual                               |
| unit    | EUR    | Euros (not PPS or national currency) |
| statinfo| TC     | Quantile *threshold* (cut-off value) |
| time    | 2025   | Income reference year 2025           |

### Values taken (saved in `data/greece_income_2025_quantiles.csv`)

| Percentile | Income (EUR/year) |
|-----------:|------------------:|
| 1          | 1,700             |
| 2          | 2,761             |
| 3          | 3,274             |
| 4          | 3,780             |
| 5          | 4,190             |
| 10         | 5,537             |
| 20         | 7,110             |
| 30         | 8,916             |
| 40         | 10,269            |
| 50         | 11,700            |
| 60         | 13,184            |
| 70         | 14,818            |
| 80         | 17,056            |
| 90         | 20,796            |
| 95         | 26,476            |
| 96         | 29,280            |
| 97         | 32,624            |
| 98         | 36,933            |
| 99         | 49,279            |

---

## 2. Mean and median income — 2025

### Where it comes from
- **Publisher:** Eurostat
- **Dataset:** `ilc_di03` — "Mean and median income by age and sex"

### Exact source (human page)
https://ec.europa.eu/eurostat/databrowser/view/ilc_di03

### Exact query used (API)
```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_di03
  ?format=JSON
  &geo=EL
  &freq=A
  &unit=EUR
  &age=TOTAL
  &sex=T
  &statinfo=MEAN_EI
  &statinfo=MED_EI
  &time=2025
```

### Values taken (overall population)

| Indicator | Value (EUR/year) | Meaning                                        |
|-----------|-----------------:|------------------------------------------------|
| MEAN_EI   | 13,381           | Mean equivalised disposable income             |
| MED_EI    | 11,700           | Median equivalised disposable income           |

> The **median (€11,700)** is confirmed by two independent sources: this
> `ilc_di03` MED_EI value and the `ilc_di01` 50th-percentile cut-off (also
> €11,700). Both agree, so this is a reliable figure.
>
> Note: the mean/median in `ilc_di02` ("Distribution of income by different
> income groups") are *sub-group* figures (income of people above/below the
> at-risk-of-poverty threshold), so they are **not** used here.

---

## 3. Salary distribution (gross earnings of employees) — 2022

Not used in the histogram, but downloaded for reference. This is the true
*gross salary* distribution.

### Where it comes from
- **Publisher:** ELSTAT (Hellenic Statistical Authority)
- **Survey:** Structure of Earnings Survey (SES)
- **ELSTAT publication:** "Distribution of earnings (Structure) NACE Rev.2", code `SJO47`, year 2022

### Exact source (human page)
https://www.statistics.gr/en/statistics/-/publication/SJO47/2022

### Files downloaded (into `data/raw/`)
| Local file | ELSTAT table | Contents |
|-----------|--------------|----------|
| `table1_sector_size.xls` | Table 1 | Employees & gross earnings by sector & enterprise size |
| `table2_earnings_status.xls` | Table 2 | Mean/median, D1 & D9 deciles by sector |
| `table3_occupation.xls` | Table 3 | Employees & earnings by occupation (ISCO-08) |
| `table4_demographics.xls` | Table 4 | Earnings by age / education |
| `table4b_demographics.xls` | Table 4B | Same, 2014–2022 |
| `table5_gpg.xls` | Table 5 | Gender pay gap |
| `table5b_gpg.xls` | Table 5B | Gender pay gap, 2014–2022 |
| `methodology_ses.pdf` | Methodology | Survey methodology |
| `pressrelease_ses.pdf` | Press release | 2022 SES press release |

### Cross-check via Eurostat (`earn_ses_annual`)
The salary quantiles were also extracted cleanly from Eurostat's version of the
same survey:

- **Dataset:** `earn_ses_annual` — "Structure of earnings survey — annual earnings"
- **Human page:** https://ec.europa.eu/eurostat/databrowser/view/earn_ses_annual
- **Query:** `geo=EL`, `freq=A`, `nace_r2=B-S_X_O`, `isco08=TOTAL`, `worktime=TOTAL`,
  `age=TOTAL`, `sex=T`, `time=2022`, indicators `MEAN_E_EUR`, `MED_E_EUR`, `D1_E_EUR`, `D9_E_EUR`.

### Values taken (Greece 2022, all employees, gross annual earnings)

| Indicator | Total | Male | Female |
|-----------|------:|-----:|-------:|
| Mean      | 19,703 | 21,947 | 17,360 |
| Median    | 15,924 | 17,264 | 14,735 |
| D1 (10th) | 4,579  | 4,770  | 4,413  |
| D9 (90th) | 35,297 | 40,394 | 29,672 |

---

## 4. Household net wealth (2023) — held for later use

Not yet used in the calculator, but downloaded and saved for a future
"net worth" tool.

### Where it comes from
- **Publisher:** ECB (Eurosystem Household Finance and Consumption Survey)
- **National authority for Greece:** Bank of Greece
- **Survey:** HFCS, 2023 wave (5th wave)
- **Table:** J3 "Net wealth per household – distribution"
- **File:** `HFCS_Statistical_Tables_Wave_2023_June_2026.xlsx` (published June 2026)

### Exact source
https://www.ecb.europa.eu/home/pdf/research/hfcn/HFCS_Statistical_Tables_Wave_2023_June_2026.zip

### Values taken (Greece 2023, household net wealth, EUR)

| Percentile | Net wealth (EUR) |
|-----------:|-----------------:|
| P10        | 4,300            |
| P20        | 16,800           |
| P30        | 49,100           |
| P40        | 75,800           |
| P50 (median)| 103,200          |
| P60        | 138,300          |
| P70        | 181,600          |
| P80        | 246,700          |
| P90        | 376,200          |
| Mean       | 170,200          |

Saved in `data/greece_networth_2023_quantiles.csv`.

> Note: household-level (not equivalised, not per person); the published
> distribution stops at P90 (no P95/P99).

---

## 5. Household financial assets (2023) — used by the "stash" calculator

Used by `calculator/financial-assets.html`.

### What it measures
Household **financial assets** (savings & investments): bank deposits, mutual
funds, bonds, publicly-traded shares, managed accounts, private pension plans,
cash-value life insurance, money lent to others, precious metals and other
financial assets.

It **excludes** "real assets": the main residence (house), other real estate,
vehicles, valuables, and actively-run self-employment businesses.

### Where it comes from
- **Publisher:** ECB (HFCS), **national authority:** Bank of Greece
- **Survey:** HFCS, 2023 wave (5th wave)
- **Table:** C3 "Total financial assets – distribution"
- **File:** `HFCS_Statistical_Tables_Wave_2023_June_2026.xlsx`

### Exact source
https://www.ecb.europa.eu/home/pdf/research/hfcn/HFCS_Statistical_Tables_Wave_2023_June_2026.zip

### Values taken (Greece 2023, household financial assets, EUR)

| Percentile | Financial assets (EUR) |
|-----------:|-----------------------:|
| P10        | 200                    |
| P20        | 500                    |
| P30        | 1,000                  |
| P40        | 1,500                  |
| P50 (median)| 3,000                 |
| P60        | 5,000                  |
| P70        | 8,400                  |
| P80        | 15,000                 |
| P90        | 31,900                 |
| Mean       | 14,200                 |

Saved in `data/greece_financial_assets_2023_quantiles.csv`.

> Note: per household (not size-adjusted) and conditional on households holding
> at least some financial asset (≈99% of households). The distribution **stops
> at P90** — the ECB does not publish P95/P99 (thin top tail, sampling
> uncertainty, and confidentiality).

---

## Quick reference — value → source

| Value used in project | Comes from | File |
|-----------------------|------------|------|
| 19 quantile thresholds (income) | Eurostat `ilc_di01` (2025) | `data/greece_income_2025_quantiles.csv` |
| **Median income €11,700** | Eurostat `ilc_di03` & `ilc_di01` (2025, both agree) | `README.md` |
| Mean income €13,381 (reference only) | Eurostat `ilc_di03` (2025) | `README.md` |
| Salary **median** €15,924 (annual, 2022) | Eurostat `earn_ses_annual` / ELSTAT `SJO47` | `README.md`, `data/raw/table2_earnings_status.xls` |
| Net worth percentiles (P10–P90) | ECB HFCS 2023 (Bank of Greece) | `data/greece_networth_2023_quantiles.csv` |
| Financial assets percentiles (P10–P90) | ECB HFCS 2023 (Bank of Greece) | `data/greece_financial_assets_2023_quantiles.csv` |

---

## Definitions (for interpreting the numbers)

- **Equivalised disposable income** — household disposable income (all income
  minus taxes and social contributions, plus benefits) divided by a household-
  size weight (modified-OECD scale: first adult 1.0, each extra adult 0.5,
  each child <14 0.3). Expressed per "equivalent adult".
- **Gross annual earnings (SES)** — an employee's gross earnings from the
  employer over the year, before tax and social contributions.
