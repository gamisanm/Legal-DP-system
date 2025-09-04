from datetime import datetime
import streamlit as st
import os
from helpers import get_paginated_data, display_card
from database import db
from user_profile import display_profile  

def view_data(config, selected_city, cities):
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "list"

    if st.session_state.view_mode == "list":
        data = get_paginated_data(config, selected_city, context="view")
        if not data:
            st.info("Нет записей для отображения. Попробуйте изменить фильтры или добавить новые записи.")
        else:
            st.subheader("📋 Список записей")
            with st.container():
                cols = st.columns(2)
                for idx, doc in enumerate(data):
                    with cols[idx % 2]:
                        display_card(doc, config)
                        if st.button("👀 Открыть профиль", key=f"view_profile_{str(doc['_id'])}"):
                            st.session_state.profile_doc = doc
                            st.session_state.view_mode = "profile"
                            st.rerun()

    elif st.session_state.view_mode == "profile" and "profile_doc" in st.session_state:
        display_profile(st.session_state.profile_doc, config, cities)
        if st.button("🔙 Вернуться к списку"):
            st.session_state.view_mode = "list"
            del st.session_state.profile_doc
            st.rerun()

def add_data(config, cities):
    st.subheader("➕ Добавление новой записи")
    
    with st.form("add_form", clear_on_submit=True):
        values = {}
        
        with st.container():
            col1, col2 = st.columns(2)
            
            for idx, (field, label, field_type) in enumerate(zip(config["fields"], config["labels"], config["types"])):
                current_col = col1 if idx % 2 == 0 else col2
                
                with current_col:
                    if field_type == "text":
                        values[field] = st.text_input(label, help=f"Введите {label.lower()}")
                    elif field_type == "date":
                        values[field] = st.date_input(label, help=f"Выберите {label.lower()}")
                    elif field_type == "select" and field == "city":
                        values[field] = st.selectbox(label, cities[1:], help="Выберите город")
        
        submitted = st.form_submit_button("✅ Добавить запись")
        
        if submitted:
            empty_fields = [label for field, label, field_type in zip(config["fields"], config["labels"], config["types"]) 
                            if field_type == "text" and not values.get(field)]
            
            if empty_fields:
                st.error(f"Пожалуйста, заполните обязательные поля: {', '.join(empty_fields)}")
            else:
                for i, field in enumerate(config["fields"]):
                    if config["types"][i] == "date" and values[field]:
                        values[field] = datetime.combine(values[field], datetime.min.time())
                
                try:
                    db[config["collection_name"]].insert_one(values)
                    st.success("🎉 Запись успешно добавлена!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении записи: {str(e)}")

def add_tech_data(config):
    st.subheader("➕ Добавление фото техпаспорта")
    
    with st.form("add_tech_form", clear_on_submit=True):
        values = {}
        
        uploaded_file = st.file_uploader("Выберите фото техпаспорта", type=["jpg", "png", "jpeg"])
        
        with st.container():
            col1, col2 = st.columns(2)
            
            for idx, (field, label, field_type) in enumerate(zip(config["fields"], config["labels"], config["types"])):
                current_col = col1 if idx % 2 == 0 else col2
                
                with current_col:
                    if field_type == "text":
                        values[field] = st.text_input(label, help=f"Введите {label.lower()}")
        
        submitted = st.form_submit_button("✅ Добавить")
        
        if submitted:
            if not uploaded_file:
                st.error("Пожалуйста, загрузите фото техпаспорта.")
                return
            
            empty_fields = [label for field, label, field_type in zip(config["fields"], config["labels"], config["types"]) 
                            if field_type == "text" and not values.get(field)]
            
            if empty_fields:
                st.error(f"Пожалуйста, заполните обязательные поля: {', '.join(empty_fields)}")
            else:
                os.makedirs("uploads", exist_ok=True)
                photo_path = f"uploads/{uploaded_file.name}"
                with open(photo_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                values["photo_path"] = photo_path
                
                try:
                    db[config["collection_name"]].insert_one(values)
                    st.success("🎉 Фото техпаспорта успешно добавлено!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении: {str(e)}")

def view_tech_data(config):
    if "tech_view_mode" not in st.session_state:
        st.session_state.tech_view_mode = "list"

    if st.session_state.tech_view_mode == "list":
        data = get_paginated_data(config, None, context="tech_view")
        if not data:
            st.info("Нет фото техпаспортов для отображения.")
        else:
            st.subheader("📋 Список авто")
            with st.container():
                cols = st.columns(2)
                for idx, doc in enumerate(data):
                    with cols[idx % 2]:
                        display_card(doc, config)
                        if st.button("👀 Открыть профиль", key=f"tech_view_profile_{str(doc['_id'])}"):
                            st.session_state.tech_profile_doc = doc
                            st.session_state.tech_view_mode = "profile"
                            st.rerun()

    elif st.session_state.tech_view_mode == "profile" and "tech_profile_doc" in st.session_state:
        display_profile(st.session_state.tech_profile_doc, config)
        if st.button("🔙 Вернуться к списку"):
            st.session_state.tech_view_mode = "list"
            del st.session_state.tech_profile_doc
            st.rerun()