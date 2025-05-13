import streamlit as st
import pandas as pd
import os

# 모듈 임포트
from utils.data_processor import (
    load_excel_file, read_sheet_data, process_data, 
    calculate_summary, generate_comparison_data,
    create_demo_data, suggest_columns, validate_data,
    preprocess_data, detect_outliers, calculate_trends
)
from utils.visualization import (
    get_color_scheme, create_bar_chart, create_pie_chart, 
    create_treemap, create_comparison_chart, create_bullet_chart, create_heatmap,
    create_trend_chart, create_outlier_chart, create_correlation_heatmap,
    create_distribution_chart
)
from utils.advanced_charts import (
    create_sunburst_chart, create_radar_chart, create_bubble_chart,
    create_timeline_chart, create_boxplot, create_sankey_diagram, create_gauge_chart
)
from utils.hr_metrics import calculate_hr_metrics
from utils.ui.sidebar import set_page_config, load_css, render_sidebar
from utils.ui.metrics import render_metrics, render_hr_metrics_dashboard
from utils.ui.comparison import render_comparison_section, render_enhanced_comparison_section
from utils.ui.empty_state import render_empty_state
from pages.department_analysis import department_analysis_tab
from pages.detail_analysis import detail_analysis_tab
from pages.comparison_analysis import comparison_analysis_tab
from pages.advanced_analysis import advanced_analysis_tab
from layout.title import render_title
from layout.footer import render_footer

