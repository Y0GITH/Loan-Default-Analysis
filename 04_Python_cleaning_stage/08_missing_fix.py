import pandas as pd

# ---- All 7 file paths, defined individually ----
BASE = r"C:\Users\Lenovo\Documents\fintach projects\01 Credit Risk  Loan Default\03_cleaned_data_sets"

PATH_APPLICATION_TRAIN = BASE + r"\01_cleaned_application_train.csv"
PATH_BUREAU = BASE + r"\02_cleaned_bureau.csv"
PATH_BUREAU_BALANCE = BASE + r"\03_cleaned_bureau_balance.csv"
PATH_INSTALLMENTS = BASE + r"\04_cleaned_installments_payments.csv"
PATH_PREVIOUS_APP = BASE + r"\05_clean_previous_application.csv"
PATH_CREDIT_CARD = BASE + r"\06_cleaned_credit_card_balance.csv"
PATH_POS_CASH = BASE + r"\07_clean_POS_CASH_balance.csv"


# ==========================================================
# application_train -- the only file that actually needs fixes
# ==========================================================
df = pd.read_csv(PATH_APPLICATION_TRAIN)

# 1. NAME_TYPE_SUITE
df["NAME_TYPE_SUITE"] = df["NAME_TYPE_SUITE"].fillna("Unknown")

# 2. CNT_FAM_MEMBERS
df["CNT_FAM_MEMBERS"] = df["CNT_FAM_MEMBERS"].fillna(df["CNT_FAM_MEMBERS"].median())

# 3. Social circle columns
social_cols = [
    "OBS_30_CNT_SOCIAL_CIRCLE",
    "DEF_30_CNT_SOCIAL_CIRCLE",
    "OBS_60_CNT_SOCIAL_CIRCLE",
    "DEF_60_CNT_SOCIAL_CIRCLE",
]
for col in social_cols:
    df[col + "_MISSING"] = df[col].isnull().astype(int)
    df[col] = df[col].fillna(0)

# 4. DAYS_LAST_PHONE_CHANGE
df["DAYS_LAST_PHONE_CHANGE"] = df["DAYS_LAST_PHONE_CHANGE"].fillna(
    df["DAYS_LAST_PHONE_CHANGE"].median()
)

# 5. AMT_REQ_CREDIT_BUREAU_* columns
bureau_req_cols = [
    "AMT_REQ_CREDIT_BUREAU_HOUR",
    "AMT_REQ_CREDIT_BUREAU_DAY",
    "AMT_REQ_CREDIT_BUREAU_WEEK",
    "AMT_REQ_CREDIT_BUREAU_MON",
    "AMT_REQ_CREDIT_BUREAU_QRT",
    "AMT_REQ_CREDIT_BUREAU_YEAR",
]
for col in bureau_req_cols:
    df[col + "_MISSING"] = df[col].isnull().astype(int)
    df[col] = df[col].fillna(0)

print(
    "application_train -- remaining missing values (should only show the intentional ones):"
)
print(df.isnull().sum()[df.isnull().sum() > 0])
print("Shape:", df.shape)

# Overwrite the SAME file, no new file created
df.to_csv(PATH_APPLICATION_TRAIN, index=False)
print("Overwritten:", PATH_APPLICATION_TRAIN)


# ==========================================================
# The other 6 files -- already fully cleaned, just a final
# confirmation pass. Not modified, only re-checked.
# ==========================================================
for name, path in [
    ("bureau", PATH_BUREAU),
    ("bureau_balance", PATH_BUREAU_BALANCE),
    ("installments_payments", PATH_INSTALLMENTS),
    ("previous_application", PATH_PREVIOUS_APP),
    ("credit_card_balance", PATH_CREDIT_CARD),
    ("POS_CASH_balance", PATH_POS_CASH),
]:
    check = pd.read_csv(path)
    missing = check.isnull().sum()
    missing = missing[missing > 0]
    print(
        f"\n{name} -- missing values found (expected: only the intentional ones we flagged earlier):"
    )
    print(missing if len(missing) > 0 else "None")
