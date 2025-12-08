import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ny_high_schools.csv")
pd.set_option('display.max_columns',  50)
pd.set_option('future.no_silent_downcasting', True)

metric_name = "Percent Scoring 80 or Above"

# My column is "Percent Scoring 80 or Above"
dirty_series = df[metric_name]

# Removing 's' values with NaN in order to be able to calculate the mean
clean_series_with_nans = pd.to_numeric(dirty_series, errors='coerce')

# Calculate the mean of the "Percent Scoring 80 or Above" column
mean_of_top80 = clean_series_with_nans.mean()

# First, replace 0s with NaNs and then fill in NaNs with the mean
df[metric_name] = clean_series_with_nans.replace(0, pd.NA).fillna(mean_of_top80)

# Create a Data frame containing my school only (DBN 01M140) for 2017
my_school_df  = df[
    (df['School DBN'] == "01M140") & (df['Year'] == 2017)
]

my_school_mean  = my_school_df[metric_name].mean()
print(f"P.S. 140 Nathan Straus School Mean across all regents exams for above 80% performers in 2017 is {my_school_mean:.2f}" )

# Dataframe containing other schools for 2017
other_school_df = df[
    (df['School DBN'] != "01M140") & (df['Year'] == 2017)
]
other_school_mean = other_school_df[metric_name].mean()
print(f"Other Schools Mean across all regents exams for above 80% performers in 2017 {other_school_mean:.2f}")

