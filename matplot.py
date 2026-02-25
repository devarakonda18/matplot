#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Title: Top 100 Global Banks – Matplotlib Project
Purpose:
    Create four visualizations using the STATELESS pyplot interface only.
    (Object-oriented approach with explicit figure and axis objects)

Visualizations:
    1. Bar Chart – Top 10 Banks by Total Assets
    2. Histogram – Distribution of Total Assets
    3. Stacked Bar Chart – Asset Composition by Top 5 Countries and Bank Type
    4. Boxplot – Statistical Dispersion of Assets
'''

# ============================================
# Import Libraries
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dpi = 300

# ============================================
# Load Dataset
# ============================================

file_path = "top100banks2017-12-31.xlsx"
df = pd.read_excel(file_path)


# ============================================
# Visualization 1: Bar Chart
# Top 10 Banks by Total Assets
# ============================================

top10 = df.sort_values(by="total_assets_us_b", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12,6))
ax.bar(range(len(top10)), top10["total_assets_us_b"])

ax.set_title("Top 10 Banks by Total Assets (2017)")
ax.set_xlabel("Bank")
ax.set_ylabel("Total Assets (USD Billions)")
ax.set_xticks(range(len(top10)))
ax.set_xticklabels(top10["bank"], rotation=90)

# Add value labels on top of bars
for i, v in enumerate(top10["total_assets_us_b"]):
    ax.text(i, v + 50, f'{v:.0f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig("viz1_top10_banks.png", dpi=dpi)
plt.show()
plt.close(fig)


# ============================================
# Visualization 2: Histogram
# Distribution of Total Assets
# ============================================

fig, ax = plt.subplots(figsize=(10,6))

# Create histogram with custom styling
n, bins, patches = ax.hist(df["total_assets_us_b"], bins=20, edgecolor='black', linewidth=1.2)

# Color the bars based on value
for i, patch in enumerate(patches):
    patch.set_facecolor(plt.cm.viridis(i/len(patches)))

ax.set_title("Distribution of Bank Total Assets")
ax.set_xlabel("Total Assets (USD Billions)")
ax.set_ylabel("Frequency")

# Add mean and median lines
mean_val = df["total_assets_us_b"].mean()
median_val = df["total_assets_us_b"].median()
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.0f}')
ax.axvline(median_val, color='blue', linestyle=':', linewidth=2, label=f'Median: {median_val:.0f}')
ax.legend()

plt.tight_layout()
plt.savefig("viz2_histogram_assets.png", dpi=dpi)
plt.show()
plt.close(fig)


# ============================================
# Visualization 3: Stacked Bar Chart
# Asset Composition by Top 5 Countries and Bank Type
# ============================================

# Create a bank type classification based on asset size
df['bank_type'] = pd.cut(df['total_assets_us_b'],
                         bins=[0, 500, 1000, 2000, 5000],
                         labels=['Small (<500B)', 'Medium (500B-1T)',
                                'Large (1T-2T)', 'Mega (>2T)'])

# Get top 5 countries by total assets
top5_countries = df.groupby("country")["total_assets_us_b"].sum().nlargest(5).index.tolist()

# Filter data for top 5 countries
df_top5 = df[df['country'].isin(top5_countries)]

# Create pivot table for stacked bar chart
pivot_data = df_top5.groupby(['country', 'bank_type']).size().unstack(fill_value=0)

# Sort countries by total banks
pivot_data['total'] = pivot_data.sum(axis=1)
pivot_data = pivot_data.sort_values('total', ascending=True).drop('total', axis=1)

fig, ax = plt.subplots(figsize=(12,8))

# Create stacked bars
bottom = np.zeros(len(pivot_data))
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

for i, col in enumerate(pivot_data.columns):
    ax.barh(pivot_data.index, pivot_data[col], left=bottom,
            label=col, color=colors[i % len(colors)], edgecolor='white', linewidth=0.5)
    bottom += pivot_data[col]

ax.set_title("Bank Type Distribution in Top 5 Countries", fontsize=16, fontweight='bold')
ax.set_xlabel("Number of Banks", fontsize=12)
ax.set_ylabel("Country", fontsize=12)

# Add value labels on bars
for i, country in enumerate(pivot_data.index):
    cum_sum = 0
    for col in pivot_data.columns:
        val = pivot_data.loc[country, col]
        if val > 0:
            ax.text(cum_sum + val/2, i, str(int(val)),
                   ha='center', va='center', fontsize=9, fontweight='bold')
        cum_sum += val

ax.legend(title='Bank Type', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig("viz3_country_composition.png", dpi=dpi, bbox_inches='tight')
plt.show()
plt.close(fig)


# ============================================
# Visualization 4: Boxplot
# Statistical Dispersion of Assets with Country Comparison
# ============================================

# Get top 5 countries with most banks for comparison
top5_by_count = df['country'].value_counts().nlargest(5).index.tolist()

# Prepare data for boxplot
boxplot_data = []
country_labels = []
for country in top5_by_count:
    country_data = df[df['country'] == country]['total_assets_us_b'].dropna()
    if len(country_data) > 0:
        boxplot_data.append(country_data)
        country_labels.append(f"{country}\n(n={len(country_data)})")

fig, ax = plt.subplots(figsize=(12,8))

# Create boxplot
bp = ax.boxplot(boxplot_data, labels=country_labels, patch_artist=True)

# Customize boxplot colors
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB366']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Add individual data points (jittered)
for i, data in enumerate(boxplot_data):
    x = np.random.normal(i+1, 0.04, size=len(data))
    ax.scatter(x, data, alpha=0.3, color='gray', s=30)

ax.set_title("Distribution of Bank Assets by Country", fontsize=16, fontweight='bold')
ax.set_ylabel("Total Assets (USD Billions)", fontsize=12)
ax.set_xlabel("Country", fontsize=12)

# Add grid for better readability
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add statistical summary as text
stats_text = "Summary Statistics:\n"
for i, data in enumerate(boxplot_data):
    stats_text += f"{country_labels[i].split('\\n')[0]}: "
    stats_text += f"Median={data.median():.0f}B, "
    stats_text += f"Mean={data.mean():.0f}B\n"

ax.text(1.02, 0.98, stats_text, transform=ax.transAxes,
        fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig("viz4_country_boxplot.png", dpi=dpi, bbox_inches='tight')
plt.show()
plt.close(fig)


print("All visualizations created using stateless pyplot interface (object-oriented approach).")
print("\nVisualization types created:")
print("1. Top 10 Banks Bar Chart (with value labels)")
print("2. Assets Distribution Histogram (with mean/median lines)")
print("3. Stacked Bar Chart - Bank Type by Country")
print("4. Comparative Boxplot by Country (with jittered data points)")
