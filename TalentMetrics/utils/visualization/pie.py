import plotly.express as px
import streamlit as st

def create_pie_chart(df, category_col, value_col, color_scheme, title=""):
    if df is None or df.empty:
        return None
    if len(df) < 2:
        st.warning("파이 차트를 그리기 위한 데이터가 충분하지 않습니다.")
        return None
    try:
        fig = px.pie(
            df,
            names=category_col,
            values=value_col,
            color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None,
            hole=0.6,
            title=title
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
            title=dict(
                text=title,
                font=dict(size=20, color='#1f2937'),
                x=0.5,
                y=0.95
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color='#6b7280')
            )
        )
        fig.update_traces(
            selector=dict(type='pie'),
            textposition='inside',
            insidetextorientation='radial',
            textinfo='label+percent',
            textfont=dict(size=14, color='#1f2937', family="Pretendard, -apple-system, system-ui"),
            marker=dict(line=dict(color='white', width=2)),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} (%{percent})<extra></extra>'
        )
        return fig
    except Exception as e:
        st.error(f"파이 차트 생성 중 오류 발생: {str(e)}")
        return None 