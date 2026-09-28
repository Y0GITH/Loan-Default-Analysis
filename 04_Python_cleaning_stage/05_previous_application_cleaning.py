import pandas as pd
import numpy as np

prev_app = pd.read_csv("01_project_data_set/previous_application.csv")  # fixed path
print(prev_app.shape)
prev_app = prev_app.copy()  # defragment early

days_cols = [
    "DAYS_FIRST_DRAWING",
    "DAYS_FIRST_DUE",
    "DAYS_LAST_DUE_1ST_VERSION",
    "DAYS_LAST_DUE",
    "DAYS_TERMINATION",
]

# check anomaly counts before fixing
for col in days_cols:
    print(col, (prev_app[col] == 365243).sum())

# 365243 is a placeholder for missing, same pattern as DAYS_EMPLOYED
for col in days_cols:
    prev_app[col] = prev_app[col].replace(365243, np.nan)

# verify they're gone
for col in days_cols:
    print(col, (prev_app[col] == 365243).sum())  # should all be 0

# Fix the anomaly, separately from the true missing values
for col in [
    "DAYS_FIRST_DRAWING",
    "DAYS_FIRST_DUE",
    "DAYS_LAST_DUE_1ST_VERSION",
    "DAYS_LAST_DUE",
    "DAYS_TERMINATION",
]:
    # Flag rows hit by the 365243 placeholder specifically
    prev_app[col + "_ANOM"] = prev_app[col] == 365243
    # Replace the placeholder with NaN -- now it joins the "genuinely missing" rows
    prev_app[col] = prev_app[col].replace({365243: np.nan})

# Recheck missing % now that both issues are combined into one clean NaN pattern
print(
    prev_app[
        [
            "DAYS_FIRST_DRAWING",
            "DAYS_FIRST_DUE",
            "DAYS_LAST_DUE_1ST_VERSION",
            "DAYS_LAST_DUE",
            "DAYS_TERMINATION",
        ]
    ]
    .isnull()
    .mean()
    * 100
)

# ---- 1. The lifecycle DAYS_* columns (42-54% missing) ----
# Same reasoning as bureau's DAYS_ENDDATE_FACT: missing means "this loan
# never became active," not "unknown." No honest number can stand in for
# that, so we leave these as NaN -- the _ANOM flags from Step 3 already
# mark what we fixed. Add one shared flag capturing the underlying reason:
prev_app["LOAN_WAS_ACTIVATED"] = prev_app["DAYS_FIRST_DUE"].notnull().astype(int)

# ---- 2. DAYS_FIRST_DRAWING -- now 96.2% missing, too sparse to keep ----
prev_app = prev_app.drop(columns=["DAYS_FIRST_DRAWING", "DAYS_FIRST_DRAWING_ANOM"])

# ---- 3. AMT_ANNUITY, AMT_GOODS_PRICE, CNT_PAYMENT (~22-23% missing) ----
# Guide says this cluster = rejected/unapproved apps with no finalized terms.
# Missing genuinely means "no annuity/goods price/term was ever set" -- 0 is honest here.
for col in ["AMT_ANNUITY", "AMT_GOODS_PRICE", "CNT_PAYMENT"]:
    prev_app[col + "_MISSING"] = prev_app[col].isnull().astype(int)
    prev_app[col] = prev_app[col].fillna(0)

# ---- 4. AMT_DOWN_PAYMENT, RATE_DOWN_PAYMENT (53.6% missing) ----
# Same idea -- many loan types have no down payment concept at all, so 0 fits.
for col in ["AMT_DOWN_PAYMENT", "RATE_DOWN_PAYMENT"]:
    prev_app[col + "_MISSING"] = prev_app[col].isnull().astype(int)
    prev_app[col] = prev_app[col].fillna(0)

# ---- 5. NFLAG_INSURED_ON_APPROVAL -- part of the lifecycle cluster, but ----
# this one's a binary flag, not a days-value, so 0 ("not insured") is a
# true statement even for loans that never got that far.
prev_app["NFLAG_INSURED_ON_APPROVAL"] = prev_app["NFLAG_INSURED_ON_APPROVAL"].fillna(0)

# ---- 6. RATE_INTEREST_PRIMARY / RATE_INTEREST_PRIVILEGED -- 99.7% missing ----
# Effectively unusable, and NAME_YIELD_GROUP already covers this need. Drop both.
prev_app = prev_app.drop(columns=["RATE_INTEREST_PRIMARY", "RATE_INTEREST_PRIVILEGED"])

# ---- 7. NAME_TYPE_SUITE (49.1% missing, text column) ----
prev_app["NAME_TYPE_SUITE"] = prev_app["NAME_TYPE_SUITE"].fillna("Unknown")

# ---- 8. PRODUCT_COMBINATION (346 missing, negligible) ----
prev_app["PRODUCT_COMBINATION"] = prev_app["PRODUCT_COMBINATION"].fillna("Unknown")

# ---- 9. AMT_CREDIT (1 missing, negligible) ----
prev_app["AMT_CREDIT"] = prev_app["AMT_CREDIT"].fillna(prev_app["AMT_CREDIT"].median())

# ---- Final check -- should show 0 for everything except the 4 lifecycle
# columns we deliberately left as NaN on purpose ----
print(prev_app.isnull().sum()[prev_app.isnull().sum() > 0])
print("Shape:", prev_app.shape)

# ---- Save ----
prev_app.to_csv("03_cleaned_data_sets/05_clean_previous_application.csv", index=False)
print("Saved.")
