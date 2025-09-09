from datetime import datetime
from dateutil.parser import parse as date_parse
import streamlit as st
from helpers import format_value, get_paginated_data
from database import db

def display_card(doc, config):
    display_name = doc.get(config["display_field"], "Неизвестно")
    doc_id = str(doc['_id'])[-8:]
    
    with st.container(border=True):
        st.markdown(f"**{config['icon']} {display_name}** (ID: {doc_id})")
        
        for field, label in zip(config["fields"], config["labels"]):
            value = format_value(doc.get(field))
            st.write(f"{label}: {value}")
    
    return doc_id

def display_profile(doc, config, cities):
    doc_id = str(doc['_id'])
    display_name = doc.get(config["display_field"], "Неизвестно")

    st.subheader(f"{config['icon']} Профиль: {display_name} (ID: {doc_id[-8:]})")

    with st.expander("📋 Текущие данные", expanded=True):
        for field, label in zip(config["fields"], config["labels"]):
            value = format_value(doc.get(field))
            st.write(f"**{label}:** {value}")

    if st.button("✏️ Редактировать профиль"):
        st.session_state.editing_vehicle_profile = True

    if "editing_vehicle_profile" in st.session_state and st.session_state.editing_vehicle_profile:
        st.divider()
        st.subheader("📝 Редактирование профиля")

        with st.form("vehicle_edit_form"):
            values = {}
            col1, col2 = st.columns(2)

            for idx, (field, label, field_type) in enumerate(zip(config["fields"], config["labels"], config["types"])):
                current_col = col1 if idx % 2 == 0 else col2
                default_value = doc.get(field)

                with current_col:
                    if field_type == "date":
                        if isinstance(default_value, datetime):
                            default_value = default_value.date()
                        elif isinstance(default_value, str) and default_value:
                            try:
                                default_value = date_parse(default_value).date()
                            except Exception:
                                default_value = None
                        values[field] = st.date_input(label, value=default_value)
                    elif field_type == "text":
                        values[field] = st.text_input(label, value=format_value(default_value) if default_value != "—" else "")
                    elif field_type == "select" and field == "city":
                        index = cities[1:].index(default_value) if default_value in cities[1:] else 0
                        values[field] = st.selectbox(label, cities[1:], index=index)

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("❌ Отмена"):
                    st.session_state.editing_vehicle_profile = False
                    st.rerun()
            with col2:
                submitted = st.form_submit_button("💾 Сохранить изменения")

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
                        db[config["collection_name"]].update_one({"_id": doc["_id"]}, {"$set": values})
                        st.success("🎉 Профиль авто успешно обновлен!")
                        st.session_state.editing_vehicle_profile = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Ошибка при обновлении профиля: {str(e)}")

def view_vehicle(config, selected_city, cities):
    session_prefix = "vehicle_"
    if session_prefix + "view_mode" not in st.session_state:
        st.session_state[session_prefix + "view_mode"] = "list"

    if st.session_state[session_prefix + "view_mode"] == "list":
        data = get_paginated_data(config, selected_city, context="vehicle_view")
        if not data:
            st.info("Нет авто для отображения. Попробуйте изменить фильтры или добавить новые.")
        else:
            st.subheader("📋 Список авто")
            with st.container():
                cols = st.columns(2)
                for idx, doc in enumerate(data):
                    with cols[idx % 2]:
                        display_card(doc, config)
                        if st.button("👀 Открыть профиль", key=f"vehicle_view_profile_{str(doc['_id'])}"):
                            st.session_state[session_prefix + "profile_doc"] = doc
                            st.session_state[session_prefix + "view_mode"] = "profile"
                            st.rerun()

    elif st.session_state[session_prefix + "view_mode"] == "profile" and session_prefix + "profile_doc" in st.session_state:
        display_profile(st.session_state[session_prefix + "profile_doc"], config, cities)
        if st.button("🔙 Вернуться к списку"):
            st.session_state[session_prefix + "view_mode"] = "list"
            del st.session_state[session_prefix + "profile_doc"]
            st.rerun()