# UI 컴포넌트 및 레이아웃을 담당합니다:
import streamlit as st
import pandas as pd
import datetime
from utils.data_processor import create_demo_data, suggest_columns
import plotly.express as px
import plotly.graph_objects as go

def set_page_config():
    """
    페이지 기본 설정을 적용합니다.
    """
    st.set_page_config(
        page_title="TalentMetrics - HR 채용 대시보드",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_css():
    """
    CSS 스타일을 로드합니다.
    """
    try:
        with open("assets/css/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # 기본 CSS 스타일 적용
        css = """
        <style>
            .main {
                background-color: #f8f9fa;
            }
            .st-emotion-cache-16idsys {
                font-size: 2.5rem;
                font-weight: 700;
                color: #0f52ba;
            }
            .stButton>button {
                background-color: #0f52ba;
                color: white;
                border-radius: 5px;
                border: none;
                padding: 10px 24px;
                font-weight: 600;
            }
            .stButton>button:hover {
                background-color: #0d47a1;
            }
            .dashboard-card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .metric-value {
                font-size: 2rem;
                font-weight: 700;
                color: #0f52ba;
            }
            .metric-label {
                font-size: 1rem;
                color: #6c757d;
            }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

def render_sidebar(df=None):
    """
    사이드바 UI를 렌더링합니다.
    
    Args:
        df: 데이터프레임
        
    Returns:
        설정값 딕셔너리
    """
    with st.sidebar:
        st.header("설정")
        
        # 파일 업로더에 고유한 key 추가
        uploaded_file = st.file_uploader(
            "엑셀 파일 업로드", 
            type=["xlsx", "xls"],
            key="excel_file_uploader"  # 고유한 key 추가
        )
        
        # 기본 설정값
        config = {
            "uploaded_file": uploaded_file,
            "sheet_name": None,
            "category_col": None,
            "value_col": None,
            "dashboard_style": "기본 대시보드"
        }
        
        if uploaded_file is None:
            st.info("엑셀 파일을 업로드해주세요.")
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
            
            # 데모 데이터 다운로드 버튼
            if st.button("데모 데이터 다운로드"):
                demo_data = create_demo_data()
                st.download_button(
                    label="데모 엑셀 파일 다운로드",
                    data=demo_data,
                    file_name="hr_demo_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        if df is not None:
            # 데이터 미리보기
            st.subheader("데이터 미리보기")
            st.dataframe(df.head(3))
            
            # 열 선택
            st.subheader("데이터 설정")
            
            # 열 추천
            suggested_cat_cols, suggested_val_cols = suggest_columns(df)
            
            # 모든 열 목록
            all_columns = df.columns.tolist()
            
            # 부서/카테고리 열 선택
            cat_index = 0
            if suggested_cat_cols and suggested_cat_cols[0] in all_columns:
                cat_index = all_columns.index(suggested_cat_cols[0])
            
            category_col = st.selectbox(
                "부서/카테고리 열 선택",
                all_columns,
                index=cat_index
            )
            config["category_col"] = category_col
            
            # 값 열 선택
            val_index = 0
            if suggested_val_cols and suggested_val_cols[0] in all_columns:
                val_index = all_columns.index(suggested_val_cols[0])
            
            value_col = st.selectbox(
                "인원수/값 열 선택",
                all_columns,
                index=val_index
            )
            config["value_col"] = value_col
            
            # 대시보드 스타일 선택
            st.subheader("대시보드 스타일")
            dashboard_style = st.selectbox(
                "스타일 선택",
                ["기본 대시보드", "모던 블루", "다크 테마", "미니멀리스트", "HR 특화"]
            )
            config["dashboard_style"] = dashboard_style
            
            # 실시간 업데이트 표시
            st.markdown("---")
            st.caption(f"마지막 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return config

def render_metrics(summary, category_col, value_col):
    """
    주요 지표를 렌더링합니다.
    """
    if not summary:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("총 부서 수", summary["total_categories"], "")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("총 인원", summary["total_value"], "")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("평균 인원/부서", round(summary["avg_value"], 1), "")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        if summary["max_category"]:
            max_cat = summary["max_category"]
            st.metric(
                "최다 채용 부서", 
                f"{max_cat[category_col]} ({max_cat[value_col]}명)"
            )
        st.markdown('</div>', unsafe_allow_html=True)

def render_comparison_section(df, category_col, value_col, comparison_data, comparison_chart):
    """
    비교 분석 섹션을 렌더링합니다.
    """
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("부서 비교")
    
    if "error" in comparison_data:
        st.error(comparison_data["error"])
        return
    
    # 비교 차트
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # 비교 분석 결과
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
    
    # 평균 대비 분석
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

def render_hr_metrics_dashboard(summary, hr_metrics):
    """
    HR 지표 대시보드를 렌더링합니다.
    """
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("📈 HR 핵심 지표")
    
    # 기본 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "총 인력",
            f"{hr_metrics.get('total_headcount', 0):,.0f}명",
            delta=f"{hr_metrics.get('total_headcount', 0) - hr_metrics.get('avg_headcount', 0):,.0f}명"
        )
    
    with col2:
        st.metric(
            "평균 인력",
            f"{hr_metrics.get('avg_headcount', 0):,.1f}명",
            delta=f"{hr_metrics.get('avg_headcount', 0) - hr_metrics.get('min_headcount', 0):,.1f}명"
        )
    
    with col3:
        if 'total_budget' in hr_metrics:
            st.metric(
                "총 예산",
                f"{hr_metrics['total_budget']:,.0f}원",
                f"인당 {hr_metrics.get('avg_cost_per_head', 0):,.0f}원"
            )
    
    with col4:
        if 'yearly_growth_rates' in hr_metrics:
            latest_growth = list(hr_metrics['yearly_growth_rates'].values())[-1]
            st.metric(
                "연간 성장률",
                f"{latest_growth:.1f}%",
                delta=f"{latest_growth - list(hr_metrics['yearly_growth_rates'].values())[-2]:.1f}%"
            )
    
    # 성별 분포
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
    
    # 연령대 분포
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
    
    # 부서별 분포
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
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_enhanced_comparison_section(df, category_col, value_col, comparison_data, comparison_chart, hr_metrics):
    """
    개선된 비교 분석 섹션을 렌더링합니다.
    """
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # 비교 차트
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # 상세 비교 지표
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
    
    # 차이 분석
    st.subheader("차이 분석")
    st.metric(
        "인원수 차이",
        f"{comparison_data['diff']:,.0f}명",
        f"{comparison_data['percent_diff']:,.1f}%"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_empty_state():
    """
    파일이 업로드되지 않았을 때 표시할 빈 상태를 렌더링합니다.
    """
    st.markdown('<div style="text-align: center; padding: 50px 0;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/8891/8891165.png", width=150)
    st.markdown("## HR 채용 현황 대시보드")
    st.markdown("이 대시보드는 부서별 채용 현황을 시각화하는 도구입니다.")
    st.markdown("사용하려면 사이드바에서 엑셀 파일을 업로드해주세요.")
    st.markdown("</div>", unsafe_allow_html=True)