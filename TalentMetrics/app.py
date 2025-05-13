import streamlit as st
from utils.data_processor import (
    load_excel_file, read_sheet_data, process_data, calculate_summary,
    create_demo_data, validate_data, preprocess_data, detect_outliers, calculate_trends, generate_comparison_data
)
from utils.hr_metrics import calculate_hr_metrics
from utils.visualization import get_color_scheme
from utils.ui.sidebar import render_sidebar
from utils.ui.metrics import render_hr_metrics_dashboard
from layout.title import render_title
from layout.footer import render_footer
from modules.department_analysis import department_analysis_tab
from modules.detail_analysis import detail_analysis_tab
from modules.comparison_analysis import comparison_analysis_tab
from modules.advanced_analysis import advanced_analysis_tab
from utils.visualization.comparison import create_comparison_chart
from utils.ui.comparison import render_enhanced_comparison_section
from utils.visualization.outlier import create_outlier_chart
from utils.data_processor import detect_outliers, calculate_trends
from utils.visualization.distribution import create_distribution_chart
from utils.visualization.correlation import create_correlation_heatmap
from utils.visualization.trend import create_trend_chart

# 페이지 설정 및 스타일
st.set_page_config(
    page_title="TalentMetrics - HR 채용 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif; }
    .main-title { font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #2563eb, #1d4ed8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; letter-spacing: -0.02em; }
    .sub-title { font-size: 1.2rem; color: #4b5563; margin-bottom: 2.5rem; font-weight: 400; }
    .footer { text-align: center; padding: 3rem 0; color: #6b7280; font-size: 0.95rem; border-top: 1px solid #e5e7eb; margin-top: 4rem; }
</style>
""", unsafe_allow_html=True)
render_title()

def main():
    # 1. 파일 업로드/데모 선택만 먼저 받음
    config = render_sidebar()
    uploaded_file = config["uploaded_file"]
    use_demo = config.get("use_demo", False)
    df = None
    sheet_names = []
    # 2. 파일/데모 데이터 준비
    if use_demo:
        demo_excel = create_demo_data()
        excel_file, sheet_names = load_excel_file(demo_excel)
        if excel_file and sheet_names:
            df = read_sheet_data(excel_file, sheet_names[0])
            uploaded_file = demo_excel
    elif uploaded_file:
        excel_file, sheet_names = load_excel_file(uploaded_file)
        if excel_file and sheet_names:
            sheet_name = st.sidebar.selectbox("시트 선택", sheet_names)
            df = read_sheet_data(excel_file, sheet_name)
    # 3. df가 준비된 후, 열 선택 UI 제공
    if df is not None:
        config = render_sidebar(df)
    # 4. 분석 진행
    if df is not None and "category_col" in config and "value_col" in config and config["category_col"] and config["value_col"]:
        category_col = config["category_col"]
        value_col = config["value_col"]
        dashboard_style = config["dashboard_style"]
        date_col = config.get("date_col")
        budget_col = config.get("budget_col")
        gender_col = config.get("gender_col")
        age_col = config.get("age_col")
        processed_df = process_data(df, category_col, value_col)
        if processed_df is not None and not processed_df.empty:
            is_valid, validation_message = validate_data(processed_df)
            if not is_valid:
                st.warning(validation_message)
            processed_df = preprocess_data(processed_df)
            summary = calculate_summary(processed_df, value_col)
            hr_metrics = calculate_hr_metrics(
                df, category_col=category_col, headcount_col=value_col,
                budget_col=budget_col, date_col=date_col,
                gender_col=gender_col, age_col=age_col
            )
            color_scheme, _, _ = get_color_scheme(dashboard_style)
            render_hr_metrics_dashboard(summary, hr_metrics)
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
            render_footer()
        else:
            st.error("선택한 열에서 데이터를 처리하는 데 문제가 발생했습니다. 다른 열을 선택해 보세요.")
    else:
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