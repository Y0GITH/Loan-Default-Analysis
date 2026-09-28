import pandas as pd
import numpy as np

bureau = pd.read_csv("01_project_data_set/bureau.csv")
print(bureau.shape)
bureau.head()

bureau = bureau.copy()  # defragment early

# days are negative in this dataset, flip them to positive years
bureau["YEARS_CREDIT"] = -bureau["DAYS_CREDIT"] / 365
bureau["YEARS_CREDIT_ENDDATE"] = -bureau["DAYS_CREDIT_ENDDATE"] / 365
bureau["YEARS_CREDIT_UPDATE"] = -bureau["DAYS_CREDIT_UPDATE"] / 365
# leaving DAYS_ENDDATE_FACT alone for now, nulls there mean something

# 99.9% is "currency 1", basically no signal here
print(bureau["CREDIT_CURRENCY"].value_counts())
bureau = bureau.drop(columns=["CREDIT_CURRENCY"])

# missing amount = no overdue / no annuity recorded, treating as 0
for col in ["AMT_CREDIT_MAX_OVERDUE", "AMT_ANNUITY"]:
    bureau[col + "_MISSING"] = bureau[col].isnull().astype(int)
    bureau[col] = bureau[col].fillna(0)

print(bureau[["AMT_CREDIT_MAX_OVERDUE", "AMT_ANNUITY"]].isnull().sum())  # expect 0s

print(
    bureau[["AMT_CREDIT_SUM_DEBT", "AMT_CREDIT_SUM_LIMIT", "AMT_CREDIT_SUM"]]
    .isnull()
    .sum()
)

# same logic -- missing debt/limit means nothing owed/available on record
for col in ["AMT_CREDIT_SUM_DEBT", "AMT_CREDIT_SUM_LIMIT"]:
    bureau[col + "_MISSING"] = bureau[col].isnull().astype(int)
    bureau[col] = bureau[col].fillna(0)

# only 13 missing out of 1.7M, median is fine
bureau["AMT_CREDIT_SUM"] = bureau["AMT_CREDIT_SUM"].fillna(
    bureau["AMT_CREDIT_SUM"].median()
)

print(
    bureau[["AMT_CREDIT_SUM_DEBT", "AMT_CREDIT_SUM_LIMIT", "AMT_CREDIT_SUM"]]
    .isnull()
    .sum()
)

# null DAYS_ENDDATE_FACT = credit still open, so we capture that as a flag
bureau["CREDIT_IS_CLOSED"] = bureau["DAYS_ENDDATE_FACT"].notnull().astype(int)

# null here just means no planned end date was recorded
bureau["DAYS_CREDIT_ENDDATE_MISSING"] = (
    bureau["DAYS_CREDIT_ENDDATE"].isnull().astype(int)
)

# not filling these with 0 or median -- there's no good numeric stand-in for "still active"
print(bureau[["CREDIT_IS_CLOSED", "DAYS_CREDIT_ENDDATE_MISSING"]].value_counts())

# moveing the food to table
bureau.to_csv("03_cleaned_data_sets/02_cleaned_bureau.csv", index=False)
print("done. shape:", bureau.shape)
