import streamlit as st

def render_title():
    st.markdown("""
    <div class="main-title">TalentMetrics - HR 채용 대시보드</div>
    <div class="sub-title">채용 데이터를 시각화하고 핵심 인사이트를 발견하세요</div>
    """, unsafe_allow_html=True) 