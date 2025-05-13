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
    
    # 완전히 새로운, 간결한 사이드바 스타일
    st.markdown("""
    <style>
        /* 사이드바 기본 스타일 */
        [data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        
        /* 파일 업로드 컨테이너 통합 스타일 */
        .sidebar-section-wrapper {
            padding: 0;
            box-sizing: border-box;
        }
        
        .file-upload-container {
            background-color: #f8fafc;
            border-radius: 0.5rem;
            border: 1.5px solid #cbd5e1;
            box-shadow: 0 2px 8px 0 rgba(0,0,0,0.04);
            padding: 1.25rem 1.25rem 0.5rem 1.25rem;
            margin: 0.5rem 0 0.5rem 0;
            box-sizing: border-box;
        }
        
        .file-upload-header {
            display: flex;
            align-items: center;
            font-size: 1rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 0.75rem;
            padding: 0;
        }
        
        .file-upload-header i {
            margin-right: 0.5rem;
            color: #4f46e5;
        }
        
        .file-upload-desc {
            font-size: 0.8rem;
            color: #64748b;
            margin-bottom: 0.75rem;
            line-height: 1.4;
            padding: 0;
        }
        
        /* 사이드바에서 파일 업로더의 스타일을 수정 */
        [data-testid="stFileUploader"] {
            margin: 0;
            width: 100%;
        }
        
        [data-testid="stFileUploader"] > div {
            padding: 0 1rem;
        }
        
        [data-testid="stFileUploader"] > div > div {
            padding: 1.5rem 0;
            border-width: 2px !important;
            border-style: solid !important;
            border-color: #64748b !important;
            border-radius: 0.375rem;
            background-color: rgba(241, 245, 249, 0.7);
            box-shadow: 0 0 0 2px #64748b33;
            transition: all 0.3s ease;
            margin-top: 0;
        }
        
        [data-testid="stFileUploader"] > div > div:hover {
            border-color: #818cf8;
            background-color: rgba(239, 246, 255, 0.7);
            transform: translateY(-2px);
        }
        
        [data-testid="stFileUploader"] p {
            margin-bottom: 0;
            font-size: 0.8rem;
            color: #64748b;
        }
        
        /* 버튼 컨테이너 스타일 */
        .button-container {
            display: flex;
            gap: 0.75rem;
            padding: 0;
            width: 100%;
        }
        
        /* 헤더 - 앱 타이틀 제거 */
        .new-sidebar-header {
            padding: 1.75rem 1rem 1.25rem;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
        }
        
        /* 섹션 */
        .new-sidebar-section {
            padding: 0;
            margin-bottom: 1.5rem;
        }
        
        .new-sidebar-section-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 1rem;
            padding: 0.5rem 1.25rem 0.5rem 1.25rem;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            background: #f4f6fa;
            border-radius: 0.375rem 0.375rem 0 0;
        }
        
        .new-sidebar-section-title i {
            color: #4f46e5;
            margin-right: 0.5rem;
            font-size: 0.9rem;
        }
        
        /* 정보 메시지 */
        .new-sidebar-info {
            background-color: #f1f5f9;
            border-radius: 0.375rem;
            padding: 0.75rem 1.25rem;
            margin-bottom: 1rem;
            font-size: 0.8rem;
            color: #334155;
            border: 1px solid #e2e8f0;
        }
        
        .new-sidebar-info i {
            color: #4f46e5;
            margin-right: 0.375rem;
        }
        
        /* 폼 스타일 */
        .new-form-field {
            margin-bottom: 1rem;
            padding: 0 1.25rem;
        }
        
        .new-form-label {
            font-size: 0.8rem;
            font-weight: 500;
            color: #475569;
            margin-bottom: 0.375rem;
            display: block;
        }
        
        /* 테마 프리뷰 */
        .new-theme-preview {
            display: flex;
            height: 0.375rem;
            border-radius: 0.375rem;
            overflow: hidden;
            margin: 0.75rem 0 0.75rem 1.25rem;
        }
        
        .new-theme-color {
            flex: 1;
        }
        
        .new-theme-caption {
            font-size: 0.75rem;
            color: #64748b;
            margin-bottom: 1.25rem;
            padding-left: 1.25rem;
        }
        
        /* 푸터 */
        .new-sidebar-footer {
            padding: 1rem 0;
            font-size: 0.75rem;
            color: #64748b;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            margin-top: 2rem;
        }
        
        /* 버튼 스타일 재정의 */
        div.stButton > button {
            width: 100%;
            border-radius: 0.375rem;
            font-weight: 500;
            letter-spacing: 0.01em;
        }
        
        div.stButton > button:first-child {
            background-color: #4f46e5;
            color: white;
        }
        
        div.stButton > button:first-child:hover {
            background-color: #4338ca;
        }
        
        div.stDownloadButton > button {
            width: 100%;
            border-radius: 0.375rem;
            font-weight: 500;
            letter-spacing: 0.01em;
            background-color: #4f46e5;
            color: white;
        }
        
        div.stDownloadButton > button:hover {
            background-color: #4338ca;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        if df is None:
            st.markdown("""
            <div class="file-upload-container">
                <div class="file-upload-header">
                    <i class="fas fa-file-excel"></i>
                    <span>데이터 입력</span>
                </div>
                <div class="file-upload-desc">
                    분석할 Excel 파일을 업로드하거나 데모 데이터를 사용하세요
                </div>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "",
                type=["xlsx", "xls"],
                help="HR 데이터가 포함된 Excel 파일을 업로드하세요",
                key="file_uploader",
                label_visibility="collapsed"
            )
            config["uploaded_file"] = uploaded_file

            st.markdown("""
            <div class="button-container">
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "데모 데이터",
                    help="샘플 데이터로 시작하기",
                    key="demo_btn",
                    use_container_width=True
                ):
                    config["use_demo"] = True
                    return config
            with col2:
                if st.button(
                    "초기화",
                    help="설정 초기화",
                    key="reset_btn",
                    use_container_width=True
                ):
                    st.experimental_rerun()
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="new-sidebar-section">
                <div class="new-sidebar-section-title">
                    <i class="fas fa-table"></i> 데이터 선택
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
            st.markdown('<div class="new-form-label">분석할 데이터 미리보기</div>', unsafe_allow_html=True)
            st.dataframe(df.head(3), use_container_width=True, height=120)
            st.markdown('</div>', unsafe_allow_html=True)

            suggested_cat_cols, suggested_val_cols = suggest_columns(df)
            all_columns = df.columns.tolist()

            cat_index = 0
            if suggested_cat_cols and suggested_cat_cols[0] in all_columns:
                cat_index = all_columns.index(suggested_cat_cols[0])
            st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
            st.markdown('<div class="new-form-label">분류 기준 열</div>', unsafe_allow_html=True)
            category_col = st.selectbox(
                "",
                all_columns,
                index=cat_index,
                key="category_col_select",
                help="데이터를 그룹화할 카테고리 열 (부서, 팀, 지역 등)",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            config["category_col"] = category_col

            val_index = 0
            if suggested_val_cols and suggested_val_cols[0] in all_columns:
                val_index = all_columns.index(suggested_val_cols[0])
            st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
            st.markdown('<div class="new-form-label">수치 데이터 열</div>', unsafe_allow_html=True)
            value_col = st.selectbox(
                "",
                all_columns,
                index=val_index,
                key="value_col_select",
                help="분석할 숫자 데이터가 포함된 열 (인원수, 예산 등)",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            config["value_col"] = value_col

            st.markdown("""
            <div class="new-sidebar-section">
                <div class="new-sidebar-section-title">
                    <i class="fas fa-cog"></i> 추가 설정
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("고급 설정", expanded=False):
                st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
                st.markdown('<div class="new-form-label">날짜 열 (선택사항)</div>', unsafe_allow_html=True)
                date_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="시간 기반 분석을 위한 날짜 열",
                    label_visibility="collapsed"
                )
                config["date_col"] = date_col if date_col != "없음" else None
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
                st.markdown('<div class="new-form-label">예산 열 (선택사항)</div>', unsafe_allow_html=True)
                budget_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="예산 분석을 위한 열",
                    label_visibility="collapsed"
                )
                config["budget_col"] = budget_col if budget_col != "없음" else None
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
                st.markdown('<div class="new-form-label">성별 열 (선택사항)</div>', unsafe_allow_html=True)
                gender_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="성별 분석을 위한 열",
                    label_visibility="collapsed"
                )
                config["gender_col"] = gender_col if gender_col != "없음" else None
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
                st.markdown('<div class="new-form-label">연령 열 (선택사항)</div>', unsafe_allow_html=True)
                age_col = st.selectbox(
                    "",
                    ["없음"] + all_columns,
                    index=0,
                    help="연령 분석을 위한 열",
                    label_visibility="collapsed"
                )
                config["age_col"] = age_col if age_col != "없음" else None
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="new-form-field">', unsafe_allow_html=True)
            st.markdown('<div class="new-form-label">시각화 테마</div>', unsafe_allow_html=True)
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

            if dashboard_style == "모던 블루":
                colors = ["#eef2ff", "#c7d2fe", "#818cf8", "#4f46e5", "#3730a3"]
                theme_desc = "깔끔한 블루 기반의 전문적인 테마"
            elif dashboard_style == "다크 테마":
                colors = ["#1e1b4b", "#312e81", "#4338ca", "#6366f1", "#818cf8"]
                theme_desc = "어두운 배경의 고급스러운 테마"
            elif dashboard_style == "미니멀리스트":
                colors = ["#f9fafb", "#f3f4f6", "#e5e7eb", "#9ca3af", "#6b7280"]
                theme_desc = "심플한 그레이 계열의 미니멀 테마"
            elif dashboard_style == "HR 특화":
                colors = ["#ecfdf5", "#a7f3d0", "#6ee7b7", "#10b981", "#065f46"]
                theme_desc = "HR에 어울리는 그린 계열 테마"
            st.markdown(f"""
            <div class="new-theme-preview">
                <div class="new-theme-color" style="background-color: {colors[0]};"></div>
                <div class="new-theme-color" style="background-color: {colors[1]};"></div>
                <div class="new-theme-color" style="background-color: {colors[2]};"></div>
                <div class="new-theme-color" style="background-color: {colors[3]};"></div>
                <div class="new-theme-color" style="background-color: {colors[4]};"></div>
            </div>
            <div class="new-theme-caption">{theme_desc}</div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="설정 내보내기",
                data=str(config),
                file_name="talent_metrics_config.txt",
                mime="text/plain",
                help="현재 대시보드 설정을 파일로 저장합니다",
                use_container_width=True
            )
            st.markdown(f"""
            <div class="new-sidebar-footer">
                TalentMetrics v2.0 • {datetime.datetime.now().strftime('%Y-%m-%d')}
            </div>
            """, unsafe_allow_html=True)
    return config