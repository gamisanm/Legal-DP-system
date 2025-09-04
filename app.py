import streamlit as st
from config import cities, configs
from views import view_data, add_data, add_tech_data, view_tech_data
from database import db

# Page configuration (theme управляется config.toml)
st.set_page_config(
    page_title="Легализация водителя",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🚗 Система управления LG")

# Sidebar
with st.sidebar:
    st.subheader("⚙️ Настройки")
    selected_type = st.selectbox(
        "Выберите тип данных",
        list(configs.keys()),
        help="Выберите тип данных для работы"
    )
    
    selected_city = st.selectbox(
        "Выберите город",
        cities,
        help="Фильтрация по городу (только для клиентов и авто)"
    )
    
    st.divider()
    st.subheader("📊 Статистика")
    
    config = configs[selected_type]
    collection = db[config["collection_name"]]
    
    total_count = collection.count_documents({})
    st.metric("Всего записей", total_count)
    
    if config["has_city"] and selected_city != "All":
        city_count = collection.count_documents({"city": selected_city})
        st.metric(f"В городе {selected_city}", city_count)

# Main tabs
tab1, tab2, tab3,  = st.tabs(["👀 Просмотр", "➕ Добавление", "📸 Фото техпаспортов"])

with tab1:
    view_data(config, selected_city, cities)

with tab2:
    add_data(config, cities)

with tab3:
    tech_config = {
        "collection_name": "tech_passports",
        "fields": ["brand", "model", "plate_number", "vin"],
        "labels": ["Марка", "Модель", "Номер авто", "VIN"],
        "types": ["text", "text", "text", "text"],
        "display_field": "plate_number",
        "search_field": "plate_number",
        "has_city": False,
        "icon": "📸"
    }
    tech_subtab1, tech_subtab2 = st.tabs(["➕ Добавить", "👀 Просмотр"])
    with tech_subtab1:
        add_tech_data(tech_config)
    with tech_subtab2:
        view_tech_data(tech_config)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #64748b; padding: 1rem;'>"
    "🚗 Система управления | Версия 2.0"
    "</div>",
    unsafe_allow_html=True
)