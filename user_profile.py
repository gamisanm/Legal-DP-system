from datetime import datetime
from dateutil.parser import parse as date_parse
import streamlit as st
import os
from helpers import format_value
from database import db

def display_profile(doc, config, cities=None):
    """
    Отображает профиль записи и позволяет редактировать ее.
    
    :param doc: Документ из MongoDB
    :param config: Конфигурация для типа данных
    :param cities: Список городов (если применимо)
    """
    if cities is None:
        cities = []

    doc_id = str(doc['_id'])
    display_name = doc.get(config["display_field"], "Неизвестно")

    st.subheader(f"{config['icon']} Профиль: {display_name} (ID: {doc_id[-8:]})")

    # Отображение текущих данных
    with st.expander("📋 Текущие данные", expanded=True):
        for field, label in zip(config["fields"], config["labels"]):
            value = format_value(doc.get(field))
            st.write(f"**{label}:** {value}")
        
        if config["collection_name"] == "tech_passports" and "photo_path" in doc:
            st.image(doc["photo_path"], caption="Фото техпаспорта")

    # Кнопка для начала редактирования
    if st.button("✏️ Редактировать профиль"):
        st.session_state.editing_profile = True

    # Форма редактирования
    if "editing_profile" in st.session_state and st.session_state.editing_profile:
        st.divider()
        st.subheader("📝 Редактирование профиля")

        with st.form("profile_edit_form"):
            values = {}
            
            if config["collection_name"] == "tech_passports":
                uploaded_file = st.file_uploader("Заменить фото техпаспорта (опционально)", type=["jpg", "png", "jpeg"])

            with st.container():
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
                    st.session_state.editing_profile = False
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
                    
                    if config["collection_name"] == "tech_passports":
                        if uploaded_file:
                            os.makedirs("uploads", exist_ok=True)
                            photo_path = f"uploads/{uploaded_file.name}"
                            with open(photo_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            values["photo_path"] = photo_path
                        else:
                            values["photo_path"] = doc.get("photo_path")

                    try:
                        db[config["collection_name"]].update_one({"_id": doc["_id"]}, {"$set": values})
                        st.success("🎉 Профиль успешно обновлен!")
                        st.session_state.editing_profile = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Ошибка при обновлении профиля: {str(e)}")