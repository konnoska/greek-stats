#!/usr/bin/env python3
"""
Income distribution histogram for Greece.

Builds a histogram and cumulative-distribution curve for Greek equivalised
disposable income from officially published quantile thresholds (Eurostat
EU-SILC, dataset ilc_di01 — the same survey ELSTAT releases as "Income and
Living Conditions", SFA10).

Source data: data/greece_income_2025_quantiles.csv
  - "percentile": share of the population with income at or below this level
  - "income_eur": equivalised disposable income (EUR) at that percentile

Note on the measure: equivalised disposable income is *household* disposable
income adjusted for household size (modified-OECD scale), expressed per adult
equivalent. It is not gross individual salary.

Usage:
  python3 income_histogram.py [--bin-width 2000] [--max-income 60000]
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Repository root (parent of the scripts/ directory), so this script works
# regardless of the current working directory.
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"


def load_quantiles(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        sys.stderr.write(f"Error reading CSV: {e}\n")
        sys.exit(1)
    df = df.dropna()
    if df.empty:
        sys.stderr.write("No valid rows in CSV.\n")
        sys.exit(1)
    # sort by percentile, ensure monotone income
    df = df.sort_values("percentile")
    pct = df["percentile"].to_numpy(dtype=float)
    inc = df["income_eur"].to_numpy(dtype=float)
    return pct, inc


def cdf_at(income, pct, inc):
    """Fraction (0..100) of the population at or below `income`.

    Interpolates linearly in log-income space over the published quantile
    points, which is monotone by construction.
    """
    log_inc = np.log(inc)
    log_query = np.log(np.clip(income, inc.min(), inc.max()))
    return np.interp(log_query, log_inc, pct)


def build_histogram(pct, inc, bin_width, max_income):
    """Return (bin_centers, bin_shares) for equal-width euro bins."""
    edges = np.arange(0.0, max_income + bin_width, bin_width)
    centers = (edges[:-1] + edges[1:]) / 2.0
    f_lower = cdf_at(edges[:-1], pct, inc)
    f_upper = cdf_at(edges[1:], pct, inc)
    shares = np.clip(f_upper - f_lower, 0.0, None)  # % of population per bin
    return centers, shares, edges


def plot_histogram(centers, shares, bin_width, median, output_path):
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(centers, shares, width=bin_width * 0.92, color="#2a6f97",
           edgecolor="white", linewidth=0.4)
    ax.axvline(median, color="#c4453c", lw=2.2, ls="--",
               label=f"Median: €{median:,.0f}/year")
    ax.set_title("Distribution of equivalised disposable income in Greece, 2025",
                 fontsize=13, pad=12)
    ax.set_xlabel("Equivalised disposable income (EUR / year)")
    ax.set_ylabel("Share of population (%)")
    ax.grid(axis="y", alpha=0.35)
    ax.legend(loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=140)
    plt.close(fig)
    print(f"Histogram saved to {output_path}")


def plot_cdf(pct, inc, median, output_path):
    # smooth CDF curve by evaluating on a fine grid
    grid = np.linspace(0, 60000, 601)
    f = cdf_at(grid, pct, inc)
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(grid, f, color="#c4453c", lw=2.2)
    ax.scatter(inc, pct, color="#c4453c", s=30, zorder=5,
               label="Published quantile points")
    # annotate the median (50th percentile)
    ax.axvline(median, color="#2a6f97", lw=1.4, ls=":")
    ax.axhline(50, color="#2a6f97", lw=1.4, ls=":")
    ax.annotate(f"Median: €{median:,.0f}/year → 50%",
                xy=(median, 50), xytext=(median + 7000, 40),
                fontsize=10, color="#2a6f97", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#2a6f97"))
    ax.set_title("Cumulative distribution of equivalised disposable income, "
                 "Greece 2025", fontsize=13, pad=12)
    ax.set_xlabel("Equivalised disposable income (EUR / year)")
    ax.set_ylabel("Share of population at or below (%)")
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.35)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=140)
    plt.close(fig)
    print(f"Cumulative distribution saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?",
                        default=str(DATA_DIR / "greece_income_2025_quantiles.csv"),
                        help="Path to quantile CSV (percentile,income_eur)")
    parser.add_argument("--bin-width", type=int, default=2000,
                        help="Histogram bin width in EUR (default: 2000)")
    parser.add_argument("--max-income", type=int, default=60000,
                        help="Upper edge of the histogram in EUR (default: 60000)")
    parser.add_argument("--thresholds", type=int, nargs="*",
                        default=[5000, 10000, 11700, 15000, 20000, 30000, 50000],
                        help="Income thresholds (EUR) for cumulative % output")
    parser.add_argument("--output-hist", default=str(OUTPUT_DIR / "income_histogram.png"))
    parser.add_argument("--output-cdf", default=str(OUTPUT_DIR / "income_cdf.png"))
    args = parser.parse_args()

    pct, inc = load_quantiles(args.csv)

    def ordinal(n):
        n = int(n)
        return ("%d%s" % (n, "th" if 11 <= n % 100 <= 13
                          else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")))

    print("\nPublished quantiles (equivalised disposable income, EUR, 2025):")
    for p, x in zip(pct, inc):
        print(f"  {ordinal(p):>5} percentile -> €{x:,.0f}")

    print("\nCumulative shares at selected thresholds:")
    for th in args.thresholds:
        f = cdf_at(th, pct, inc)
        print(f"  {f:5.1f}% of the population at or below €{th:,} / year")

    # headline facts
    median = inc[np.searchsorted(pct, 50)]
    print(f"\nMedian (50th percentile): €{median:,.0f}/year")

    centers, shares, edges = build_histogram(pct, inc, args.bin_width,
                                             args.max_income)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_histogram(centers, shares, args.bin_width, median, args.output_hist)
    plot_cdf(pct, inc, median, args.output_cdf)


if __name__ == "__main__":
    main()
