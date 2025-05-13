import streamlit as st
import datetime
from utils.data_processor import suggest_columns

def render_sidebar(df=None):
    config = {
        "uploaded_file": None,
        "use_demo": False,
        "category_col": None,
        "value_col": None,
        "dashboard_style": "모던 블루"
    }
    
    # 사이드바 스타일 적용
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid var(--neutral-200, #e5e5e5);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .sidebar-header {
            padding: 1.5rem 1rem;
            border-bottom: 1px solid var(--neutral-200, #e5e5e5);
            margin-bottom: 1.5rem;
            background: linear-gradient(to right, var(--primary-50, #eef2ff), white);
        }
        
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary-700, #4338ca);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
        }
        
        .sidebar-title i {
            margin-right: 0.5rem;
            font-size: 1.1em;
        }
        
        .sidebar-subtitle {
            font-size: 0.9rem;
            color: var(--neutral-600, #525252);
            line-height: 1.4;
        }
        
        .sidebar-section {
            border-top: 1px solid var(--neutral-200, #e5e5e5);
            padding-top: 1.5rem;
            margin-top: 1.5rem;
            position: relative;
        }
        
        .section-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--neutral-700, #404040);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }
        
        .section-title i {
            margin-right: 0.5rem;
            color: var(--primary-500, #6366f1);
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(to right, var(--primary-200, #c7d2fe), transparent);
        }
        
        /* 파일 업로더 스타일 */
        [data-testid="stFileUploader"] {
            margin-bottom: 1.5rem;
        }
        
        [data-testid="stFileUploader"] > div > div {
            padding: 1.5rem;
            border: 2px dashed var(--neutral-300, #d4d4d4);
            border-radius: 0.5rem;
            background-color: var(--neutral-50, #fafafa);
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"] > div > div:hover {
            border-color: var(--primary-400, #818cf8);
            background-color: var(--primary-50, #eef2ff);
        }
        
        /* 버튼 그룹 스타일 */
        .button-group {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }
        
        /* 데이터 미리보기 스타일 */
        .data-preview {
            padding: 0.75rem;
            border-radius: 0.375rem;
            background-color: var(--neutral-50, #fafafa);
            border: 1px solid var(--neutral-200, #e5e5e5);
            font-size: 0.85rem;
            max-height: 15rem;
            overflow-y: auto;
        }
        
        /* 선택기 래퍼 스타일 */
        .selector-wrapper {
            background-color: var(--neutral-50, #fafafa);
            border-radius: 0.375rem;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: 1px solid var(--neutral-200, #e5e5e5);
        }
        
        .selector-wrapper label {
            font-weight: 500;
            color: var(--neutral-700, #404040);
            margin-bottom: 0.25rem;
            display: block;
            font-size: 0.9rem;
        }
        
        /* 색상 미리보기 스타일 */
        .color-preview {
            display: flex;
            gap: 0.25rem;
            margin-top: 0.75rem;
        }
        
        .color-swatch {
            height: 1.5rem;
            flex-grow: 1;
            border-radius: 0.25rem;
            transition: all 0.3s ease;
        }
        
        .color-swatch:hover {
            transform: translateY(-2px);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        /* 팁 스타일 */
        .sidebar-tip {
            background-color: var(--primary-50, #eef2ff);
            border-left: 3px solid var(--primary-400, #818cf8);
            padding: 0.75rem;
            border-radius: 0.25rem;
            font-size: 0.85rem;
            margin: 1rem 0;
            color: var(--neutral-700, #404040);
        }
        
        .sidebar-tip i {
            color: var(--primary-500, #6366f1);
            margin-right: 0.375rem;
        }
        
        /* 푸터 스타일 */
        .sidebar-footer {
            font-size: 0.8rem;
            color: var(--neutral-500, #737373);
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--neutral-200, #e5e5e5);
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">
                <i class="fas fa-chart-bar"></i> TalentMetrics
            </div>
            <div class="sidebar-subtitle">
                채용 데이터를 시각화하고 핵심 인사이트를 발견하는 HR 대시보드 솔루션
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if df is None:
            st.markdown('<div class="section-title"><i class="fas fa-file-import"></i> 데이터 가져오기</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="sidebar-tip">
                <i class="fas fa-lightbulb"></i> Excel 파일을 업로드하거나 데모 데이터를 사용하여 시작하세요.
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "엑셀 파일 업로드",
                type=["xlsx", "xls"],
                help="채용 데이터가 포함된 엑셀 파일을 업로드하세요.",
                key="file_uploader"
            )
            
            config["uploaded_file"] = uploaded_file
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "데모 데이터 사용", 
                    help="샘플 데이터로 대시보드를 체험해보세요.", 
                    key="demo_btn",
                    use_container_width=True
                ):
                    config["use_demo"] = True
                    return config
            with col2:
                if st.button(
                    "초기화", 
                    help="모든 설정을 초기화합니다.", 
                    key="reset_btn",
                    use_container_width=True
                ):
                    st.experimental_rerun()
            
            st.markdown("""
            <div class="sidebar-tip">
                <i class="fas fa-info-circle"></i> 데모 데이터는 실제 HR 데이터 형식을 반영한 가상의 샘플입니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-title"><i class="fas fa-table"></i> 데이터 미리보기</div>', unsafe_allow_html=True)
            
            with st.expander("데이터 샘플", expanded=True):
                st.dataframe(df.head(3), use_container_width=True)
            
            st.markdown('<div class="section-title"><i class="fas fa-cog"></i> 데이터 설정</div>', unsafe_allow_html=True)
            
            suggested_cat_cols, suggested_val_cols = suggest_columns(df)
            all_columns = df.columns.tolist()
            
            cat_index = 0
            if suggested_cat_cols and suggested_cat_cols[0] in all_columns:
                cat_index = all_columns.index(suggested_cat_cols[0])
            
            st.markdown('<label>부서/카테고리 열 선택</label>', unsafe_allow_html=True)
            category_col = st.selectbox(
                "",
                all_columns,
                index=cat_index,
                key="category_col_select",
                help="그룹화할 카테고리 열을 선택하세요 (예: 부서, 지역 등)",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            config["category_col"] = category_col
            
            val_index = 0
            if suggested_val_cols and suggested_val_cols[0] in all_columns:
                val_index = all_columns.index(suggested_val_cols[0])
            
            st.markdown('<label>인원수/값 열 선택</label>', unsafe_allow_html=True)
            value_col = st.selectbox(
                "",
                all_columns,
                index=val_index,
                key="value_col_select",
                help="분석할 수치 데이터 열을 선택하세요 (예: 인원수, 예산 등)",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            config["value_col"] = value_col
            
            st.markdown('<div class="section-title"><i class="fas fa-sliders-h"></i> 추가 설정</div>', unsafe_allow_html=True)
            
            with st.expander("고급 옵션", expanded=False):
                st.markdown('<label>날짜 열 (선택사항)</label>', unsafe_allow_html=True)
                date_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="시간별 추세 분석을 위한 날짜 열",
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                config["date_col"] = date_col if date_col != "없음" else None
                
                st.markdown('<label>예산 열 (선택사항)</label>', unsafe_allow_html=True)
                budget_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="예산 분석을 위한 열",
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                config["budget_col"] = budget_col if budget_col != "없음" else None
                
                st.markdown('<label>성별 열 (선택사항)</label>', unsafe_allow_html=True)
                gender_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="성별 분석을 위한 열",
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                config["gender_col"] = gender_col if gender_col != "없음" else None
                
                st.markdown('<label>연령 열 (선택사항)</label>', unsafe_allow_html=True)
                age_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="연령대 분석을 위한 열",
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                config["age_col"] = age_col if age_col != "없음" else None
            
            st.markdown('<div class="section-title"><i class="fas fa-palette"></i> 시각화 스타일</div>', unsafe_allow_html=True)
            
            st.markdown('<label>테마 선택</label>', unsafe_allow_html=True)
            dashboard_style = st.selectbox(
                "",
                ["모던 블루", "다크 테마", "미니멀리스트", "HR 특화"],
                index=0,
                key="dashboard_style_select",
                help="대시보드의 색상과 스타일 테마",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            config["dashboard_style"] = dashboard_style
            
            # 색상 미리보기
            if dashboard_style == "모던 블루":
                colors = ["#eef2ff", "#c7d2fe", "#818cf8", "#4f46e5", "#3730a3"]
                theme_desc = "청량감 있는 블루 톤으로 전문적인 느낌의 테마입니다."
            elif dashboard_style == "다크 테마":
                colors = ["#1e1b4b", "#312e81", "#4338ca", "#6366f1", "#818cf8"]
                theme_desc = "어두운 배경에 밝은 색상 포인트의 고급스러운 테마입니다."
            elif dashboard_style == "미니멀리스트":
                colors = ["#f9fafb", "#f3f4f6", "#e5e7eb", "#9ca3af", "#6b7280"]
                theme_desc = "심플하고 깔끔한 그레이 톤의 미니멀 테마입니다."
            elif dashboard_style == "HR 특화":
                colors = ["#ecfdf5", "#a7f3d0", "#6ee7b7", "#10b981", "#065f46"]
                theme_desc = "HR에 어울리는 친근한 그린 계열의 테마입니다."
            
            st.markdown(f"""
            <div class="color-preview">
                <div class="color-swatch" style="background-color: {colors[0]};"></div>
                <div class="color-swatch" style="background-color: {colors[1]};"></div>
                <div class="color-swatch" style="background-color: {colors[2]};"></div>
                <div class="color-swatch" style="background-color: {colors[3]};"></div>
                <div class="color-swatch" style="background-color: {colors[4]};"></div>
            </div>
            <p style="font-size: 0.8rem; color: var(--neutral-600); margin-top: 0.5rem;">{theme_desc}</p>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
            st.caption(f"마지막 업데이트: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 내보내기 버튼
            st.download_button(
                label="설정 내보내기",
                data=str(config),
                file_name="talent_metrics_config.txt",
                mime="text/plain",
                help="현재 대시보드 설정을 저장합니다",
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    return config