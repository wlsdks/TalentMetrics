import streamlit as st

def advanced_analysis_tab(processed_df, value_col, date_col, create_outlier_chart, detect_outliers, create_distribution_chart, create_correlation_heatmap, calculate_trends, create_trend_chart):
    col1, col2 = st.columns(2)
    # 이상치 분석 (좌측)
    with col1:
        st.write("### 이상치 분석")
        outliers = detect_outliers(processed_df, value_col)
        if not outliers.empty:
            st.plotly_chart(create_outlier_chart(processed_df, value_col, outliers), use_container_width=True)
            st.write(f"발견된 이상치 수: {len(outliers)}")
        else:
            st.info("이상치가 발견되지 않았습니다.")
            st.plotly_chart(create_outlier_chart(processed_df, value_col, outliers), use_container_width=True)
    # 분포 분석 (우측)
    with col2:
        st.write("### 분포 분석")
        st.plotly_chart(create_distribution_chart(processed_df, value_col), use_container_width=True)
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