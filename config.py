import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# List of cities
cities = ["All", "Warszawa", "Gdańsk", "Kraków", "Poznań", "Łódź", "Katowice",
          "Wrocław", "Częstochowa", "Szczecin", "Lublin", "Białystok", "Bydgoszcz"]

# MongoDB URI (replace with your actual URI)
MONGODB_URI = os.getenv("MONGODB_URI") or st.secrets["MONGODB_URI"]
DB_NAME = os.getenv("DB_NAME") or st.secrets["DB_NAME"]

# Configuration for each type
configs = {
    "🚗 Автопарки": {
        "collection_name": "autopark",
        "fields": ["name", "contact_number", "status", "submission_date", "wypis_number", "brand", "model", "plate_number", "vin_code"],
        "labels": ["Название автопарка", "Номер для связи", "Статус", "Дата подачи", "Номер выписа", "Марка авто", "Модель авто", "Номер авто", "VIN CODE"],
        "types": ["text", "text", "text", "date", "text", "text", "text", "text", "text"],
        "display_field": "name",
        "search_field": "name",
        "has_city": False,
        "icon": "🚗"
    },
    "👤 Клиенты": {
        "collection_name": "clients",
        "fields": ["full_name", "city", "added_by", "driver_id", "phone", "identification", "id_submission_date", "license_date", "medical_exam_date", "psychological_exam_date"],
        "labels": ["Полное имя", "Город", "Добавлен кем", "ID водителя", "Телефон", "Идентификация", "Дата подачи ID", "Дата лицензии", "Дата медосмотра", "Дата психоосмотра"],
        "types": ["text", "select", "text", "text", "text", "text", "date", "date", "date", "date"],
        "display_field": "full_name",
        "search_field": "full_name",
        "has_city": True,
        "icon": "👤"
    },
    "🚙 Авто": {
        "collection_name": "vehicles",
        "fields": ["vehicle_brand", "vehicle_model", "added_by", "vehicle_number", "phone", "extract_submission_date", "extract_number", "vin_code"],
        "labels": ["Марка", "Модель", "Добавлен кем", "Номер авто", "Телефон", "Дата подачи wypis", "Номер выписа", "VIN"],
        "types": ["text", "select", "text", "text", "text", "date", "text", "text"],
        "display_field": "full_name",
        "search_field": "full_name",
        "has_city": True,
        "icon": "🚙"
    }
}