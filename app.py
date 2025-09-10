import streamlit as st
from config import cities, configs
from database import db
from adds.add_autopark import add_autopark
from adds.add_client import add_client
from adds.add_vehicle import add_vehicle
from adds.add_tech_passport import add_tech_passport
from views.view_autopark import view_autopark
from views.view_client import view_client
from views.view_vehicle import view_vehicle
from views.view_tech_passport import view_tech_passport

# Page configuration
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
    
    config = configs[selected_type]
    
    if config["has_city"]:
        selected_city = st.selectbox(
            "Выберите город",
            cities,
            help="Фильтрация по городу (только для клиентов и авто)"
        )
    else:
        selected_city = None
    
    st.divider()
    st.subheader("📊 Статистика")
    
    collection = db[config["collection_name"]]
    
    total_count = collection.count_documents({})
    st.metric("Всего записей", total_count)
    
    if config["has_city"] and selected_city != "All":
        city_count = collection.count_documents({"city": selected_city})
        st.metric(f"В городе {selected_city}", city_count)

# Main tabs
tab1, tab2 = st.tabs(["👀 Просмотр", "➕ Добавление"])

with tab1:
    if selected_type == "🚗 Автопарки":
        view_autopark(config, selected_city, cities)
    elif selected_type == "👤 Клиенты":
        view_client(config, selected_city, cities)
    elif selected_type == "🚙 Авто":
        view_vehicle(config, selected_city, cities)
    elif selected_type == "📸 Техпаспорта":
        view_tech_passport(config, selected_city, cities)

with tab2:
    if selected_type == "🚗 Автопарки":
        add_autopark(config, cities)
    elif selected_type == "👤 Клиенты":
        add_client(config, cities)
    elif selected_type == "🚙 Авто":
        add_vehicle(config, cities)
    elif selected_type == "📸 Техпаспорта":
        add_tech_passport(config, cities)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #64748b; padding: 1rem;'>"
    "🚗 Система управления | Версия 2.0"
    "</div>",
    unsafe_allow_html=True
)