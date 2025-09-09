from datetime import datetime, date
from dateutil.parser import parse as date_parse
import streamlit as st
from database import db

def format_value(value):
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    elif isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    elif value is None or value == "":
        return "—"
    return str(value)

def get_paginated_data(config, selected_city, context=""):
    query = {}
    if config["has_city"] and selected_city and selected_city != "All":
        query["city"] = selected_city
    
    with st.container():
        search_key = f"search_{config['collection_name']}_{context}"
        search = st.text_input(
            "🔍 Поиск",
            placeholder=f"Введите имя для поиска...",
            key=search_key,
            help="Поиск по имени с использованием регулярных выражений"
        )
        if search:
            query[config["search_field"]] = {"$regex": search, "$options": "i"}
    
    collection = db[config["collection_name"]]
    total_items = collection.count_documents(query)
    items_per_page = 8
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    
    with st.container():
        st.write(f"**Найдено:** {total_items} записей")
        
        page_key = f"page_{config['collection_name']}_{context}"
        if total_pages > 1:
            page = st.select_slider(
                "Страница",
                options=list(range(1, total_pages + 1)),
                value=1,
                key=page_key,
                format_func=lambda x: f"Стр. {x} из {total_pages}"
            )
        else:
            page = 1
        
        st.write(f"**На странице:** {items_per_page}")
    
    data = list(
        collection.find(query)
        .sort(config["display_field"], 1)
        .skip((page - 1) * items_per_page)
        .limit(items_per_page)
    )
    return data