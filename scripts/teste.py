import pandas as pd

raw = pd.read_parquet(
    "Dados/Raw/archive/pnadc_2024/PNADC_2024_v5.parquet"
)

dirty = pd.read_parquet(
    "Dados/dirty/PNADC_2024_dirty.parquet"
)

print("RAW:")
print(raw["V1022"].isna().sum())

print("DIRTY:")
print(dirty["V1022"].isna().sum())