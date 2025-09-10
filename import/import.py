import csv
import sys
from pymongo import MongoClient
from collections import defaultdict

# Подключение к MongoDB
client = MongoClient("mongodb+srv://fiftystasik:le5VjLrrrKpQ7gc9@cluster0.gsorenq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["leg_dep"]
collection = db["clients"]

csv.field_size_limit(sys.maxsize)

with open("data.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=",")  
    data = list(reader)

seen = defaultdict(int)
for row in data:
    did = row.get("driver_id")
    if not did:
        continue
    seen[did] += 1
    if seen[did] > 1:
        row["driver_id"] = f"{did}_DUP{seen[did]-1}"

if data:
    collection.insert_many(data)

print(f"Импорт завершён! Загружено {len(data)} записей.")
