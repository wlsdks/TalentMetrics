import streamlit as st
import plotly.graph_objects as go
import time

def render_metrics(summary, category_col, value_col):
    if not summary:
        return
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">총 {}</div>
            <div class="metric-value">{:,}</div>
        </div>
        """.format(value_col, summary.get("total_value", 0)), unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">평균 {}</div>
            <div class="metric-value">{:,.1f}</div>
        </div>
        """.format(value_col, summary.get("avg_value", 0)), unsafe_allow_html=True)
    with col3:
        max_category = summary.get("max_category", {})
        max_value = max_category.get(value_col, 0) if isinstance(max_category, dict) else 0
        max_name = max_category.get(category_col, "N/A") if isinstance(max_category, dict) else "N/A"
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">최대 {}</div>
            <div class="metric-value">{:,}</div>
            <div class="metric-change">{}</div>
        </div>
        """.format(value_col, max_value, max_name), unsafe_allow_html=True)
    with col4:
        min_category = summary.get("min_category", {})
        min_value = min_category.get(value_col, 0) if isinstance(min_category, dict) else 0
        min_name = min_category.get(category_col, "N/A") if isinstance(min_category, dict) else "N/A"
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">최소 {}</div>
            <div class="metric-value">{:,}</div>
            <div class="metric-change">{}</div>
        </div>
        """.format(value_col, min_value, min_name), unsafe_allow_html=True)

def render_hr_metrics_dashboard(summary, hr_metrics):
    message_placeholder = st.empty()
    message_placeholder.info("데이터 처리 중...")
    time.sleep(0.5)
    message_placeholder.empty()
    st.markdown('<div class="dashboard-card" style="padding: 20px;">', unsafe_allow_html=True)
    st.subheader("📈 HR 핵심 지표")
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown("""
        <div class="metric-card" style="margin-bottom: 20px;">
            <div class="metric-label">총 인력</div>
            <div class="metric-value">{:,}명</div>
        </div>
        """.format(hr_metrics.get('total_headcount', 0)), unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="margin-bottom: 20px;">
            <div class="metric-label">평균 인력</div>
            <div class="metric-value">{:.1f}명</div>
        </div>
        """.format(hr_metrics.get('avg_headcount', 0)), unsafe_allow_html=True)
    with col3:
        if 'total_budget' in hr_metrics:
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 20px;">
                <div class="metric-label">총 예산</div>
                <div class="metric-value">{:,}원</div>
            </div>
            """.format(hr_metrics['total_budget']), unsafe_allow_html=True)
    with col4:
        if 'yearly_growth_rates' in hr_metrics:
            latest_growth = list(hr_metrics['yearly_growth_rates'].values())[-1]
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 20px;">
                <div class="metric-label">연간 성장률</div>
                <div class="metric-value">{:.1f}%</div>
            </div>
            """.format(latest_growth), unsafe_allow_html=True)
    if 'gender_distribution' in hr_metrics:
        st.subheader("성별 분포")
        gender_data = hr_metrics['gender_distribution']
        fig = go.Figure(data=[go.Pie(
            labels=list(gender_data.keys()),
            values=list(gender_data.values()),
            hole=.3
        )])
        fig.update_layout(
            title="성별 분포",
            showlegend=True,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    if 'age_distribution' in hr_metrics:
        st.subheader("연령대 분포")
        age_data = hr_metrics['age_distribution']
        fig = go.Figure(data=[go.Bar(
            x=list(age_data.keys()),
            y=list(age_data.values()),
            text=[f"{v:.1f}%" for v in age_data.values()],
            textposition='auto',
        )])
        fig.update_layout(
            title="연령대 분포",
            xaxis_title="연령대",
            yaxis_title="비율 (%)",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    if 'department_distribution' in hr_metrics:
        st.subheader("부서별 분포")
        dept_data = hr_metrics['department_distribution']
        fig = go.Figure(data=[go.Bar(
            x=list(dept_data['sum'].keys()),
            y=list(dept_data['sum'].values()),
            text=[f"{v:,.0f}명" for v in dept_data['sum'].values()],
            textposition='auto',
        )])
        fig.update_layout(
            title="부서별 인력 분포",
            xaxis_title="부서",
            yaxis_title="인원수",
            height=400,
            template="plotly_white",
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="#7f7f7f"
            ),
            margin=dict(l=40, r=40, t=40, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True) 