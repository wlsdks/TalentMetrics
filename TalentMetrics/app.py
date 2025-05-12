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
from utils.ui import (
    set_page_config, load_css, render_sidebar, render_metrics, 
    render_hr_metrics_dashboard, render_enhanced_comparison_section, render_empty_state
)

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
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    /* 카드 스타일 */
    .dashboard-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 2px solid #2563eb;
    }
    
    /* 메트릭 스타일 */
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: white;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    
    /* 데이터프레임 스타일 */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* 푸터 스타일 */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6b7280;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown("""
<div class="main-title">TalentMetrics - HR 채용 대시보드</div>
<div class="sub-title">채용 데이터를 시각화하고 핵심 인사이트를 발견하세요</div>
""", unsafe_allow_html=True)

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
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("부서별 채용 현황")
                
                # 상단 요약 통계
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{summary['total_value']:,.0f}</div>
                        <div class="metric-label">총 채용 인원</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{summary['avg_value']:,.1f}</div>
                        <div class="metric-label">평균 채용 인원</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{summary['max_category'].get(value_col, 0):,.0f}</div>
                        <div class="metric-label">최대 채용 인원</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{summary['min_category'].get(value_col, 0):,.0f}</div>
                        <div class="metric-label">최소 채용 인원</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 차트 행 1
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("부서별 채용 현황")
                    
                    # 막대 차트
                    bar_fig = create_bar_chart(
                        processed_df, 
                        category_col, 
                        value_col, 
                        color_scheme,
                        title=f"{category_col}별 {value_col}"
                    )
                    
                    if bar_fig:
                        st.plotly_chart(bar_fig, use_container_width=True)
                    
                    # 데이터가 많을 경우 알림
                    if len(processed_df) > 15:
                        st.caption(f"* 모든 {category_col}이 표시되지 않을 수 있습니다.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("채용 분포")
                    
                    # 파이 차트 생성
                    pie_df = processed_df.head(10) if len(processed_df) > 10 else processed_df
                    pie_fig = create_pie_chart(
                        pie_df,
                        category_col,
                        value_col,
                        color_scheme
                    )
                    if pie_fig:
                        st.plotly_chart(pie_fig, use_container_width=True)
                    
                    # 데이터가 많을 경우 알림
                    if len(processed_df) > 10:
                        st.caption(f"* 상위 10개 {category_col}만 표시됩니다.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # 차트 행 2
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("평균 대비 성과")
                    
                    # 불릿 차트
                    bullet_fig, is_truncated = create_bullet_chart(
                        processed_df,
                        category_col,
                        value_col,
                        summary["avg_value"],
                        color_scheme
                    )
                    
                    if bullet_fig:
                        st.plotly_chart(bullet_fig, use_container_width=True)
                        
                        if is_truncated:
                            st.caption(f"* 상위 15개 {category_col}만 표시됩니다.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("히트맵 분석")
                    
                    # 히트맵
                    heatmap_fig = create_heatmap(
                        processed_df,
                        category_col,
                        value_col,
                        color_scheme
                    )
                    
                    if heatmap_fig:
                        st.plotly_chart(heatmap_fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # 시계열 데이터가 있으면 추세 차트 추가
                if date_col and date_col in df.columns:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("채용 추세 분석")
                    
                    # 타임라인 차트
                    timeline_fig = create_timeline_chart(
                        df,
                        date_col,
                        value_col,
                        category_col=category_col,
                        color_scheme=color_scheme
                    )
                    
                    if timeline_fig:
                        st.plotly_chart(timeline_fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.subheader("상세 데이터 분석")
                
                # 다양한 시각화 옵션 선택
                viz_options = ["트리맵", "레이더 차트", "상자 그림", "버블 차트"]
                if budget_col:
                    viz_options.append("효율성 분석")
                if gender_col:
                    viz_options.append("성별 분포")
                if age_col:
                    viz_options.append("연령대 분포")
                
                selected_viz = st.multiselect(
                    "표시할 시각화 선택", 
                    viz_options,
                    default=["트리맵", "레이더 차트"] if len(viz_options) >= 2 else viz_options[:1]
                )
                
                # 선택한 시각화 표시
                if "트리맵" in selected_viz:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader(f"{category_col} 분포 (트리맵)")
                    
                    treemap_fig = create_treemap(
                        processed_df,
                        category_col,
                        value_col,
                        color_scheme
                    )
                    
                    if treemap_fig:
                        st.plotly_chart(treemap_fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if "레이더 차트" in selected_viz:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("부서별 다차원 비교 (레이더 차트)")
                    
                    # 레이더 차트용 지표 선택
                    metrics_cols = []
                    if value_col:
                        metrics_cols.append(value_col)
                    if budget_col:
                        metrics_cols.append(budget_col)
                    
                    # 추가 숫자형 열 찾기
                    extra_metrics = [col for col in df.select_dtypes(include=['number']).columns 
                                    if col not in [value_col, budget_col] and col in df.columns]
                    metrics_cols.extend(extra_metrics[:3])  # 최대 3개 추가
                    
                    radar_fig = create_radar_chart(
                        processed_df,
                        category_col,
                        metrics_cols,
                        color_scheme
                    )
                    
                    if radar_fig:
                        st.plotly_chart(radar_fig, use_container_width=True)
                    else:
                        st.info("레이더 차트를 생성하려면 3개 이상의 숫자형 열이 필요합니다.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # 상세 데이터 테이블
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("상세 데이터")
                
                # 검색 기능 추가
                search_term = st.text_input("부서 검색", placeholder="검색어 입력...")
                
                # 검색어에 따라 필터링
                filtered_df = processed_df
                if search_term:
                    filtered_df = processed_df[processed_df[category_col].str.contains(search_term, case=False, na=False)]
                
                # 정렬 기능
                sort_col = st.radio("정렬 기준", [category_col, value_col], horizontal=True)
                sort_order = st.radio("정렬 순서", ["오름차순", "내림차순"], horizontal=True)
                
                # 정렬 적용
                if sort_order == "오름차순":
                    filtered_df = filtered_df.sort_values(by=sort_col)
                else:
                    filtered_df = filtered_df.sort_values(by=sort_col, ascending=False)
                
                # 데이터 테이블에 스타일링 적용
                st.dataframe(
                    filtered_df.style.background_gradient(cmap='Blues', subset=[value_col]),
                    use_container_width=True,
                    height=400
                )
                
                # 다운로드 버튼
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="CSV로 다운로드",
                    data=csv,
                    file_name=f"{category_col}_{value_col}_분석.csv",
                    mime="text/csv",
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.subheader("비교 분석")
                
                # 부서 비교 기능
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("부서 비교 분석")
                
                # 부서 비교 설명
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 0.9rem;">두 개의 부서를 선택하여 채용 현황을 비교해보세요. 
                    인원수, 효율성, 성장률 등 다양한 지표를 기반으로 비교 분석 결과를 확인할 수 있습니다.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 비교할 부서 선택
                categories = processed_df[category_col].unique().tolist()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    cat1 = st.selectbox("첫 번째 부서", categories, index=0)
                
                with col2:
                    remaining_cats = [c for c in categories if c != cat1]
                    cat2_index = 0 if remaining_cats else 0
                    cat2 = st.selectbox(
                        "두 번째 부서", 
                        remaining_cats,
                        index=cat2_index
                    )
                
                # 비교 데이터 생성
                comparison_data = generate_comparison_data(
                    processed_df, 
                    category_col, 
                    value_col, 
                    cat1, 
                    cat2
                )
                
                # 비교 차트 생성
                comparison_chart = create_comparison_chart(
                    comparison_data,
                    category_col,
                    value_col,
                    color_scheme
                )
                
                # 개선된 비교 섹션 렌더링
                if comparison_chart:
                    render_enhanced_comparison_section(
                        processed_df,
                        category_col,
                        value_col,
                        comparison_data,
                        comparison_chart,
                        hr_metrics
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                st.subheader("고급 분석")
                
                # 이상치 분석
                st.write("### 이상치 분석")
                outliers = detect_outliers(processed_df, value_col)
                if not outliers.empty:
                    st.plotly_chart(create_outlier_chart(processed_df, value_col, outliers))
                    st.write(f"발견된 이상치 수: {len(outliers)}")
                
                # 분포 분석
                st.write("### 분포 분석")
                st.plotly_chart(create_distribution_chart(processed_df, value_col))
                
                # 상관관계 분석
                if len(processed_df.select_dtypes(include=['number']).columns) > 1:
                    st.write("### 상관관계 분석")
                    numeric_cols = processed_df.select_dtypes(include=['number']).columns.tolist()
                    st.plotly_chart(create_correlation_heatmap(processed_df, numeric_cols))
                
                # 추세 분석
                if date_col:
                    st.write("### 추세 분석")
                    trends = calculate_trends(processed_df, date_col, value_col)
                    if trends:
                        st.plotly_chart(create_trend_chart(trends))
            
            # 푸터
            st.markdown("""
            <div class="footer">
                <p>© 2025 TalentMetrics - HR 채용 대시보드 v2.0</p>
                <p style="font-size: 0.8rem; color: #9ca3af;">데이터 기반의 스마트한 채용 의사결정을 위한 솔루션</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error("선택한 열에서 데이터를 처리하는 데 문제가 발생했습니다. 다른 열을 선택해 보세요.")
    else:
        # 빈 상태 표시
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h2 style="color: #1f2937; margin-bottom: 1rem;">TalentMetrics에 오신 것을 환영합니다</h2>
            <p style="color: #6b7280; margin-bottom: 2rem;">채용 데이터를 업로드하여 인사이트를 발견하세요</p>
            <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <h3 style="color: #2563eb; margin-bottom: 1rem;">시작하기</h3>
                <p style="color: #4b5563; margin-bottom: 1.5rem;">왼쪽 사이드바에서 Excel 파일을 업로드하세요</p>
                <ul style="text-align: left; color: #6b7280; margin-bottom: 1.5rem;">
                    <li>채용 현황 분석</li>
                    <li>부서별 비교</li>
                    <li>추세 분석</li>
                    <li>고급 인사이트</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()