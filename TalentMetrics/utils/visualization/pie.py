import plotly.express as px
import streamlit as st

def create_pie_chart(df, category_col, value_col, color_scheme, title=""):
    if df is None or df.empty:
        return None
    
    if len(df) < 2:
        st.warning("파이 차트를 그리기 위한 데이터가 충분하지 않습니다.")
        return None
    
    try:
        # 상위 10개 항목만 표시 (데이터가 많을 경우)
        display_df = df.head(10) if len(df) > 10 else df
        
        # 차트 생성
        fig = px.pie(
            display_df,
            names=category_col,
            values=value_col,
            color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None,
            hole=0.6,
            title=title
        )
        
        # 레이아웃 설정
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Noto Sans KR, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
            title=dict(
                text=title,
                font=dict(size=18, color='#1f2937'),
                x=0.5,
                y=0.95
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color='#6b7280'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.1)',
                borderwidth=1
            ),
            annotations=[
                dict(
                    text="부서별<br>비율",
                    x=0.5,
                    y=0.5,
                    font=dict(
                        size=14, 
                        color='#4f46e5',
                        family="Noto Sans KR, sans-serif"
                    ),
                    showarrow=False
                )
            ]
        )
        
        # 트레이스 스타일 설정
        fig.update_traces(
            selector=dict(type='pie'),
            textposition='inside',
            insidetextorientation='radial',
            textinfo='label+percent',
            textfont=dict(
                size=13, 
                color='#1f2937', 
                family="Noto Sans KR, sans-serif"
            ),
            marker=dict(
                line=dict(color='white', width=2),
                pattern=dict(shape="")
            ),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} (%{percent})<extra></extra>',
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Noto Sans KR, sans-serif"
            )
        )
        
        # 데이터가 많은 경우 안내 메시지
        if len(df) > 10:
            fig.add_annotation(
                x=0.5,
                y=-0.3,
                xref="paper",
                yref="paper",
                text=f"* 상위 10개 {category_col}만 표시됩니다 (전체 {len(df)}개 중).",
                showarrow=False,
                font=dict(size=12, color="#6b7280"),
                align="center"
            )
        
        return fig
    except Exception as e:
        st.error(f"파이 차트 생성 중 오류 발생: {str(e)}")
        return None