import streamlit as st

def detail_analysis_tab(processed_df, category_col, value_col, df, budget_col, gender_col, age_col, color_scheme):
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
    from utils.visualization import create_treemap, create_radar_chart
    # 트리맵
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
    # 레이더 차트
    if "레이더 차트" in selected_viz:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("부서별 다차원 비교 (레이더 차트)")
        metrics_cols = []
        if value_col:
            metrics_cols.append(value_col)
        if budget_col:
            metrics_cols.append(budget_col)
        extra_metrics = [col for col in df.select_dtypes(include=['number']).columns 
                        if col not in [value_col, budget_col] and col in df.columns]
        metrics_cols.extend(extra_metrics[:3])
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
    search_term = st.text_input("부서 검색", placeholder="검색어 입력...")
    filtered_df = processed_df
    if search_term:
        filtered_df = processed_df[processed_df[category_col].str.contains(search_term, case=False, na=False)]
    sort_col = st.radio("정렬 기준", [category_col, value_col], horizontal=True)
    sort_order = st.radio("정렬 순서", ["오름차순", "내림차순"], horizontal=True)
    if sort_order == "오름차순":
        filtered_df = filtered_df.sort_values(by=sort_col)
    else:
        filtered_df = filtered_df.sort_values(by=sort_col, ascending=False)
    st.dataframe(
        filtered_df.style.background_gradient(cmap='Blues', subset=[value_col]),
        use_container_width=True,
        height=400
    )
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSV로 다운로드",
        data=csv,
        file_name=f"{category_col}_{value_col}_분석.csv",
        mime="text/csv",
    )
    st.markdown('</div>', unsafe_allow_html=True) 