import streamlit as st
import plotly.graph_objects as go
import time

def render_metrics(summary, category_col, value_col):
    if not summary:
        return
        
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card staggered-item">
            <div class="metric-icon">
                <i class="fas fa-users"></i>
            </div>
            <div class="metric-title">총 {value_col}</div>
            <div class="metric-value animated-number">{summary.get("total_value", 0):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card staggered-item">
            <div class="metric-icon">
                <i class="fas fa-calculator"></i>
            </div>
            <div class="metric-title">평균 {value_col}</div>
            <div class="metric-value animated-number">{summary.get("avg_value", 0):,.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        max_category = summary.get("max_category", {})
        max_value = max_category.get(value_col, 0) if isinstance(max_category, dict) else 0
        max_name = max_category.get(category_col, "N/A") if isinstance(max_category, dict) else "N/A"
        
        st.markdown(f"""
        <div class="metric-card staggered-item">
            <div class="metric-icon">
                <i class="fas fa-arrow-up"></i>
            </div>
            <div class="metric-title">최대 {value_col}</div>
            <div class="metric-value animated-number">{max_value:,}</div>
            <div class="metric-label">{max_name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        min_category = summary.get("min_category", {})
        min_value = min_category.get(value_col, 0) if isinstance(min_category, dict) else 0
        min_name = min_category.get(category_col, "N/A") if isinstance(min_category, dict) else "N/A"
        
        st.markdown(f"""
        <div class="metric-card staggered-item">
            <div class="metric-icon">
                <i class="fas fa-arrow-down"></i>
            </div>
            <div class="metric-title">최소 {value_col}</div>
            <div class="metric-value animated-number">{min_value:,}</div>
            <div class="metric-label">{min_name}</div>
        </div>
        """, unsafe_allow_html=True)

def render_hr_metrics_dashboard(summary, hr_metrics):
    message_placeholder = st.empty()
    message_placeholder.info("데이터 처리 중...")
    time.sleep(0.5)
    message_placeholder.empty()
    
    # 전체 스타일 한번에 적용
    st.markdown("""
    <style>
        .metric-section {
            background-color: white;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 2rem;
            border: 1px solid var(--neutral-200);
            animation: fadeIn 0.6s ease-out;
        }
        
        .metric-section-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--neutral-200);
        }
        
        .metric-section-icon {
            background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
            color: white;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .metric-section-title h2 {
            margin: 0;
            padding: 0;
            font-size: 1.5rem;
            color: var(--neutral-800);
            font-weight: 600;
        }
        
        .metric-section-title p {
            margin: 0;
            padding: 0;
            font-size: 0.9rem;
            color: var(--neutral-500);
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metric-card-emphasis {
            background-color: white;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--neutral-200);
            transition: all 0.3s ease;
            position: relative;
            display: flex;
            align-items: center;
            overflow: hidden;
        }
        
        .metric-card-emphasis:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card-emphasis::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary-400), var(--primary-600));
        }
        
        .metric-card-icon {
            width: 3.5rem;
            height: 3.5rem;
            background: linear-gradient(135deg, var(--primary-50), var(--primary-100));
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 1.25rem;
            font-size: 1.5rem;
            color: var(--primary-600);
            flex-shrink: 0;
        }
        
        .metric-card-content {
            flex-grow: 1;
        }
        
        .metric-card-title {
            font-size: 0.875rem;
            color: var(--neutral-500);
            margin-bottom: 0.25rem;
        }
        
        .metric-card-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--neutral-900);
            margin-bottom: 0.375rem;
            line-height: 1.2;
        }
        
        .metric-card-trend {
            font-size: 0.875rem;
            display: flex;
            align-items: center;
        }
        
        .metric-grid-header {
            grid-column: 1 / -1;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--neutral-700);
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--neutral-200);
            display: flex;
            align-items: center;
        }
        
        .metric-grid-header i {
            margin-right: 0.5rem;
            color: var(--primary-500);
        }
        
        /* 반응형 */
        @media screen and (max-width: 768px) {
            .metric-section-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .metric-card-emphasis {
                flex-direction: column;
                text-align: center;
                padding: 1.25rem;
            }
            
            .metric-card-emphasis::before {
                width: 100%;
                height: 4px;
                top: 0;
                left: 0;
                background: linear-gradient(to right, var(--primary-400), var(--primary-600));
            }
            
            .metric-card-icon {
                margin-right: 0;
                margin-bottom: 1rem;
            }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .animate-pulse {
            animation: pulse 3s infinite ease-in-out;
        }
        
        .animate-fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        .animate-slide-in {
            animation: slideIn 0.6s ease-out;
        }
        
        .metric-grid > div:nth-child(1) { animation-delay: 0.1s; }
        .metric-grid > div:nth-child(2) { animation-delay: 0.2s; }
        .metric-grid > div:nth-child(3) { animation-delay: 0.3s; }
        .metric-grid > div:nth-child(4) { animation-delay: 0.4s; }
    </style>
    """, unsafe_allow_html=True)
    
    # 헤더 섹션
    st.markdown("""
    <div class="metric-section">
        <div class="metric-section-header">
            <div class="metric-section-icon">
                <i class="fas fa-chart-pie"></i>
            </div>
            <div class="metric-section-title">
                <h2>HR 핵심 지표</h2>
                <p>현재 인력 현황과 중요 지표를 한눈에 파악하세요</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 메트릭 카드들을 컬럼으로 배치
    col1, col2, col3, col4 = st.columns(4)
    
    # 총 인력
    with col1:
        st.markdown(f"""
        <div class="metric-card-emphasis animate-fade-in">
            <div class="metric-card-icon">
                <i class="fas fa-users"></i>
            </div>
            <div class="metric-card-content">
                <div class="metric-card-title">총 인력</div>
                <div class="metric-card-value">{hr_metrics.get('total_headcount', 0):,}명</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 평균 인력
    with col2:
        st.markdown(f"""
        <div class="metric-card-emphasis animate-fade-in">
            <div class="metric-card-icon">
                <i class="fas fa-user-check"></i>
            </div>
            <div class="metric-card-content">
                <div class="metric-card-title">평균 인력</div>
                <div class="metric-card-value">{hr_metrics.get('avg_headcount', 0):.1f}명</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 총 예산
    with col3:
        if 'total_budget' in hr_metrics:
            st.markdown(f"""
            <div class="metric-card-emphasis animate-fade-in">
                <div class="metric-card-icon">
                    <i class="fas fa-money-bill-wave"></i>
                </div>
                <div class="metric-card-content">
                    <div class="metric-card-title">총 예산</div>
                    <div class="metric-card-value">{hr_metrics['total_budget']:,}원</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card-emphasis animate-fade-in">
                <div class="metric-card-icon">
                    <i class="fas fa-money-bill-wave"></i>
                </div>
                <div class="metric-card-content">
                    <div class="metric-card-title">총 예산</div>
                    <div class="metric-card-value">-</div>
                    <div class="metric-card-trend" style="color: var(--neutral-500);">데이터 없음</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 연간 성장률
    with col4:
        if 'yearly_growth_rates' in hr_metrics:
            latest_growth = list(hr_metrics['yearly_growth_rates'].values())[-1]
            growth_icon = "fa-arrow-up" if latest_growth > 0 else "fa-arrow-down"
            growth_color = "var(--success-500)" if latest_growth > 0 else "var(--danger-500)"
            st.markdown(f"""
            <div class="metric-card-emphasis animate-fade-in">
                <div class="metric-card-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="metric-card-content">
                    <div class="metric-card-title">연간 성장률</div>
                    <div class="metric-card-value" style="color: {growth_color};">
                        {latest_growth:.1f}%
                    </div>
                    <div class="metric-card-trend" style="color: {growth_color};">
                        <i class="fas {growth_icon}"></i> 작년 대비
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card-emphasis animate-fade-in">
                <div class="metric-card-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="metric-card-content">
                    <div class="metric-card-title">연간 성장률</div>
                    <div class="metric-card-value">-</div>
                    <div class="metric-card-trend" style="color: var(--neutral-500);">데이터 없음</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 차트 섹션 - 성별 분포
    if 'gender_distribution' in hr_metrics:
        st.markdown("""
        <div class="metric-grid-header animate-fade-in">
            <i class="fas fa-venus-mars"></i> 성별 분포
        </div>
        """, unsafe_allow_html=True)
        
        gender_data = hr_metrics['gender_distribution']
        
        fig = go.Figure(data=[go.Pie(
            labels=list(gender_data.keys()),
            values=list(gender_data.values()),
            hole=.6,
            marker=dict(
                colors=['#4f46e5', '#f43f5e'],
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=14)
        )])
        
        fig.update_layout(
            title="",
            showlegend=True,
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            annotations=[dict(
                text='성별 분포',
                x=0.5, y=0.5,
                font=dict(size=16, color='#4f46e5'),
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 차트 섹션 - 연령대 분포
    if 'age_distribution' in hr_metrics:
        st.markdown("""
        <div class="metric-grid-header animate-fade-in">
            <i class="fas fa-users"></i> 연령대 분포
        </div>
        """, unsafe_allow_html=True)
        
        age_data = hr_metrics['age_distribution']
        
        fig = go.Figure(data=[go.Bar(
            x=list(age_data.keys()),
            y=list(age_data.values()),
            text=[f"{v:.1f}%" for v in age_data.values()],
            textposition='auto',
            marker=dict(
                color='rgba(79, 70, 229, 0.8)',
                line=dict(color='rgba(79, 70, 229, 1.0)', width=1),
                colorscale='Bluyl',
                showscale=False
            )
        )])
        
        fig.update_layout(
            title="",
            xaxis_title="연령대",
            yaxis_title="비율 (%)",
            height=300,
            template="plotly_white",
            margin=dict(t=0, b=40, l=40, r=20),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=12)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 차트 섹션 - 부서별 분포
    if 'department_distribution' in hr_metrics:
        st.markdown("""
        <div class="metric-grid-header animate-fade-in">
            <i class="fas fa-building"></i> 부서별 분포
        </div>
        """, unsafe_allow_html=True)
        
        dept_data = hr_metrics['department_distribution']
        
        # 상위 10개 부서만 표시 (많은 경우)
        dept_items = list(dept_data['sum'].items())
        dept_items.sort(key=lambda x: x[1], reverse=True)
        
        if len(dept_items) > 10:
            top_depts = dict(dept_items[:10])
            others_sum = sum([item[1] for item in dept_items[10:]])
            top_depts['기타 부서'] = others_sum
            chart_data = top_depts
        else:
            chart_data = dict(dept_items)
        
        fig = go.Figure(data=[go.Bar(
            x=list(chart_data.keys()),
            y=list(chart_data.values()),
            text=[f"{v:,.0f}명" for v in chart_data.values()],
            textposition='auto',
            marker=dict(
                color='rgba(79, 70, 229, 0.8)',
                line=dict(color='rgba(79, 70, 229, 1.0)', width=1),
                colorscale='Bluyl',
                showscale=False
            )
        )])
        
        fig.update_layout(
            title="",
            xaxis_title="부서",
            yaxis_title="인원수",
            height=400,
            template="plotly_white",
            font=dict(
                family="Pretendard, Noto Sans KR, sans-serif",
                size=12,
                color="#6b7280"
            ),
            margin=dict(l=40, r=40, t=0, b=80),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=12)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)