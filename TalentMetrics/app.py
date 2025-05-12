import streamlit as st
import pandas as pd
import os

# 모듈 임포트
from utils.data_processor import (
    load_excel_file, read_sheet_data, process_data, 
    calculate_summary, generate_comparison_data
)
from utils.visualization import (
    get_color_scheme, create_bar_chart, create_pie_chart, 
    create_treemap, create_comparison_chart, create_bullet_chart, create_heatmap
)
from utils.ui import (
    set_page_config, load_css, render_sidebar, 
    render_metrics, render_comparison_section, render_empty_state
)

# 페이지 설정
set_page_config()

# CSS 로드
load_css()

# 타이틀
st.title("TalentMetrics - HR 채용 대시보드")
st.markdown("---")

# 메인 앱 로직
def main():
    # 사이드바 설정 및 파일 업로드
    excel_file = None
    sheet_names = []
    df = None
    sheet_name = None
    
    # 사이드바 렌더링
    config = render_sidebar()
    uploaded_file = config["uploaded_file"]
    
    if uploaded_file is not None:
        # 엑셀 파일 로드
        excel_file, sheet_names = load_excel_file(uploaded_file)
        
        if excel_file and sheet_names:
            # 시트 선택
            sheet_name = st.sidebar.selectbox("시트 선택", sheet_names)
            
            if sheet_name:
                # 데이터 로드
                df = read_sheet_data(excel_file, sheet_name)
                
                # 사이드바 업데이트 (데이터 로드 후)
                config = render_sidebar(df)
    
    # 데이터가 로드된 경우 대시보드 표시
    if df is not None and "category_col" in config and "value_col" in config:
        category_col = config["category_col"]
        value_col = config["value_col"]
        dashboard_style = config["dashboard_style"]
        
        # 데이터 처리
        processed_df = process_data(df, category_col, value_col)
        
        if processed_df is not None and not processed_df.empty:
            # 데이터 요약 통계 계산
            summary = calculate_summary(processed_df, value_col)
            
            # 색상 스키마 설정
            color_scheme, bg_color, text_color = get_color_scheme(dashboard_style)
            
            # 탭으로 여러 대시보드 스타일 제공
            tab1, tab2, tab3 = st.tabs(["주요 지표", "상세 분석", "비교 분석"])
            
            with tab1:
                st.subheader("주요 HR 채용 지표")
                
                # 상단 요약 통계
                render_metrics(summary, category_col, value_col)
                
                # 차트 영역
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
                        st.caption(f"* 모든 {category_col}이 표시되지 않을 수 있습니다. 상세 분석 탭에서 전체 데이터를 확인하세요.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("채용 분포 (파이 차트)")
                    
                    # 파이 차트 (너무 많은 카테고리가 있을 경우 상위 10개만 표시)
                    pie_df = processed_df.head(10) if len(processed_df) > 10 else processed_df
                    
                    pie_fig = create_pie_chart(
                        pie_df,
                        category_col,
                        value_col,
                        color_scheme
                    )
                    
                    if pie_fig:
                        st.plotly_chart(pie_fig, use_container_width=True)
                    
                    if len(processed_df) > 10:
                        st.caption(f"* 상위 10개 {category_col}만 표시됩니다.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.subheader("상세 분석")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader(f"{category_col} 분포 (트리맵)")
                    
                    # 트리맵
                    treemap_fig = create_treemap(
                        processed_df,
                        category_col,
                        value_col,
                        color_scheme
                    )
                    
                    if treemap_fig:
                        st.plotly_chart(treemap_fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                    st.subheader("히트맵")
                    
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
                
                # 상세 데이터 테이블
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("상세 데이터")
                
                # 데이터 테이블에 스타일링 적용
                st.dataframe(
                    processed_df.style.background_gradient(cmap='Blues', subset=[value_col]),
                    use_container_width=True,
                    height=400
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.subheader("비교 분석")
                
                # 부서 비교 기능
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("부서 비교")
                
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
                
                # 비교 섹션 렌더링
                if comparison_chart:
                    render_comparison_section(
                        processed_df,
                        category_col,
                        value_col,
                        comparison_data,
                        comparison_chart
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 평균 대비 성과 차트
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("평균 대비 성과")
                
                # 불릿 차트 생성
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
                
            # 푸터
            st.markdown("---")
            st.caption("© 2025 TalentMetrics - HR 채용 대시보드 v1.0")
            
        else:
            st.error("선택한 열에서 데이터를 처리하는 데 문제가 발생했습니다. 다른 열을 선택해 보세요.")
    else:
        # 빈 상태 표시
        render_empty_state()

if __name__ == "__main__":
    main()