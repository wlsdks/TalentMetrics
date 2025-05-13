import streamlit as st
import datetime
from utils.data_processor import suggest_columns

def render_sidebar(df=None):
    config = {
        "uploaded_file": None,
        "use_demo": False,
        "category_col": None,
        "value_col": None,
        "dashboard_style": "모던 블루"
    }
    
    # 사이드바 스타일 적용
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid var(--neutral-200);
            box-shadow: var(--shadow-sm);
        }
        
        .sidebar-header {
            padding: 1rem;
            border-bottom: 1px solid var(--neutral-200);
            margin-bottom: 1rem;
        }
        
        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        .sidebar-subtitle {
            font-size: 0.9rem;
            color: var(--neutral-600);
        }
        
        .sidebar-section {
            border-top: 1px solid var(--neutral-200);
            padding-top: 1rem;
            margin-top: 1rem;
        }
        
        /* 파일 업로더 스타일 */
        [data-testid="stFileUploader"] > div > div {
            padding: 1rem;
            border: 2px dashed var(--neutral-300);
            border-radius: 0.5rem;
            background-color: var(--neutral-50);
            transition: var(--transition-all);
        }
        
        [data-testid="stFileUploader"] > div > div:hover {
            border-color: var(--primary-color);
            background-color: #f0f4ff;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">TalentMetrics</div>
            <div class="sidebar-subtitle">HR 채용 데이터 분석</div>
        </div>
        """, unsafe_allow_html=True)
        
        if df is None:
            st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
            st.subheader("데이터 가져오기")
            
            uploaded_file = st.file_uploader(
                "엑셀 파일 업로드",
                type=["xlsx", "xls"],
                help="채용 데이터가 포함된 엑셀 파일을 업로드하세요.",
                key="file_uploader"
            )
            
            config["uploaded_file"] = uploaded_file
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "데모 데이터 사용", 
                    help="샘플 데이터로 대시보드를 체험해보세요.", 
                    key="demo_btn",
                    use_container_width=True
                ):
                    config["use_demo"] = True
                    return config
            with col2:
                if st.button(
                    "초기화", 
                    help="모든 설정을 초기화합니다.", 
                    key="reset_btn",
                    use_container_width=True
                ):
                    st.experimental_rerun()
        else:
            st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
            st.subheader("데이터 미리보기")
            
            with st.expander("데이터 샘플", expanded=True):
                st.dataframe(df.head(3), use_container_width=True)
            
            st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
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
                key="category_col_select",
                help="그룹화할 카테고리 열을 선택하세요 (예: 부서, 지역 등)"
            )
            config["category_col"] = category_col
            
            val_index = 0
            if suggested_val_cols and suggested_val_cols[0] in all_columns:
                val_index = all_columns.index(suggested_val_cols[0])
            
            value_col = st.selectbox(
                "인원수/값 열 선택",
                all_columns,
                index=val_index,
                key="value_col_select",
                help="분석할 수치 데이터 열을 선택하세요 (예: 인원수, 예산 등)"
            )
            config["value_col"] = value_col
            
            st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
            st.subheader("추가 설정")
            
            with st.expander("고급 옵션", expanded=False):
                date_col = st.selectbox(
                    "날짜 열 (선택사항)",
                    ["없음"] + all_columns,
                    index=0,
                    help="시간별 추세 분석을 위한 날짜 열"
                )
                config["date_col"] = date_col if date_col != "없음" else None
                
                budget_col = st.selectbox(
                    "예산 열 (선택사항)",
                    ["없음"] + all_columns,
                    index=0,
                    help="예산 분석을 위한 열"
                )
                config["budget_col"] = budget_col if budget_col != "없음" else None
                
                gender_col = st.selectbox(
                    "성별 열 (선택사항)",
                    ["없음"] + all_columns,
                    index=0,
                    help="성별 분석을 위한 열"
                )
                config["gender_col"] = gender_col if gender_col != "없음" else None
                
                age_col = st.selectbox(
                    "연령 열 (선택사항)",
                    ["없음"] + all_columns,
                    index=0,
                    help="연령대 분석을 위한 열"
                )
                config["age_col"] = age_col if age_col != "없음" else None
            
            st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
            st.subheader("시각화 스타일")
            
            dashboard_style = st.selectbox(
                "테마 선택",
                ["모던 블루", "다크 테마", "미니멀리스트", "HR 특화"],
                index=0,
                key="dashboard_style_select",
                help="대시보드의 색상과 스타일 테마"
            )
            config["dashboard_style"] = dashboard_style
            
            # 색상 미리보기
            if dashboard_style == "모던 블루":
                colors = ["#f8f9fa", "#e2e8f0", "#90cdf4", "#3182ce", "#2c5282"]
            elif dashboard_style == "다크 테마":
                colors = ["#1a202c", "#2d3748", "#667eea", "#434190", "#2c3e50"]
            elif dashboard_style == "미니멀리스트":
                colors = ["#ffffff", "#f7fafc", "#cbd5e0", "#718096", "#2d3748"]
            elif dashboard_style == "HR 특화":
                colors = ["#f0f8ff", "#c6f6d5", "#4fd1c5", "#38b2ac", "#234e52"]
            
            cols = st.columns(5)
            for i, col in enumerate(cols):
                col.markdown(
                    f"""<div style="background-color: {colors[i]}; height: 30px; width: 100%; border-radius: 4px;"></div>""",
                    unsafe_allow_html=True
                )
            
            st.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)
            st.caption(f"마지막 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 내보내기 버튼
            st.download_button(
                label="설정 내보내기",
                data=str(config),
                file_name="talent_metrics_config.txt",
                mime="text/plain",
                help="현재 대시보드 설정을 저장합니다",
            )
    
    return config