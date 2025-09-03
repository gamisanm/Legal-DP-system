custom_css = """
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #2a2a2a;
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
        background: #121212;
    }
    
    .stSidebar > div:first-child {
        padding-top: 2rem;
    }
    
    /* Card styling */
    .record-card {
        background: #748799;
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
        color: white;
        margin: 0;
    }
    
    .record-id {
        font-size: 0.8rem;
        color: white;
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
        color: white;
        flex: 0 0 40%;
    }
    
    .field-value {
        color: white;
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
        color: white;
        margin: 0;
    }
    
    .stat-label {
        color: white;
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
        color: white;
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
"""