import streamlit as st

def department_analysis_tab(processed_df, summary, category_col, value_col, dashboard_style, color_scheme, df, date_col):
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
    # 차트 행 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("부서별 채용 현황")
        from utils.visualization import create_bar_chart
        bar_fig = create_bar_chart(
            processed_df, 
            category_col, 
            value_col, 
            color_scheme,
            title=f"{category_col}별 {value_col}"
        )
        if bar_fig:
            st.plotly_chart(bar_fig, use_container_width=True)
        if len(processed_df) > 15:
            st.caption(f"* 모든 {category_col}이 표시되지 않을 수 있습니다.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("채용 분포")
        from utils.visualization import create_pie_chart
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
    # 차트 행 2
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("평균 대비 성과")
        from utils.visualization import create_bullet_chart
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
        from utils.visualization import create_heatmap
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
        from utils.advanced_charts import create_timeline_chart
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