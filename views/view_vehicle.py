from datetime import datetime
from dateutil.parser import parse as date_parse
from bson.binary import Binary
import streamlit as st
from helpers import format_value, get_paginated_data
from database import db

def display_card(doc, config, columns_count=2):
    display_name = doc.get(config["display_field"], "Неизвестно")
    doc_id = str(doc['_id'])[-8:]
    
    with st.container(border=True):
        st.markdown(f"**{config['icon']} {display_name}** (ID: {doc_id})")
        
        # создаём колонки для полей внутри карточки
        fields = zip(config["fields"], config["labels"], config["types"])
        cols = st.columns(columns_count)
        
        for idx, (field, label, field_type) in enumerate(fields):
            current_col = cols[idx % columns_count]
            
            with current_col:
                if field_type == "file":
                    value = "Есть фото" if doc.get(field) else "Нет фото"
                    st.write(f"**{label}:** {value}")
                else:
                    value = format_value(doc.get(field))
                    st.write(f"**{label}:** {value}")
    
    return doc_id


def display_profile(doc, config, cities=None, columns_count=3):
    doc_id = str(doc['_id'])
    display_name = doc.get(config["display_field"], "Неизвестно")

    st.subheader(f"{config['icon']} Профиль: {display_name} (ID: {doc_id[-8:]})")

    with st.expander("📋 Текущие данные", expanded=True):
        fields = zip(config["fields"], config["labels"], config["types"])
        cols = st.columns(columns_count)
        for idx, (field, label, field_type) in enumerate(fields):
            current_col = cols[idx % columns_count]

            with current_col:
                if field_type == "file":
                    if field in doc:
                        st.image(doc[field], caption=label, width='stretch')
                    else:
                        st.write(f"{label}: Нет файла")
                else:
                    value = format_value(doc.get(field))
                    st.write(f"**{label}:** {value}")

    if st.button("✏️ Редактировать профиль"):
        st.session_state.editing_vehicle_profile = True

    if st.session_state.get("editing_vehicle_profile"):
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
                        values[field] = st.text_input(
                            label, 
                            value=format_value(default_value) if default_value != "—" else ""
                        )
                    
                    elif field_type == "file":
                        values[field] = st.file_uploader(label, type=["jpg", "png", "jpeg"])
                    
                    elif field_type == "select":
                        options = config.get("options", {}).get(field, [])
                        if field == "city" and cities:
                            options = cities[1:]
                        if options:
                            # определяем индекс выбранного значения
                            index = options.index(default_value) if default_value in options else 0
                            values[field] = st.selectbox(label, options, index=index)
                        else:
                            st.warning(f"⚠ Для поля {label} не заданы варианты выбора")
                            values[field] = None

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("❌ Отмена"):
                    st.session_state.editing_vehicle_profile = False
                    st.rerun()
            with col2:
                submitted = st.form_submit_button("💾 Сохранить изменения")

            if submitted:
                empty_fields = [
                    label for field, label, field_type in zip(config["fields"], config["labels"], config["types"])
                    if field_type in ("text", "select") and not values.get(field)
                ]

                if empty_fields:
                    st.error(f"Пожалуйста, заполните обязательные поля: {', '.join(empty_fields)}")
                else:
                    for i, field in enumerate(config["fields"]):
                        if config["types"][i] == "date" and values[field]:
                            values[field] = datetime.combine(values[field], datetime.min.time())
                        elif config["types"][i] == "file":
                            if values[field]:
                                values[field] = Binary(values[field].getvalue())
                            else:
                                values[field] = doc.get(field)
                    
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