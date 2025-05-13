import streamlit as st
import time

def render_comparison_section(df, category_col, value_col, comparison_data, comparison_chart):
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("부서 비교")
    if "error" in comparison_data:
        st.error(comparison_data["error"])
        return
    st.plotly_chart(comparison_chart, use_container_width=True)
    cat1 = comparison_data["category1"]
    cat2 = comparison_data["category2"]
    diff = comparison_data["diff"]
    diff_percent = comparison_data["percent_diff"]
    st.info(
        f"**비교 결과:** {cat1['name']}({cat1['value']}명)은 "
        f"{cat2['name']}({cat2['value']}명)보다 {abs(diff)}명 "
        f"{'많습니다' if diff > 0 else '적습니다'} "
        f"(차이: {abs(round(diff_percent, 1))}%)"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            f"{cat1['name']} 평균 대비",
            f"{round(cat1['vs_avg'], 1)}%",
            delta=round(cat1['vs_avg'], 1)
        )
    with col2:
        st.metric(
            f"{cat2['name']} 평균 대비",
            f"{round(cat2['vs_avg'], 1)}%",
            delta=round(cat2['vs_avg'], 1)
        )
    st.markdown('</div>', unsafe_allow_html=True)

def render_enhanced_comparison_section(df, category_col, value_col, comparison_data, comparison_chart, hr_metrics):
    message_placeholder = st.empty()
    message_placeholder.info("비교 분석 중...")
    time.sleep(0.5)
    message_placeholder.empty()
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.plotly_chart(comparison_chart, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{comparison_data['category1']['name']} 분석")
        st.metric(
            "인원수",
            f"{comparison_data['category1']['value']:,.0f}명",
            f"평균 대비 {comparison_data['category1']['vs_avg']:,.1f}%"
        )
        if 'department_efficiency' in hr_metrics:
            dept1_efficiency = hr_metrics['department_efficiency'].get(comparison_data['category1']['name'], {})
            if dept1_efficiency:
                st.metric(
                    "인당 비용",
                    f"{dept1_efficiency.get('cost_per_head', 0):,.0f}원"
                )
    with col2:
        st.subheader(f"{comparison_data['category2']['name']} 분석")
        st.metric(
            "인원수",
            f"{comparison_data['category2']['value']:,.0f}명",
            f"평균 대비 {comparison_data['category2']['vs_avg']:,.1f}%"
        )
        if 'department_efficiency' in hr_metrics:
            dept2_efficiency = hr_metrics['department_efficiency'].get(comparison_data['category2']['name'], {})
            if dept2_efficiency:
                st.metric(
                    "인당 비용",
                    f"{dept2_efficiency.get('cost_per_head', 0):,.0f}원"
                )
    st.subheader("차이 분석")
    st.metric(
        "인원수 차이",
        f"{comparison_data['diff']:,.0f}명",
        f"{comparison_data['percent_diff']:,.1f}%"
    )
    st.markdown('</div>', unsafe_allow_html=True) 