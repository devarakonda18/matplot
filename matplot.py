# ============================================
# Top 100 Global Banks – Matplotlib Project
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------
# Load Dataset
# --------------------------------------------
file_path = "top100banks2017-12-31.xlsx"
df = pd.read_excel(file_path)

# ============================================
# Visualization 1: Bar Chart
# Top 10 Banks by Total Assets
# ============================================

top10 = df.sort_values(by="total_assets_us_b", ascending=False).head(10)

plt.bar(top10["bank"], top10["total_assets_us_b"])
plt.xticks(rotation=90)
plt.xlabel("Bank")
plt.ylabel("Total Assets (USD Billions)")
plt.title("Top 10 Banks by Total Assets (2017)")
plt.tight_layout()
plt.savefig("viz1_top10_banks.png")
plt.show()
plt.clf()


# ============================================
# Visualization 2: Histogram
# Distribution of Total Assets
# ============================================

plt.hist(df["total_assets_us_b"], bins=20)
plt.xlabel("Total Assets (USD Billions)")
plt.ylabel("Frequency")
plt.title("Distribution of Bank Total Assets")
plt.tight_layout()
plt.savefig("viz2_histogram_assets.png")
plt.show()
plt.clf()


# ============================================
# Visualization 3: Pie Chart
# Asset Share by Top 5 Countries
# ============================================

country_assets = (
    df.groupby("country")["total_assets_us_b"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

plt.pie(country_assets.values, labels=country_assets.index, autopct="%1.1f%%")
plt.title("Asset Share of Top 5 Countries")
plt.tight_layout()
plt.savefig("viz3_country_share.png")
plt.show()
plt.clf()


# ============================================
# Visualization 4: Boxplot
# Statistical Dispersion of Assets
# ============================================

plt.boxplot(df["total_assets_us_b"])
plt.ylabel("Total Assets (USD Billions)")
plt.title("Boxplot of Bank Total Assets")
plt.tight_layout()
plt.savefig("viz4_boxplot_assets.png")
plt.show()
plt.clf()


print("All visualizations created using the pyplot interface.")
