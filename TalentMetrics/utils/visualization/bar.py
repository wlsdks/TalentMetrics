import plotly.express as px
import streamlit as st

def create_bar_chart(df, category_col, value_col, color_scheme, title=""):
    if df is None or df.empty:
        return None
    fig = px.bar(
        df,
        x=category_col,
        y=value_col,
        color=value_col,
        color_continuous_scale=color_scheme,
        template="plotly_white",
        title=title
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
        title=dict(
            font=dict(size=20, color='#1f2937'),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=12, color='#6b7280')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False,
            tickfont=dict(size=12, color='#6b7280')
        ),
        bargap=0.15
    )
    fig.update_traces(
        selector=dict(type='bar'),
        texttemplate='%{y:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br><span style="color:#2563eb;font-weight:bold;">%{y:,.0f}</span><extra></extra>'
    )
    return fig 