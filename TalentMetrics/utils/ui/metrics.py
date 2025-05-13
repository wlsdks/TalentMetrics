import streamlit as st
import plotly.graph_objects as go
import time

def render_metrics(summary, category_col, value_col):
    if not summary:
        return
        
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-users"></i>
            </div>
            <div class="metric-title">총 {value_col}</div>
            <div class="metric-value animated-number">{summary.get("total_value", 0):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
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
        <div class="metric-card">
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
        <div class="metric-card">
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
    
    st.markdown('<div class="dashboard-card" style="padding: 20px;">', unsafe_allow_html=True)
    
    # 헤더 섹션
    st.markdown("""
    <div class="metric-section-header">
        <div class="metric-section-icon">
            <i class="fas fa-chart-pie"></i>
        </div>
        <div class="metric-section-title">
            <h2>HR 핵심 지표</h2>
            <p>현재 인력 현황과 중요 지표를 한눈에 파악하세요</p>
        </div>
    </div>
    
    <style>
        .metric-section-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--neutral-200);
        }
        
        .metric-section-icon {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: var(--shadow-md);
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
        
        .metric-icon {
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-bottom: 0.75rem;
        }
        
        .metric-label {
            font-size: 0.85rem;
            color: var(--neutral-500);
            margin-top: 0.25rem;
        }
        
        /* 반응형 */
        @media screen and (max-width: 768px) {
            .metric-section-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 주요 메트릭 카드
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-users"></i>
            </div>
            <div class="metric-title">총 인력</div>
            <div class="metric-value animated-number">{hr_metrics.get('total_headcount', 0):,}명</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-user-check"></i>
            </div>
            <div class="metric-title">평균 인력</div>
            <div class="metric-value animated-number">{hr_metrics.get('avg_headcount', 0):.1f}명</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if 'total_budget' in hr_metrics:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">
                    <i class="fas fa-money-bill-wave"></i>
                </div>
                <div class="metric-title">총 예산</div>
                <div class="metric-value animated-number">{hr_metrics['total_budget']:,}원</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">
                    <i class="fas fa-money-bill-wave"></i>
                </div>
                <div class="metric-title">총 예산</div>
                <div class="metric-value animated-number">-</div>
                <div class="metric-label">데이터 없음</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if 'yearly_growth_rates' in hr_metrics:
            latest_growth = list(hr_metrics['yearly_growth_rates'].values())[-1]
            growth_icon = "fa-arrow-up" if latest_growth > 0 else "fa-arrow-down"
            growth_color = "var(--success-color)" if latest_growth > 0 else "var(--danger-color)"
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="metric-title">연간 성장률</div>
                <div class="metric-value animated-number" style="color: {growth_color};">
                    <i class="fas {growth_icon}"></i> {latest_growth:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="metric-title">연간 성장률</div>
                <div class="metric-value animated-number">-</div>
                <div class="metric-label">데이터 없음</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 차트 섹션
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    if 'gender_distribution' in hr_metrics:
        st.markdown("""
        <div class="chart-section-header">
            <i class="fas fa-venus-mars"></i> 성별 분포
        </div>
        
        <style>
            .chart-section-header {
                font-size: 1.2rem;
                font-weight: 600;
                color: var(--neutral-700);
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid var(--neutral-200);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
        </style>
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
    
    if 'age_distribution' in hr_metrics:
        st.markdown("""
        <div class="chart-section-header">
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
                line=dict(color='rgba(79, 70, 229, 1.0)', width=1)
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
    
    if 'department_distribution' in hr_metrics:
        st.markdown("""
        <div class="chart-section-header">
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
                colorscale='Blues',
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
                family="Noto Sans KR, sans-serif",
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
    
    st.markdown('</div>', unsafe_allow_html=True)