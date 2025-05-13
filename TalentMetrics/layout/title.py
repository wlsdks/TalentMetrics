import streamlit as st

def render_title():
    st.markdown("""
    <div class="header-container">
        <div class="header-content">
            <div class="main-title">TalentMetrics <i class="fas fa-chart-line"></i></div>
            <div class="sub-title">채용 데이터를 시각화하고 핵심 인사이트를 발견하세요</div>
        </div>
    </div>
    """, unsafe_allow_html=True)