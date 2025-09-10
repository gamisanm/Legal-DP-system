import csv

with open("data.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)  # печатает список колонок
