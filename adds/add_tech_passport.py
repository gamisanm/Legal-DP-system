from bson.binary import Binary  # Импорт для Binary
import streamlit as st
from database import db

def add_tech_passport(config, cities):
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
                # Сохраняем фото как Binary в MongoDB
                values["photo"] = Binary(uploaded_file.getvalue())
                
                try:
                    db[config["collection_name"]].insert_one(values)
                    st.success("🎉 Фото техпаспорта успешно добавлено!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении: {str(e)}")