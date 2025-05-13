import plotly.graph_objects as go
import streamlit as st

def create_heatmap(df, category_col, value_col, color_scheme):
    if df is None or df.empty:
        return None
    try:
        categories = df[category_col].tolist()
        values = df[value_col].tolist()
        min_val = min(values)
        max_val = max(values)
        if isinstance(color_scheme, list) and len(color_scheme) >= 3:
            colorscale = [[0, color_scheme[0]], [0.5, color_scheme[len(color_scheme)//2]], [1, color_scheme[-1]]]
        else:
            colorscale = [[0, "#e0f2fe"], [0.5, "#3b82f6"], [1, "#1e40af"]]
        fig = go.Figure(go.Heatmap(
            z=[values],
            x=categories,
            colorscale=colorscale,
            zmin=min_val,
            zmax=max_val,
            showscale=True,
            text=[[f"{v:,.0f}" for v in values]],
            texttemplate="%{text}",
            textfont=dict(size=12, color='#1f2937')
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=80),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=12, color='#6b7280')
            ),
            coloraxis_colorbar=dict(
                title=dict(
                    text=value_col,
                    font=dict(size=12, color='#6b7280')
                ),
                tickfont=dict(size=12, color='#6b7280')
            )
        )
        return fig
    except Exception as e:
        st.error(f"히트맵 생성 중 오류 발생: {str(e)}")
        return None 