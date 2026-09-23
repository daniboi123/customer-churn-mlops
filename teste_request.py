import json
import requests

url = "http://127.0.0.1:5001/invocations"

# payload = {
#    "dataframe_split": {
#        "columns": [
#            "idade",
#            "renda_mensal",
#            "tempo_emprego_anos",
#            "score_interno",
#            "valor_solicitado",
#            "num_parcelas",
#            "tipo_renda",
#            "possui_restricao",
#        ],
#        "data": [
#            [34, 4200.0, 5.0, 620, 12000.0, 24, "CLT", "nao"],
#        ],
#    },
#    "params": {
#        "threshold": 0.5,
#    },
# }

# response = requests.post(
#    url,
#    headers={"Content-Type": "application/json"},
#    data=json.dumps(payload),
#    timeout=30,
# )

# print("Status code:", response.status_code)
# print(response.json())


##########################################

payload_invalido = {
   "dataframe_split": {
       "columns": [
           "idade",
           "renda_mensal",
           "tempo_emprego_anos",
           # "score_interno" removido de propósito
           "valor_solicitado",
           "num_parcelas",
           "tipo_renda",
           "possui_restricao",
       ],
       "data": [
           [34, 4200.0, 5.0, 12000.0, 24, "CLT", "nao"],
       ],
   },
   "params": {
       "threshold": 0.3,
   },
}

response = requests.post(
   url,
   headers={"Content-Type": "application/json"},
   data=json.dumps(payload_invalido),
   timeout=30,
)

print("Status code:", response.status_code)
print(response.text)

