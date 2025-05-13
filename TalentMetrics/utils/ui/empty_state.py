import streamlit as st

def render_empty_state():
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h2 style="color: #6b7280; margin-bottom: 20px;">데이터를 업로드해주세요</h2>
        <p style="color: #6b7280; margin-bottom: 30px;">
            채용 데이터가 포함된 엑셀 파일을 업로드하여 대시보드를 시작하세요.<br>
            또는 데모 데이터를 사용하여 기능을 체험해보세요.
        </p>
    </div>
    """, unsafe_allow_html=True) 