# 페이지 설정
st.set_page_config(
    page_title="TalentMetrics - HR 채용 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    /* 전체 앱 스타일 */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #4b5563;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* 카드 스타일 */
    .dashboard-card {
        background-color: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        display: none;  /* 기본적으로 숨김 */
    }
    
    .dashboard-card:has(> div:not(:empty)) {
        display: block;  /* 내용이 있을 때만 표시 */
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2.5rem;
        border-bottom: 2px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 56px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        gap: 1rem;
        padding: 1rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
        color: #6b7280;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: white;
        border-bottom: none;
    }
    
    /* 메트릭 스타일 */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease-in-out;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: white;
        box-shadow: 4px 0 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    
    /* 데이터프레임 스타일 */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* 푸터 스타일 */
    .footer {
        text-align: center;
        padding: 3rem 0;
        color: #6b7280;
        font-size: 0.95rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 4rem;
    }
    
    /* 로딩 스피너 스타일 */
    .stSpinner > div {
        border-color: #2563eb;
    }
    
    /* 차트 컨테이너 스타일 */
    .chart-container {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        display: none;  /* 기본적으로 숨김 */
    }
    
    .chart-container:has(> div:not(:empty)) {
        display: block;  /* 내용이 있을 때만 표시 */
    }
    
    /* 빈 상태 스타일 */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    .empty-state h2 {
        color: #1f2937;
        margin-bottom: 1rem;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .empty-state p {
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    .empty-state .features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .empty-state .feature-item {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: left;
    }
    
    .empty-state .feature-item h3 {
        color: #2563eb;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .empty-state .feature-item p {
        color: #4b5563;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .sub-title {
            font-size: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .dashboard-card {
            padding: 1.5rem;
        }
        
        .empty-state .features {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
render_title()

# 메인 앱 로직
def main():
    # 초기화
    excel_file = None
    sheet_names = []
    df = None
    sheet_name = None

    # 사이드바 렌더링
    config = render_sidebar()
    uploaded_file = config["uploaded_file"]
    use_demo = config.get("use_demo", False)

    # 데모 데이터 사용 버튼이 눌렸을 때만 처리
    if use_demo:
        demo_excel = create_demo_data()
        excel_file, sheet_names = load_excel_file(demo_excel)
        if excel_file and sheet_names:
            # 첫 번째 시트 자동 선택
            sheet_name = sheet_names[0]
            df = read_sheet_data(excel_file, sheet_name)
            uploaded_file = demo_excel  # 이후 로직에서 업로드 파일처럼 취급
    
    if uploaded_file is not None:
        # 로딩 스피너
        with st.spinner("데이터 분석 중..."):
            # 엑셀 파일 로드
            excel_file, sheet_names = load_excel_file(uploaded_file)
            
            if excel_file and sheet_names:
                # 시트 선택
                sheet_name = st.sidebar.selectbox("시트 선택", sheet_names, key="sheet_selector")
                
                if sheet_name:
                    # 데이터 로드
                    df = read_sheet_data(excel_file, sheet_name)
                    
                    # 데이터프레임 로드된 후 필요한 UI 컴포넌트 추가
                    if df is not None:
                        # 카테고리 열과 값 열 선택 (사이드바에 추가)
                        with st.sidebar:
                            st.subheader("데이터 설정")
                            
                            # 모든 열 목록
                            all_columns = df.columns.tolist()
                            
                            # 카테고리 열 선택
                            category_col = st.selectbox(
                                "부서/카테고리 열 선택",
                                all_columns,
                                key="category_col_select"
                            )
                            config["category_col"] = category_col
                            
                            # 카테고리 열을 제외한 나머지 열들
                            remaining_cols = [col for col in all_columns if col != category_col]
                            
                            # 값 열 선택 (숫자형 데이터만)
                            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                            # 만약 숫자형 열이 없으면 나머지 모든 열 사용
                            if not numeric_cols:
                                numeric_cols = remaining_cols
                            
                            # 값 열 선택
                            value_col = st.selectbox(
                                "인원수/값 열 선택",
                                numeric_cols,
                                key="value_col_select"
                            )
                            config["value_col"] = value_col
                            
                            # 고급 설정 섹션
                            with st.expander("고급 설정"):
                                # 날짜 열 선택
                                date_cols = [col for col in all_columns if '날짜' in col.lower() or '일자' in col.lower() or '입사' in col.lower() or 'date' in col.lower()]
                                date_col = st.selectbox(
                                    "날짜 열 선택 (선택 사항)",
                                    ["없음"] + all_columns,
                                    index=0 if not date_cols else 1 + all_columns.index(date_cols[0]) if date_cols and date_cols[0] in all_columns else 0
                                )
                                date_col = None if date_col == "없음" else date_col
                                
                                # 예산 열 선택
                                budget_cols = [col for col in all_columns if '예산' in col.lower() or '비용' in col.lower() or 'budget' in col.lower() or 'cost' in col.lower()]
                                budget_col = st.selectbox(
                                    "예산 열 선택 (선택 사항)",
                                    ["없음"] + numeric_cols,
                                    index=0 if not budget_cols else 1 + numeric_cols.index(budget_cols[0]) if budget_cols and budget_cols[0] in numeric_cols else 0
                                )
                                budget_col = None if budget_col == "없음" else budget_col
                                
                                # 성별 열 선택
                                gender_cols = [col for col in all_columns if '성별' in col.lower() or 'gender' in col.lower()]
                                gender_col = st.selectbox(
                                    "성별 열 선택 (선택 사항)",
                                    ["없음"] + all_columns,
                                    index=0 if not gender_cols else 1 + all_columns.index(gender_cols[0]) if gender_cols and gender_cols[0] in all_columns else 0
                                )
                                gender_col = None if gender_col == "없음" else gender_col
                                
                                # 연령대 열 선택
                                age_cols = [col for col in all_columns if '연령' in col.lower() or '나이' in col.lower() or 'age' in col.lower()]
                                age_col = st.selectbox(
                                    "연령대 열 선택 (선택 사항)",
                                    ["없음"] + all_columns,
                                    index=0 if not age_cols else 1 + all_columns.index(age_cols[0]) if age_cols and age_cols[0] in all_columns else 0
                                )
                                age_col = None if age_col == "없음" else age_col
                            
                            # 고급 설정 값 저장
                            config["date_col"] = date_col
                            config["budget_col"] = budget_col
                            config["gender_col"] = gender_col
                            config["age_col"] = age_col
                            
                            # 값 선택 검증
                            if category_col == value_col:
                                st.error("카테고리 열과 값 열은 서로 다른 열이어야 합니다.")
                                category_col = None
                                value_col = None
                            
                            # 대시보드 스타일 선택
                            st.subheader("대시보드 스타일")
                            dashboard_style = st.selectbox(
                                "스타일 선택",
                                ["모던 블루", "테크 테마", "미니멀리스트", "다크 모드", "HR 특화"],
                                key="style_select",
                                index=0
                            )
                            config["dashboard_style"] = dashboard_style
    
    # 데이터가 로드된 경우 대시보드 표시
    if df is not None and "category_col" in config and "value_col" in config:
        category_col = config["category_col"]
        value_col = config["value_col"]
        dashboard_style = config["dashboard_style"]
        
        # 추가 열 정보
        date_col = config.get("date_col")
        budget_col = config.get("budget_col")
        gender_col = config.get("gender_col") 
        age_col = config.get("age_col")
        
        # 데이터 처리
        processed_df = process_data(df, category_col, value_col)
        
        if processed_df is not None and not processed_df.empty:
            # 데이터 검증
            is_valid, validation_message = validate_data(processed_df)
            if not is_valid:
                st.warning(validation_message)
            
            # 데이터 전처리
            processed_df = preprocess_data(processed_df)
            
            # 데이터 요약 통계 계산
            summary = calculate_summary(processed_df, value_col)
            
            # HR 지표 계산
            hr_metrics = calculate_hr_metrics(
                df, 
                category_col=category_col,
                headcount_col=value_col,
                budget_col=budget_col,
                date_col=date_col,
                gender_col=gender_col,
                age_col=age_col
            )
            
            # 색상 스키마 설정
            color_scheme, bg_color, text_color = get_color_scheme(dashboard_style)
            
            # HR 지표 대시보드 렌더링
            render_hr_metrics_dashboard(summary, hr_metrics)
            
            # 탭으로 여러 대시보드 스타일 제공
            tab1, tab2, tab3, tab4 = st.tabs(["📈 부서별 분석", "🔍 상세 분석", "🔄 비교 분석", "📊 고급 분석"])
            
            with tab1:
                department_analysis_tab(processed_df, summary, category_col, value_col, dashboard_style, color_scheme, df, date_col)
            with tab2:
                detail_analysis_tab(processed_df, category_col, value_col, df, budget_col, gender_col, age_col, color_scheme)
            with tab3:
                comparison_analysis_tab(
                    processed_df, category_col, value_col, color_scheme,
                    generate_comparison_data, create_comparison_chart, render_enhanced_comparison_section, hr_metrics
                )
            with tab4:
                advanced_analysis_tab(
                    processed_df, value_col, date_col,
                    create_outlier_chart, detect_outliers, create_distribution_chart, create_correlation_heatmap, calculate_trends, create_trend_chart
                )
            
            # 푸터
            render_footer()
            
        else:
            st.error("선택한 열에서 데이터를 처리하는 데 문제가 발생했습니다. 다른 열을 선택해 보세요.")
    else:
        # 빈 상태 표시
        st.markdown("""
        <div class="empty-state">
            <h2>TalentMetrics에 오신 것을 환영합니다</h2>
            <p>채용 데이터를 업로드하여 인사이트를 발견하세요</p>
            <div class="features">
                <div class="feature-item">
                    <h3>📊 채용 현황 분석</h3>
                    <p>부서별 채용 현황을 한눈에 파악하고 분석하세요</p>
                </div>
                <div class="feature-item">
                    <h3>🔄 부서별 비교</h3>
                    <p>다양한 지표를 기반으로 부서 간 비교 분석을 수행하세요</p>
                </div>
                <div class="feature-item">
                    <h3>📈 추세 분석</h3>
                    <p>시간에 따른 채용 추세를 파악하고 예측하세요</p>
                </div>
                <div class="feature-item">
                    <h3>🔍 고급 인사이트</h3>
                    <p>데이터 기반의 스마트한 채용 의사결정을 내리세요</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()