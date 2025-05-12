import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="HR 대시보드",
    page_icon="📊",
    layout="wide"
)

# 타이틀
st.title("HR 채용 현황 대시보드")
st.markdown("---")

# 사이드바 - 파일 업로드
with st.sidebar:
    st.header("설정")
    uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        st.success("파일이 성공적으로 업로드되었습니다!")

# 메인 화면
if uploaded_file is not None:
    # 엑셀 파일 읽기
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        # 시트 선택
        selected_sheet = st.sidebar.selectbox("시트 선택", sheet_names)
        
        # 데이터 읽기
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        # 데이터 미리보기
        st.subheader("데이터 미리보기")
        st.dataframe(df.head())
        
        # 열 선택
        st.sidebar.subheader("데이터 설정")
        cols = df.columns.tolist()
        
        # 부서/카테고리 열 선택
        dept_col = st.sidebar.selectbox("부서/카테고리 열 선택", cols)
        
        # 값 열 선택 (숫자형 데이터)
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if num_cols:
            value_col = st.sidebar.selectbox("인원수/값 열 선택", num_cols)
            
            # 간단한 차트 표시
            st.subheader("기본 차트")
            
            # 데이터 준비
            chart_data = df[[dept_col, value_col]].dropna()
            chart_data = chart_data.sort_values(by=value_col, ascending=False)
            
            # 막대 차트
            fig = px.bar(
                chart_data,
                x=dept_col,
                y=value_col,
                title=f"{dept_col}별 {value_col}"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    # 파일이 업로드되지 않은 경우 안내 메시지
    st.info("시작하려면 왼쪽 사이드바에서 엑셀 파일을 업로드하세요.")
    
    # 예시 데이터 설명
    st.markdown("""
    ### 예시 데이터 형식
    아래와 같은 형식의 엑셀 파일을 업로드하세요:
    
    | 부서 | 인원수 |
    |------|-------|
    | 인사팀 | 5 |
    | 마케팅 | 8 |
    | 개발팀 | 12 |
    | ... | ... |
    """)