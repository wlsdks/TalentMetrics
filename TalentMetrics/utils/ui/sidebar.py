import streamlit as st
import datetime
from utils.data_processor import create_demo_data, suggest_columns

def set_page_config():
    st.set_page_config(
        page_title="TalentMetrics - HR 채용 대시보드",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_css():
    st.markdown("""
    <style>
    .dashboard-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    /* ... (생략: 기존 CSS) ... */
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(df=None):
    config = {
        "uploaded_file": None,
        "use_demo": False,
        "category_col": None,
        "value_col": None,
        "dashboard_style": "기본 대시보드"
    }
    with st.sidebar:
        if df is None:
            uploaded_file = st.file_uploader(
                "엑셀 파일 업로드",
                type=["xlsx", "xls"],
                help="채용 데이터가 포함된 엑셀 파일을 업로드하세요.",
                key="file_uploader"
            )
            config["uploaded_file"] = uploaded_file
            if st.button("데모 데이터 사용", help="샘플 데이터로 대시보드를 체험해보세요.", key="demo_btn"):
                config["use_demo"] = True
                return config
        else:
            st.subheader("데이터 미리보기")
            st.dataframe(df.head(3))
            st.subheader("데이터 설정")
            suggested_cat_cols, suggested_val_cols = suggest_columns(df)
            all_columns = df.columns.tolist()
            cat_index = 0
            if suggested_cat_cols and suggested_cat_cols[0] in all_columns:
                cat_index = all_columns.index(suggested_cat_cols[0])
            category_col = st.selectbox(
                "부서/카테고리 열 선택",
                all_columns,
                index=cat_index,
                key="category_col_select"
            )
            config["category_col"] = category_col
            val_index = 0
            if suggested_val_cols and suggested_val_cols[0] in all_columns:
                val_index = all_columns.index(suggested_val_cols[0])
            value_col = st.selectbox(
                "인원수/값 열 선택",
                all_columns,
                index=val_index,
                key="value_col_select"
            )
            config["value_col"] = value_col
            st.subheader("대시보드 스타일")
            dashboard_style = st.selectbox(
                "스타일 선택",
                ["기본 대시보드", "모던 블루", "다크 테마", "미니멀리스트", "HR 특화"],
                key="dashboard_style_select"
            )
            config["dashboard_style"] = dashboard_style
            st.markdown("---")
            st.caption(f"마지막 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return config 