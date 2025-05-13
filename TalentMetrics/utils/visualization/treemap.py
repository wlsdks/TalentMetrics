import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def create_treemap(df, category_col, value_col, color_scheme, title=""):
    if df is None or df.empty:
        return None
    try:
        chart_df = df.copy()
        chart_df[category_col] = chart_df[category_col].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Treemap(
            labels=chart_df[category_col].tolist(),
            values=chart_df[value_col].tolist(),
            parents=[""] * len(chart_df),
            marker=dict(
                colors=chart_df[value_col].tolist(),
                colorscale="Blues",
                line=dict(width=0)
            ),
            textinfo="label+value+percent parent",
            textfont=dict(size=12, color='#1f2937')
        ))
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
            title=dict(
                font=dict(size=20, color='#1f2937'),
                x=0.5,
                y=0.95
            )
        )
        return fig
    except Exception as e:
        st.error(f"트리맵 생성 중 오류 발생: {str(e)}")
        return None 