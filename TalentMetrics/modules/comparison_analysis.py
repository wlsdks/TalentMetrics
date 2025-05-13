import streamlit as st

def comparison_analysis_tab(processed_df, category_col, value_col, color_scheme, generate_comparison_data, create_comparison_chart, render_enhanced_comparison_section, hr_metrics):
    st.subheader("비교 분석")
    st.subheader("부서 비교 분석")
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <p style="margin: 0; font-size: 0.9rem;">두 개의 부서를 선택하여 채용 현황을 비교해보세요. 
        인원수, 효율성, 성장률 등 다양한 지표를 기반으로 비교 분석 결과를 확인할 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)
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
    comparison_data = generate_comparison_data(
        processed_df, 
        category_col, 
        value_col, 
        cat1, 
        cat2
    )
    comparison_chart = create_comparison_chart(
        comparison_data,
        category_col,
        value_col,
        color_scheme
    )
    if comparison_chart:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_enhanced_comparison_section(
            processed_df,
            category_col,
            value_col,
            comparison_data,
            comparison_chart,
            hr_metrics
        )
        st.markdown('</div>', unsafe_allow_html=True) 