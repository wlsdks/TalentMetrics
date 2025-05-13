import streamlit as st

def render_footer():
    st.markdown("""
    <div class="footer">
        <p>© 2025 TalentMetrics - HR 채용 대시보드 v2.0</p>
        <p style="font-size: 0.8rem; color: #9ca3af;">데이터 기반의 스마트한 채용 의사결정을 위한 솔루션</p>
    </div>
    """, unsafe_allow_html=True) 