# ============================================
# Top 100 Global Banks – Matplotlib Project
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------
# 1. Load Dataset
# --------------------------------------------
file_path = "top100banks2017-12-31.xlsx"
df = pd.read_excel(file_path)

# --------------------------------------------
# Visualization 1: Horizontal Bar Chart
# Top 15 Banks by Total Assets
# --------------------------------------------
top15 = df.sort_values(by="total_assets_us_b", ascending=False).head(15)

plt.figure()
plt.barh(top15["bank"], top15["total_assets_us_b"])
plt.xlabel("Total Assets (USD Billions)")
plt.title("Top 15 Global Banks by Total Assets (2017)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("viz1_top15_banks.png")
plt.show()


# --------------------------------------------
# Visualization 2: Histogram
# Distribution of Assets
# --------------------------------------------
plt.figure()
plt.hist(df["total_assets_us_b"], bins=20)
plt.xlabel("Total Assets (USD Billions)")
plt.ylabel("Number of Banks")
plt.title("Distribution of Total Assets Across Top 100 Banks")
plt.tight_layout()
plt.savefig("viz2_asset_distribution.png")
plt.show()


# --------------------------------------------
# Visualization 3: Pie Chart
# Top 5 Countries by Asset Share
# --------------------------------------------
country_assets = df.groupby("country")["total_assets_us_b"].sum().sort_values(ascending=False)
top5 = country_assets.head(5)

plt.figure()
plt.pie(top5.values, labels=top5.index, autopct='%1.1f%%')
plt.title("Asset Share of Top 5 Countries")
plt.tight_layout()
plt.savefig("viz3_country_share.png")
plt.show()


# --------------------------------------------
# Visualization 4: Boxplot
# Asset Dispersion & Outliers
# --------------------------------------------
plt.figure()
plt.boxplot(df["total_assets_us_b"])
plt.ylabel("Total Assets (USD Billions)")
plt.title("Boxplot of Bank Total Assets")
plt.tight_layout()
plt.savefig("viz4_boxplot_assets.png")
plt.show()

print("All visualizations displayed and saved successfully.")
