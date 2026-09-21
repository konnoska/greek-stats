import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt


def load_data(csv_path, income_column):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        sys.stderr.write(f"Error reading CSV: {e}\n")
        sys.exit(1)
    if income_column not in df.columns:
        sys.stderr.write(f"Column '{income_column}' not found in CSV. Available columns: {list(df.columns)}\n")
        sys.exit(1)
    # Drop missing or non‑numeric values
    incomes = pd.to_numeric(df[income_column], errors='coerce').dropna()
    return incomes


def plot_histogram(incomes, bins, output_path):
    plt.figure(figsize=(10, 6))
    plt.hist(incomes, bins=bins, edgecolor='black')
    plt.title('Income Distribution of Greeks')
    plt.xlabel('Annual Net Income (€)')
    plt.ylabel('Number of Households')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Histogram saved to {output_path}")


def cumulative_percentages(incomes, thresholds):
    total = len(incomes)
    results = {}
    for th in thresholds:
        count = (incomes <= th).sum()
        results[th] = 100 * count / total
    return results


def main():
    parser = argparse.ArgumentParser(description='Generate a histogram of Greek income distribution from ELSTAT data.')
    parser.add_argument('csv', help='Path to the CSV file containing income data')
    parser.add_argument('--column', default='income', help='Name of the column that holds annual net income (default: income)')
    parser.add_argument('--bins', type=int, nargs='*', default=[0, 10000, 20000, 30000, 40000, 50000, 75000, 100000, 150000, 200000, 300000],
                        help='Bin edges for the histogram (default: typical income ranges)')
    parser.add_argument('--output', default='income_histogram.png', help='Path to save the histogram image')
    parser.add_argument('--thresholds', type=int, nargs='*', default=[20000, 30000, 40000, 50000],
                        help='Income thresholds (in €) for cumulative percentage output')
    args = parser.parse_args()

    incomes = load_data(args.csv, args.column)
    plot_histogram(incomes, bins=args.bins, output_path=args.output)

    cum_perc = cumulative_percentages(incomes, args.thresholds)
    print('\nCumulative percentages:')
    for th, perc in cum_perc.items():
        print(f"- {perc:.1f}% of households earn ≤ €{th:,}")

if __name__ == '__main__':
    main()
