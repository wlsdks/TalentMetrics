import plotly.express as px
import streamlit as st
import pandas as pd

def create_comparison_chart(data, category_col, value_col, color_scheme):
    if "error" in data:
        return None
    try:
        compare_df = pd.DataFrame({
            category_col: [data["category1"]["name"], data["category2"]["name"]],
            value_col: [data["category1"]["value"], data["category2"]["value"]]
        })
        colors = [color_scheme[1], color_scheme[5]] if isinstance(color_scheme, list) and len(color_scheme) > 5 else ["#2563eb", "#1d4ed8"]
        fig = px.bar(
            compare_df,
            x=category_col,
            y=value_col,
            color=category_col,
            text=value_col,
            color_discrete_sequence=colors
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
            showlegend=False,
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
            )
        )
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside',
            marker=dict(
                line=dict(width=0)
            )
        )
        return fig
    except Exception as e:
        st.error(f"비교 차트 생성 중 오류 발생: {str(e)}")
        return None 