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

# 내장 CSS 스타일 (기본 스타일시트 외 인라인 스타일)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
    /* 깔끔한 모던 스타일 적용 */
    :root {
        /* 기본 색상 팔레트 */
        --primary-50: #eef2ff;
        --primary-100: #e0e7ff;
        --primary-200: #c7d2fe;
        --primary-300: #a5b4fc;
        --primary-400: #818cf8;
        --primary-500: #6366f1;
        --primary-600: #4f46e5;
        --primary-700: #4338ca;
        --primary-800: #3730a3;
        --primary-900: #312e81;
        --primary-950: #1e1b4b;
        
        --success-50: #ecfdf5;
        --success-100: #d1fae5;
        --success-500: #10b981;
        --success-700: #047857;
        
        --danger-50: #fef2f2;
        --danger-100: #fee2e2;
        --danger-500: #ef4444;
        --danger-700: #b91c1c;
        
        --warning-50: #fffbeb;
        --warning-100: #fef3c7;
        --warning-500: #f59e0b;
        --warning-700: #b45309;
        
        --neutral-50: #fafafa;
        --neutral-100: #f5f5f5;
        --neutral-200: #e5e5e5;
        --neutral-300: #d4d4d4;
        --neutral-400: #a3a3a3;
        --neutral-500: #737373;
        --neutral-600: #525252;
        --neutral-700: #404040;
        --neutral-800: #262626;
        --neutral-900: #171717;
        
        /* 그림자 */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* 메인 스타일링 */
    body, .stApp {
        font-family: 'Pretendard', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
        background-color: var(--neutral-50);
    }
    
    /* 스크롤바 스타일 */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--neutral-100);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--neutral-300);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--neutral-400);
    }
    
    /* 헤더 스타일링 */
    .header-container {
        background: linear-gradient(120deg, var(--primary-600), var(--primary-800));
        color: white;
        padding: 1.75rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        transform: rotate(30deg);
        z-index: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
        flex-grow: 1;
    }
    
    .header-icon {
        font-size: 2.5rem;
        margin-right: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
        background: linear-gradient(to right, white, rgba(255, 255, 255, 0.8));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0;
        font-weight: 400;
        letter-spacing: -0.01em;
    }
    
    /* 카드 스타일링 */
    .dashboard-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        margin-bottom: 1.5rem;
        border: 1px solid var(--neutral-200);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to right, var(--primary-600), var(--primary-400));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .dashboard-card:hover::before {
        opacity: 1;
    }
    
    /* 메트릭 카드 스타일링 */
    .metric-card {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--neutral-200);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(to right, var(--primary-600), var(--primary-300));
        opacity: 0.7;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary-200);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 3rem;
        height: 3rem;
        margin: 0 auto 0.75rem;
        background: linear-gradient(135deg, var(--primary-500), var(--primary-700));
        border-radius: 50%;
        color: white;
        font-size: 1.25rem;
        box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-700);
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .metric-title {
        font-size: 1rem;
        color: var(--neutral-700);
        margin-bottom: 0.25rem;
        font-weight: 600;
    }
    
    .metric-desc {
        font-size: 0.875rem;
        color: var(--neutral-500);
    }
    
    /* 버튼 스타일링 */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
        color: white;
        border-radius: 0.375rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-700), var(--primary-600));
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .stButton > button:hover::after {
        transform: translateX(100%);
    }
    
    /* 다운로드 버튼 스타일링 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--success-500), #069668);
        color: white;
        border-radius: 0.375rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
        box-shadow: var(--shadow-sm);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #069668, var(--success-500));
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* 탭 스타일링 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        background-color: transparent;
        padding: 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1.5rem;
        border-radius: 0.5rem 0.5rem 0 0;
        background-color: var(--neutral-100);
        border: 1px solid var(--neutral-200);
        border-bottom: none;
        color: var(--neutral-600);
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--neutral-50);
        color: var(--primary-600);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: var(--primary-600) !important;
        font-weight: 600;
        border-top: 3px solid var(--primary-600);
        box-shadow: var(--shadow-sm);
    }
    
    /* 데이터프레임 스타일링 */
    .dataframe {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 0.5rem;
        overflow: hidden;
        border: 1px solid var(--neutral-200);
        box-shadow: var(--shadow-sm);
    }
    
    .dataframe th {
        background-color: var(--neutral-100);
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        color: var(--primary-800);
        border-bottom: 2px solid var(--neutral-300);
        position: sticky;
        top: 0;
        z-index: 1;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--neutral-200);
        transition: all 0.3s ease;
    }
    
    .dataframe tr:hover td {
        background-color: var(--neutral-50);
    }
    
    .dataframe tr:last-child td {
        border-bottom: none;
    }
    
    /* 인사이트 박스 스타일링 */
    .insight-box {
        background-color: var(--neutral-50);
        border-left: 4px solid var(--primary-600);
        padding: 1rem;
        border-radius: 0.375rem;
        margin-bottom: 1.25rem;
        transition: all 0.3s ease;
    }
    
    .insight-box:hover {
        box-shadow: var(--shadow-md);
        transform: translateX(2px);
    }
    
    /* 추세 표시 스타일링 */
    .positive-trend {
        color: var(--success-500);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .positive-trend::before {
        content: '↑';
    }
    
    .negative-trend {
        color: var(--danger-500);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .negative-trend::before {
        content: '↓';
    }
    
    .neutral-trend {
        color: var(--neutral-500);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .neutral-trend::before {
        content: '→';
    }
    
    /* 푸터 스타일링 */
    .footer {
        text-align: center;
        padding: 2.5rem 0;
        color: var(--neutral-500);
        font-size: 0.95rem;
        border-top: 1px solid var(--neutral-200);
        margin-top: 4rem;
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: var(--shadow-sm);
    }
    
    /* 애니메이션 효과 */
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(10px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .dashboard-card, .metric-card {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* 스태거드 애니메이션 효과 */
    .staggered-item:nth-child(1) { animation-delay: 0.1s; }
    .staggered-item:nth-child(2) { animation-delay: 0.2s; }
    .staggered-item:nth-child(3) { animation-delay: 0.3s; }
    .staggered-item:nth-child(4) { animation-delay: 0.4s; }
    .staggered-item:nth-child(5) { animation-delay: 0.5s; }
    
    /* 빈 상태 스타일링 */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background-color: white;
        border-radius: 0.75rem;
        box-shadow: var(--shadow-md);
        margin: 2rem 0;
    }
    
    .empty-state h2 {
        font-size: 1.8rem;
        color: var(--primary-600);
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .empty-state p {
        color: var(--neutral-600);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .feature-item {
        background-color: var(--neutral-50);
        padding: 1.25rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
        border: 1px solid var(--neutral-200);
        position: relative;
        overflow: hidden;
    }
    
    .feature-item:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        background-color: white;
    }
    
    .feature-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary-600), var(--primary-400));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-item:hover::before {
        opacity: 1;
    }
    
    .feature-item h3 {
        font-size: 1.2rem;
        color: var(--primary-600);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .feature-item p {
        color: var(--neutral-600);
        font-size: 0.95rem;
    }
    
    /* 그래프 스타일 개선 */
    .js-plotly-plot {
        border-radius: 0.5rem;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        box-shadow: var(--shadow-md);
    }
    
    /* 반응형 스타일 */
    @media screen and (max-width: 992px) {
        .metric-value {
            font-size: 1.8rem;
        }
        
        .metric-title {
            font-size: 0.95rem;
        }
        
        .dashboard-card {
            padding: 1rem;
        }
        
        .features {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media screen and (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .sub-title {
            font-size: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .metric-title {
            font-size: 0.9rem;
        }
        
        .dashboard-card {
            padding: 0.75rem;
        }
        
        .features {
            grid-template-columns: 1fr;
        }
    }
    
    /* 다크 모드 지원 */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: var(--primary-400);
            --primary-light: var(--primary-300);
            --primary-dark: var(--primary-600);
        }
        
        .stApp {
            background-color: var(--neutral-900);
            color: var(--neutral-200);
        }
        
        .dashboard-card,
        .metric-card,
        .dataframe th,
        .empty-state,
        .footer,
        [data-testid="stSidebar"] {
            background-color: var(--neutral-800);
            border-color: var(--neutral-700);
        }
        
        .sub-title {
            color: var(--neutral-400);
        }
        
        .metric-title {
            color: var(--neutral-300);
        }
        
        .metric-desc {
            color: var(--neutral-400);
        }
        
        .dataframe th {
            background-color: var(--neutral-800);
            color: var(--primary-300);
            border-bottom: 2px solid var(--neutral-700);
        }
        
        .dataframe td {
            border-bottom: 1px solid var(--neutral-700);
        }
        
        .dataframe tr:hover td {
            background-color: var(--neutral-800);
        }
        
        .insight-box {
            background-color: var(--neutral-800);
        }
        
        .feature-item {
            background-color: var(--neutral-800);
            border-color: var(--neutral-700);
        }
        
        .feature-item:hover {
            background-color: var(--neutral-700);
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 헤더 섹션
    st.markdown("""
    <div class="header-container">
        <div class="header-icon">
            <i class="fas fa-chart-line"></i>
        </div>
        <div class="header-content">
            <div class="main-title">TalentMetrics</div>
            <div class="sub-title">채용 데이터를 시각화하고 핵심 인사이트를 발견하세요</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. 파일 업로드/데모 선택만 먼저 받음
    config = render_sidebar()
    uploaded_file = config["uploaded_file"]
    use_demo = config.get("use_demo", False)
    df = None
    sheet_names = []
    
    # 2. 파일/데모 데이터 준비
    if use_demo:
        with st.spinner("데모 데이터 준비 중..."):
            demo_excel = create_demo_data()
            excel_file, sheet_names = load_excel_file(demo_excel)
            if excel_file and sheet_names:
                df = read_sheet_data(excel_file, sheet_names[0])
                uploaded_file = demo_excel
                st.success("데모 데이터가 준비되었습니다!")
    elif uploaded_file:
        with st.spinner("파일 분석 중..."):
            excel_file, sheet_names = load_excel_file(uploaded_file)
            if excel_file and sheet_names:
                sheet_name = st.sidebar.selectbox("시트 선택", sheet_names)
                df = read_sheet_data(excel_file, sheet_name)
                st.success(f"{uploaded_file.name} 파일이 성공적으로 로드되었습니다!")
    
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
        
        with st.spinner("데이터 처리 중..."):
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
                
                # 대시보드 표시
                render_hr_metrics_dashboard(summary, hr_metrics)
                
                # 탭 섹션
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📈 부서별 분석", 
                    "🔍 상세 분석", 
                    "🔄 비교 분석", 
                    "📊 고급 분석"
                ])
                
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
                <div class="feature-item staggered-item">
                    <h3><i class="fas fa-chart-bar"></i> 채용 현황 분석</h3>
                    <p>부서별 채용 현황을 한눈에 파악하고 분석하세요</p>
                </div>
                <div class="feature-item staggered-item">
                    <h3><i class="fas fa-exchange-alt"></i> 부서별 비교</h3>
                    <p>다양한 지표를 기반으로 부서 간 비교 분석을 수행하세요</p>
                </div>
                <div class="feature-item staggered-item">
                    <h3><i class="fas fa-chart-line"></i> 추세 분석</h3>
                    <p>시간에 따른 채용 추세를 파악하고 예측하세요</p>
                </div>
                <div class="feature-item staggered-item">
                    <h3><i class="fas fa-search"></i> 고급 인사이트</h3>
                    <p>데이터 기반의 스마트한 채용 의사결정을 내리세요</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()