import streamlit as st
import pymongo
from datetime import datetime, date
from bson.objectid import ObjectId
from dateutil.parser import parse as date_parse
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Легализация водителя",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    }
    
    .stSidebar > div:first-child {
        padding-top: 2rem;
    }
    
    /* Card styling */
    .record-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .record-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .record-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .card-header {
        display: flex;
        justify-content: between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a202c;
        margin: 0;
    }
    
    .record-id {
        font-size: 0.8rem;
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-weight: 500;
    }
    
    .record-field {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    .field-label {
        font-weight: 500;
        color: #4a5568;
        flex: 0 0 40%;
    }
    
    .field-value {
        color: #2d3748;
        flex: 1;
        text-align: right;
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        flex: 1;
        border-top: 4px solid #667eea;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Form styling */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    /* Search container */
    .search-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #64748b;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
     
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 10px;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 10px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        border-radius: 10px;
        background: transparent;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Pagination */
    .pagination-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# MongoDB connection (replace with your actual MongoDB URI)
client = pymongo.MongoClient("mongodb+srv://fiftystasik:le5VjLrrrKpQ7gc9@cluster0.gsorenq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["leg_dep"]

# List of cities
cities = ["All", "Warszawa", "Gdańsk", "Kraków", "Poznań", "Łódź", "Katowice",
          "Wrocław", "Częstochowa", "Szczecin", "Lublin", "Białystok", "Bydgoszcz"]

# Configuration for each type
configs = {
    "🚗 Автопарки": {
        "collection_name": "autopark",
        "fields": ["name", "contact_number", "status", "submission_date", "wypis_number", "brand", "model", "plate_number", "vin_code"],
        "labels": ["Название автопарка", "Номер для связи", "Статус", "Дата подачи", "Номер выписа", "Марка авто", "Модель авто", "Номер авто", "VIN CODE"],
        "types": ["text", "text", "text", "date", "text", "text", "text", "text", "text"],
        "display_field": "name",
        "search_field": "name",
        "has_city": False,
        "icon": "🚗"
    },
    "👤 Клиенты": {
        "collection_name": "clients",
        "fields": ["full_name", "city", "added_by", "driver_id", "phone", "identification", "id_submission_date", "license_date", "medical_exam_date", "psychological_exam_date"],
        "labels": ["Полное имя", "Город", "Добавлен кем", "ID водителя", "Телефон", "Идентификация", "Дата подачи ID", "Дата лицензии", "Дата медосмотра", "Дата психоосмотра"],
        "types": ["text", "select", "text", "text", "text", "text", "date", "date", "date", "date"],
        "display_field": "full_name",
        "search_field": "full_name",
        "has_city": True,
        "icon": "👤"
    },
    "🚙 Авто": {
        "collection_name": "vehicles",
        "fields": ["full_name", "city", "added_by", "driver_id", "phone", "wypis_submission_date", "identification"],
        "labels": ["Полное имя", "Город", "Добавлен кем", "ID водителя", "Телефон", "Дата подачи wypis", "Идентификация"],
        "types": ["text", "select", "text", "text", "text", "date", "text"],
        "display_field": "full_name",
        "search_field": "full_name",
        "has_city": True,
        "icon": "🚙"
    }
}

# # Header
# st.markdown("""
# <div class="main-header">
#     <h1>🚗 Система управления легальным департаментом</h1>
#     <p>Управление автопарками, клиентами и транспортными средствами</p>
# </div>
# """, unsafe_allow_html=True)

# Sidebar with improved design
with st.sidebar:
    st.markdown("### ⚙️ Настройки")
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
    
    st.markdown("---")
    st.markdown("### 📊 Статистика")
    
    # Quick stats in sidebar
    config = configs[selected_type]
    collection = db[config["collection_name"]]
    
    total_count = collection.count_documents({})
    st.metric("Всего записей", total_count)
    
    if config["has_city"] and selected_city != "All":
        city_count = collection.count_documents({"city": selected_city})
        st.metric(f"В городе {selected_city}", city_count)

# Helper functions
def format_value(value):
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    elif isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    elif value is None or value == "":
        return "—"
    return str(value)

def display_modern_card(doc, config):
    display_name = doc.get(config["display_field"], "Неизвестно")
    doc_id = str(doc['_id'])[-8:]  # Show only last 8 characters of ID
    
    # Using streamlit components instead of raw HTML
    with st.container():
        # Card header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {config['icon']} {display_name}")
        with col2:
            st.markdown(f"<span style='background: rgba(99, 102, 241, 0.1); color: #6366f1; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.8rem;'>ID: {doc_id}</span>", unsafe_allow_html=True)
        
        # Card fields
        for field, label in zip(config["fields"], config["labels"]):
            value = format_value(doc.get(field))
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**{label}:**")
            with col2:
                st.markdown(f"{value}")
        
        st.markdown("---")  # Divider between cards
    
    return doc_id

def get_paginated_data(config, selected_city, context=""):
    query = {}
    if config["has_city"] and selected_city != "All":
        query["city"] = selected_city
    
    # # Search container
    # st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_key = f"search_{selected_type}_{context}"
        search = st.text_input(
            "🔍 Поиск",
            placeholder=f"Введите имя для поиска...",
            key=search_key,
            help="Поиск по имени с использованием регулярных выражений"
        )
        if search:
            query[config["search_field"]] = {"$regex": search, "$options": "i"}
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    collection = db[config["collection_name"]]
    total_items = collection.count_documents(query)
    items_per_page = 8  # Reduced for better UX
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    
    # Pagination container
    # st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"**Найдено:** {total_items} записей")
    
    with col2:
        page_key = f"page_{selected_type}_{context}"
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
    
    with col3:
        st.markdown(f"**На странице:** {items_per_page}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    data = list(
        collection.find(query)
        .sort(config["display_field"], 1)
        .skip((page - 1) * items_per_page)
        .limit(items_per_page)
    )
    return data

def view_data(config, selected_city):
    data = get_paginated_data(config, selected_city, context="view")
    if not data:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h3>Нет записей для отображения</h3>
            <p>Попробуйте изменить фильтры или добавить новые записи</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display cards in a grid
        cols = st.columns(2)
        for idx, doc in enumerate(data):
            with cols[idx % 2]:
                display_modern_card(doc, config)

def add_data(config, cities):
    st.markdown("### ➕ Добавление новой записи")
    
    with st.form("add_form", clear_on_submit=True):
        values = {}
        
        # Create form in columns for better layout
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
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "✅ Добавить запись",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Validate required fields
            empty_fields = [label for field, label, field_type in zip(config["fields"], config["labels"], config["types"]) 
                          if field_type == "text" and not values.get(field)]
            
            if empty_fields:
                st.error(f"Пожалуйста, заполните обязательные поля: {', '.join(empty_fields)}")
            else:
                # Convert dates to datetime
                for i, field in enumerate(config["fields"]):
                    if config["types"][i] == "date" and values[field]:
                        values[field] = datetime.combine(values[field], datetime.min.time())
                
                try:
                    db[config["collection_name"]].insert_one(values)
                    st.success("🎉 Запись успешно добавлена!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Ошибка при добавлении записи: {str(e)}")

def edit_data(config, selected_city):
    data = get_paginated_data(config, selected_city, context="edit")
    if not data:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📝</div>
            <h3>Нет записей для редактирования</h3>
            <p>Сначала добавьте записи или измените фильтры</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### ✏️ Выберите запись для редактирования")
        
        for doc in data:
            doc_id = display_modern_card(doc, config)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col2:
                if st.button("✏️ Редактировать", key=f"edit_button_{str(doc['_id'])}", use_container_width=True):
                    st.session_state.editing_doc = doc.copy()
        
        if "editing_doc" in st.session_state:
            doc = st.session_state.editing_doc
            st.markdown("---")
            st.markdown("### 📝 Редактирование записи")
            
            with st.form("edit_form"):
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
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.form_submit_button("❌ Отмена", use_container_width=True):
                        del st.session_state.editing_doc
                        st.rerun()
                with col3:
                    submitted = st.form_submit_button("💾 Сохранить изменения", use_container_width=True, type="primary")
                
                if submitted:
                    # Convert dates to datetime
                    for i, field in enumerate(config["fields"]):
                        if config["types"][i] == "date" and values[field]:
                            values[field] = datetime.combine(values[field], datetime.min.time())
                    
                    try:
                        db[config["collection_name"]].update_one({"_id": doc["_id"]}, {"$set": values})
                        st.success("🎉 Запись успешно обновлена!")
                        del st.session_state.editing_doc
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Ошибка при обновлении записи: {str(e)}")

# Main tabs with modern styling
tab1, tab2, tab3 = st.tabs(["👀 Просмотр", "✏️ Редактирование", "➕ Добавление"])

with tab1:
    view_data(config, selected_city)

with tab2:
    edit_data(config, selected_city)

with tab3:
    add_data(config, cities)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    <p>🚗 Система управления | Версия 2.0</p>
</div>
""", unsafe_allow_html=True)