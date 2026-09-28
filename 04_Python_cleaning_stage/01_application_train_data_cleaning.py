import pandas as pd
import numpy as np

df = pd.read_csv("01_project_data_set/application_train.csv")
print(df.shape)
print(df.head())

df = df.copy()

# fixing days_employed anomaly
print("Anomaly count:", (df["DAYS_EMPLOYED"] == 365243).sum())

df["DAYS_EMPLOYED_ANOM"] = df["DAYS_EMPLOYED"] == 365243
df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace({365243: np.nan})

# Handle CODE_GENDER = "XNA"
print(df["CODE_GENDER"].value_counts())
# F      202448
# M      105059
# XNA         4 so drop as its small
df = df[df["CODE_GENDER"] != "XNA"]
print("New shape after dropping XNA rows:", df.shape)

# Convert the DAYS_* columns to something readable
df["DAYS_EMPLOYED_ANOM"] = df["DAYS_EMPLOYED"] == 365243
df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace({365243: np.nan})
df = df[df["CODE_GENDER"] != "XNA"]

df["AGE_YEARS"] = -df["DAYS_BIRTH"] / 365
df["YEARS_EMPLOYED"] = -df["DAYS_EMPLOYED"] / 365

# Convert the remaining two DAYS_* columns  fixing negative ints
df["YEARS_REGISTRATION"] = -df["DAYS_REGISTRATION"] / 365
df["YEARS_ID_PUBLISH"] = -df["DAYS_ID_PUBLISH"] / 365

# Handle OWN_CAR_AGE
df["OWN_CAR_AGE"] = df["OWN_CAR_AGE"].fillna(0)  # as no car

# Check the housing/building block before deciding
housing_cols = [c for c in df.columns if c.endswith(("_AVG", "_MODE", "_MEDI"))] + [
    "FONDKAPREMONT_MODE",
    "HOUSETYPE_MODE",
    "TOTALAREA_MODE",
    "WALLSMATERIAL_MODE",
    "EMERGENCYSTATE_MODE",
]

print(df[housing_cols].isnull().mean().sort_values(ascending=False) * 100)

# Step 8 — Save a flag for housing info, then drop the whole block

# Rebuild the housing column list cleanly (removes accidental duplicates)
housing_cols = list(
    set(
        [c for c in df.columns if c.endswith(("_AVG", "_MODE", "_MEDI"))]
        + [
            "FONDKAPREMONT_MODE",
            "HOUSETYPE_MODE",
            "TOTALAREA_MODE",
            "WALLSMATERIAL_MODE",
            "EMERGENCYSTATE_MODE",
        ]
    )
)

# Save a flag: did we have ANY housing info for this applicant, before we drop it?
df["HOUSING_INFO_PROVIDED"] = df[housing_cols].notnull().any(axis=1).astype(int)

print(df["HOUSING_INFO_PROVIDED"].value_counts())

# Now drop the whole block
df = df.drop(columns=housing_cols)

print("Shape after dropping housing block:", df.shape)
# Shape after dropping housing block: (307507, 81)

# checking EXT_SOURCE_1,2,3 qty
print(df[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].isnull().mean() * 100)
# EXT_SOURCE_1    56.381156   mid safe
# EXT_SOURCE_2     0.214629   dont feel any isssue
# EXT_SOURCE_3    19.825565   low mid issue

# lets handle
ext_cols = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]

for col in ext_cols:
    df[col + "_MISSING"] = (
        df[col].isnull().astype(int)
    )  # Flag which rows were originally missing
    df[col] = df[col].fillna(
        df[col].median()
    )  # Fill with median — safe here since missingness is much lower than the housing block
# if u know to use lambda its good for u

print(
    df[ext_cols].isnull().sum()
)  # i was doing it in vs so i wish it was code note editor

print(
    df[[c + "_MISSING" for c in ext_cols]].sum()
)  # confirms how many rows got flagged

# Fill the two remaining small-missing numeric columns
df["AMT_ANNUITY"] = df["AMT_ANNUITY"].fillna(df["AMT_ANNUITY"].median())
df["AMT_GOODS_PRICE"] = df["AMT_GOODS_PRICE"].fillna(df["AMT_GOODS_PRICE"].median())

# Fill the occupation text column
df["OCCUPATION_TYPE"] = df["OCCUPATION_TYPE"].fillna("Unknown")

print(
    df[["AMT_ANNUITY", "AMT_GOODS_PRICE", "OCCUPATION_TYPE"]].isnull().sum()
)  # should all be 0

# Save the finished, cleaned table
df.to_csv("03_cleaned_data_sets/cleaned_application_train.csv", index=False)
print("Saved. Final shape:", df.shape)
