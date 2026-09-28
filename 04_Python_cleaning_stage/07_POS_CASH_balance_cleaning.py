import pandas as pd
import numpy as np

pos = pd.read_csv("01_project_data_set/POS_CASH_balance.csv")
print(pos.shape)

pos["MONTHS_AGO"] = -pos["MONTHS_BALANCE"]

# Guide suggests checking if the ~26,000 missing rows correlate with a specific
# NAME_CONTRACT_STATUS before deciding how to handle them -- let's check first.
print(pos[pos["CNT_INSTALMENT"].isnull()]["NAME_CONTRACT_STATUS"].value_counts())

# Once confirmed, fill -- missing installment counts most likely mean the loan
# never had a defined plan (matches whatever status shows up above), so flag + 0.
for col in ["CNT_INSTALMENT", "CNT_INSTALMENT_FUTURE"]:
    pos[col + "_MISSING"] = pos[col].isnull().astype(int)
    pos[col] = pos[col].fillna(0)

print(pos.isnull().sum()[pos.isnull().sum() > 0])
print("Shape:", pos.shape)

pos.to_csv("03_cleaned_data_sets/07_clean_POS_CASH_balance.csv", index=False)
print("Saved.")
