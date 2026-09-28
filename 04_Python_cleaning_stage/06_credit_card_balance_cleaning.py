import pandas as pd
import numpy as np

cc = pd.read_csv("01_project_data_set/credit_card_balance.csv")
print(cc.shape)

# Convert MONTHS_BALANCE to a readable positive value (0 = most recent, same convention as before)
cc["MONTHS_AGO"] = -cc["MONTHS_BALANCE"]

# The four "19.5% missing" drawing columns move together (749,816 rows each) --
# guide confirms this means "no drawing activity that month," so 0 is honest here.
drawing_cols = [
    "AMT_DRAWINGS_ATM_CURRENT",
    "AMT_DRAWINGS_OTHER_CURRENT",
    "AMT_DRAWINGS_POS_CURRENT",
    "CNT_DRAWINGS_ATM_CURRENT",
    "CNT_DRAWINGS_OTHER_CURRENT",
    "CNT_DRAWINGS_POS_CURRENT",
]
for col in drawing_cols:
    cc[col + "_MISSING"] = cc[col].isnull().astype(int)
    cc[col] = cc[col].fillna(0)

# AMT_INST_MIN_REGULARITY and CNT_INSTALMENT_MATURE_CUM (305,236 missing) --
# same idea: no installment cycle active yet that month, so 0 fits.
for col in ["AMT_INST_MIN_REGULARITY", "CNT_INSTALMENT_MATURE_CUM"]:
    cc[col + "_MISSING"] = cc[col].isnull().astype(int)
    cc[col] = cc[col].fillna(0)

# AMT_PAYMENT_CURRENT (767,988 missing, 20%) -- same "no payment that month" logic
cc["AMT_PAYMENT_CURRENT_MISSING"] = cc["AMT_PAYMENT_CURRENT"].isnull().astype(int)
cc["AMT_PAYMENT_CURRENT"] = cc["AMT_PAYMENT_CURRENT"].fillna(0)

# Check if AMT_RECIVABLE and AMT_TOTAL_RECEIVABLE are near-duplicates before touching either
print(
    "Correlation between AMT_RECIVABLE and AMT_TOTAL_RECEIVABLE:",
    cc["AMT_RECIVABLE"].corr(cc["AMT_TOTAL_RECEIVABLE"]),
)

# Final check
print(cc.isnull().sum()[cc.isnull().sum() > 0])
print("Shape:", cc.shape)

cc.to_csv("03_cleaned_data_sets/06_cleaned_credit_card_balance.csv", index=False)
print("Saved.")
