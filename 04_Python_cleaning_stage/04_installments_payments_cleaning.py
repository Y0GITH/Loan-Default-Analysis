import pandas as pd
import numpy as np

inst = pd.read_csv("01_project_data_set/installments_payments.csv")
print(inst.shape)

# Convert DAYS_INSTALMENT / DAYS_ENTRY_PAYMENT to positive "days" for readability
inst["DAYS_INSTALMENT_POS"] = -inst["DAYS_INSTALMENT"]
inst["DAYS_ENTRY_PAYMENT_POS"] = -inst["DAYS_ENTRY_PAYMENT"]

# The core signal: how late, and how much shortfall
# For the 2,905 rows where payment was never made, DAYS_ENTRY_PAYMENT_POS
# will be NaN -- that's correct and expected, don't fill it. A missing
# "days late" here isn't an unknown number, it means "never paid," which
# is a different fact than any number could represent.
inst["DAYS_LATE"] = inst["DAYS_ENTRY_PAYMENT_POS"] - inst["DAYS_INSTALMENT_POS"]
inst["AMT_SHORTFALL"] = inst["AMT_INSTALMENT"] - inst["AMT_PAYMENT"]

# Flag missed payments explicitly, as their own clear signal
inst["PAYMENT_MISSED"] = inst["AMT_PAYMENT"].isnull().astype(int)

print("Missed payments:", inst["PAYMENT_MISSED"].sum())

# Final check -- DAYS_ENTRY_PAYMENT, AMT_PAYMENT, DAYS_ENTRY_PAYMENT_POS,
# DAYS_LATE, and AMT_SHORTFALL should all still show ~2,905 missing --
# that's correct, not an error, so don't try to "fix" it further.
print(inst.isnull().sum()[inst.isnull().sum() > 0])
print("Shape:", inst.shape)

inst.to_csv("03_cleaned_data_sets/04_cleaned_installments_payments.csv", index=False)
print("Saved.")
