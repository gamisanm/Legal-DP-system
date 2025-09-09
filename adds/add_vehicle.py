from datetime import datetime
from bson.binary import Binary
import streamlit as st
from database import db

def add_vehicle(config, cities):
    st.subheader("➕ Добавление нового авто")
    
    with st.form("add_vehicle_form", clear_on_submit=True):
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
                    elif field_type == "file":
                        values[field] = st.file_uploader(label, type=["jpg", "png", "jpeg"], help=f"Загрузите {label.lower()} (опционально)")
                    elif field_type == "select":
                        # Если в конфиге есть опции для этого поля
                        options = config.get("options", {}).get(field, [])
                        # Для поля city можно дополнительно подхватить города
                        if field == "city" and cities:
                            options = cities[1:]  
                        if options:
                            values[field] = st.selectbox(label, options, help=f"Выберите {label.lower()}")
                        else:
                            st.warning(f"⚠ Для поля {label} не заданы варианты выбора")
                            values[field] = None
        
        submitted = st.form_submit_button("✅ Добавить авто")
        
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
                    elif config["types"][i] == "file" and values[field]:
                        values[field] = Binary(values[field].getvalue())
                
                try:
                    db[config["collection_name"]].insert_one(values)
                    st.success("🎉 Авто успешно добавлено!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении авто: {str(e)}")