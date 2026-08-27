import json

arquivo = "Dados/Raw/archive/pnadc_2024/dicionario_metadados_pnadc_2024_v5.json"

with open(arquivo, "r", encoding="utf-8") as f:
    dicionario = json.load(f)

print("========== V1022 ==========")
print(dicionario["V1022"])

print("\n========== V1023 ==========")
print(dicionario["V1023"])

print("\n========== V2007 ==========")
print(dicionario["V2007"])

print("\n========== V3001 ==========")
print(dicionario["V3001"])

print("\n========== VD4001 ==========")
print(dicionario["VD4001"])