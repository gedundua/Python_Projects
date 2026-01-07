df = pd.read_csv("data/books.csv")

import pandas as pd
import matplotlib.pyplot as plt

# 1) Load dataset
# (Goodbooks-10k books.csv)
url = "https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv"
df = pd.read_csv(url)

pd.set_option("display.max_columns", 50)

# 2) Cleaning (convert year to numeric)
df["original_publication_year"] = pd.to_numeric(df["original_publication_year"], errors="coerce")

# Basic text cleanup
df["authors"] = df["authors"].astype(str).str.strip()
df["title"] = df["title"].astype(str).str.strip()

# 3) Keep rows where our key columns exist (like needed_cols in your script)
needed_cols = ["original_publication_year", "authors", "title"]
df_clean = df.dropna(subset=needed_cols).copy()

# Extract "YEAR" as int (similar to ARREST_YEAR)
df_clean["PUB_YEAR"] = df_clean["original_publication_year"].astype(int)

# 4) Filter to one author (analog to "ASSAULT")
target_author = "Stephen King"  # <-- change this
author_df = df_clean[df_clean["authors"].str.contains(target_author, case=False, na=False)]
others_df = df_clean[~df_clean["authors"].str.contains(target_author, case=False, na=False)]

# 5) Count books per year for author vs others
yearly_author = author_df.groupby("PUB_YEAR").size()
yearly_others = others_df.groupby("PUB_YEAR").size()

# 6) Align years (same approach you used)
all_years = sorted(set(yearly_author.index).union(set(yearly_others.index)))

author_counts_aligned = [yearly_author.get(y, 0) for y in all_years]
others_counts_aligned = [yearly_others.get(y, 0) for y in all_years]

# Optional: focus on a reasonable year window so the chart is readable
# (uncomment if you want)
# min_year, max_year = 1900, 2020
# filtered = [(y, a, o) for y, a, o in zip(all_years, author_counts_aligned, others_counts_aligned)
#             if min_year <= y <= max_year]
# all_years, author_counts_aligned, others_counts_aligned = map(list, zip(*filtered))

# 7) Bar chart
plt.figure(figsize=(12, 6))
x = all_years
width = 0.35

plt.bar([i - width/2 for i in x], author_counts_aligned, width=width, label=f"{target_author}")
plt.bar([i + width/2 for i in x], others_counts_aligned, width=width, label="All other authors")

plt.xlabel("Publication Year")
plt.ylabel("Number of Books in Dataset")
plt.title(f"Books by Year: {target_author} vs All Other Authors")
plt.xticks(x, rotation=90)
plt.legend()
plt.tight_layout()
plt.show()