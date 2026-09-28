import pandas as pd

bureau_balance = pd.read_csv(
    "01_project_data_set/bureau_balance.csv",
    dtype={"SK_ID_BUREAU": "int32", "MONTHS_BALANCE": "int16", "STATUS": "category"},
)  # after this it loded on my pc
print(bureau_balance.shape)  # (27299925, 3)
bureau_balance.head()

# checking count
print(bureau_balance["STATUS"].value_counts())

# Create an ordered numeric version of status - i used ai hear
status_map = {
    "C": -1,  # closed
    "X": -2,  # unknown
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
}
bureau_balance["STATUS_NUMERIC"] = bureau_balance["STATUS"].map(status_map)

print(bureau_balance["STATUS_NUMERIC"].value_counts())

bureau_balance.to_csv("03_cleaned_data_sets/03_cleaned_bureau_balance.csv", index=False)
print("Saved. Final shape:", bureau_balance.shape)
