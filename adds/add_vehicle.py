from datetime import datetime
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
                    elif field_type == "select" and field == "city":
                        values[field] = st.selectbox(label, cities[1:], help="Выберите город")
        
        submitted = st.form_submit_button("✅ Добавить авто")
        
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
                    st.success("🎉 Авто успешно добавлено!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении авто: {str(e)}")