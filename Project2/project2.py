import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("nypd_arrests_historic-copy.csv")
pd.set_option("display.max_columns", 50)

# Cleaning the dataset (changing the dates in the dataframe from string to dates)
df["ARREST_DATE"] = pd.to_datetime(df["ARREST_DATE"], errors="coerce")

df["AGE_GROUP"] = df["AGE_GROUP"].replace(
        {"UNKNOWN": pd.NA, "Unknown": pd.NA, "": pd.NA}
    )

needed_cols = ["ARREST_DATE", "ARREST_BORO", "OFNS_DESC"]
df_clean = df.dropna(subset=needed_cols)

# Extract Year from the datetime
df_clean = df[df["ARREST_DATE"].notna()].copy()
df_clean["ARREST_YEAR"] = df_clean["ARREST_DATE"].dt.year

df_clean.groupby("ARREST_YEAR").size()

# To see Assaults Per Year, first filter to assaults only
assault_df = df_clean[df_clean["OFNS_DESC"].str.contains("ASSAULT", case=False, na=False)]

# Splitting Manhattan from other boroughs
manhattan_code = "M"

manhattan_assaults = assault_df[assault_df["ARREST_BORO"] == manhattan_code]
other_boros_assaults = assault_df[assault_df["ARREST_BORO"] != manhattan_code]

# Total count of assaults in Manhattan vs. other boroughs
total_manhattan = len(manhattan_assaults)
total_others = len(other_boros_assaults)

# Number of assaults per year in Manhattan vs. other boroughs
yearly_manhattan = manhattan_assaults.groupby("ARREST_YEAR").size()
yearly_others = other_boros_assaults.groupby("ARREST_YEAR").size()

# Prepping for visualization: combining and sorting all years
all_years = sorted(set(yearly_manhattan.index).union(set(yearly_others.index)))

# Aligning both series to have the same index (all years), fill missing with 0
manhattan_counts_aligned = [yearly_manhattan.get(y, 0) for y in all_years]
others_counts_aligned = [yearly_others.get(y, 0) for y in all_years]

# Bar Chart
plt.figure(figsize=(10, 5))
x = all_years  # x-axis values (years)
width = 0.35  # width of each bar
# Manhattan bars shifted to the left
plt.bar([i - width/2 for i in x],
        manhattan_counts_aligned,
        width=width,
        label="Manhattan (M)")

# Other boroughs bars shifted to the right
plt.bar([i + width/2 for i in x],
        others_counts_aligned,
        width=width,
        label="All other boroughs")

plt.xlabel("Year")
plt.ylabel("Number of Assault Arrests")
plt.title("Assault Arrests by Year: Manhattan vs All Other Boroughs")
plt.xticks(x)
plt.legend()
plt.tight_layout()
plt.show()