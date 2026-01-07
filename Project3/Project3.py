import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("RUNNING BOOKS SCRIPT")

# Load the books dataset (local CSV file)
df = pd.read_csv("books.csv")

# Display more columns when inspecting the DataFrame and view the information about the dataset
print(df.shape)
print(df.columns[:10])

print(df.head())
print(df.info())

# Data cleaning and preparation

# Convert publication year to numeric (invalid values become NaN)
df["original_publication_year"] = pd.to_numeric(
    df["original_publication_year"], errors="coerce"
)

# Clean text columns
df["title"] = df["title"].astype(str).str.strip()
df["authors"] = df["authors"].astype(str).str.strip()

# Normalize missing language codes
df["language_code"] = df["language_code"].replace(
    {"": pd.NA, "unknown": pd.NA, "Unknown": pd.NA}
)

# Keep only rows that have the core information needed for analysis
needed_cols = ["original_publication_year", "title", "language_code"]
df_clean = df.dropna(subset=needed_cols).copy()

# Create a publication year column as an integer
df_clean["PUB_YEAR"] = df_clean["original_publication_year"].astype(int)

# Filter books by keyword in the title

# Select a keyword to analyze trends over time
keyword = "WAR"  # try: LOVE, MAGIC, GIRL, DEATH, EMPIRE

# Keep only books whose titles contain the keyword
keyword_df = df_clean[
    df_clean["title"].str.contains(keyword, case=False, na=False)
]

# Split books into English vs non-English groups

# Common language codes for English-language books
english_codes = {"en", "eng", "en-US", "en-GB"}

english_books = keyword_df[
    keyword_df["language_code"].isin(english_codes)
]

non_english_books = keyword_df[
    ~keyword_df["language_code"].isin(english_codes)
]

# Print total counts for context
print(f"\nKeyword: {keyword}")
print("Total English books:", len(english_books))
print("Total non-English books:", len(non_english_books))

# Count books per publication year

english_by_year = english_books.groupby("PUB_YEAR").size()
non_english_by_year = non_english_books.groupby("PUB_YEAR").size()

# Build a complete list of years covered by either group
all_years = sorted(
    set(english_by_year.index).union(set(non_english_by_year.index))
)

# Align yearly counts so both groups share the same x-axis
english_counts = [english_by_year.get(y, 0) for y in all_years]
non_english_counts = [non_english_by_year.get(y, 0) for y in all_years]

# Optional: focus on a readable time range
min_year, max_year = 1900, 2020
filtered = [
    (y, e, n)
    for y, e, n in zip(all_years, english_counts, non_english_counts)
    if min_year <= y <= max_year
]

if filtered:
    all_years, english_counts, non_english_counts = map(list, zip(*filtered))

# Visualization


plt.figure(figsize=(12, 6))
width = 0.35

# Bars for English-language books
plt.bar(
    [y - width / 2 for y in all_years],
    english_counts,
    width=width,
    label="English"
)

# Bars for non-English books
plt.bar(
    [y + width / 2 for y in all_years],
    non_english_counts,
    width=width,
    label="Non-English"
)

plt.xlabel("Publication Year")
plt.ylabel(f'Number of "{keyword}" Books')
plt.title(f'"{keyword}" in Book Titles by Year')
plt.xticks(all_years, rotation=90)
plt.legend()
plt.tight_layout()
plt.show()
