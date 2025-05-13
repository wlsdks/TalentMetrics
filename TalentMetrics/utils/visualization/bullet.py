import plotly.graph_objects as go
import streamlit as st

def create_bullet_chart(df, category_col, value_col, avg_value, color_scheme):
    if df is None or df.empty:
        return None, False
    try:
        if len(df) > 15:
            chart_df = df.head(15)
            is_truncated = True
        else:
            chart_df = df
            is_truncated = False
        fig = go.Figure()
        for i, (_, row) in enumerate(chart_df.iterrows()):
            category = row[category_col]
            value = row[value_col]
            color_idx = i % len(color_scheme) if isinstance(color_scheme, list) else 0
            bar_color = color_scheme[color_idx] if isinstance(color_scheme, list) else "#2563eb"
            fig.add_trace(go.Bar(
                y=[category],
                x=[value],
                orientation='h',
                name=category,
                marker=dict(
                    color=bar_color,
                    line=dict(width=0)
                ),
                showlegend=False
            ))
        fig.add_trace(go.Scatter(
            y=chart_df[category_col],
            x=[avg_value] * len(chart_df),
            mode='markers',
            name='평균',
            marker=dict(
                symbol='line-ns',
                color='rgba(0, 0, 0, 0.7)',
                line=dict(width=2),
                size=10
            )
        ))
        fig.update_layout(
            height=max(350, len(chart_df) * 30),
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False,
                tickfont=dict(size=12, color='#6b7280')
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                tickfont=dict(size=12, color='#6b7280')
            )
        )
        return fig, is_truncated
    except Exception as e:
        st.error(f"불릿 차트 생성 중 오류 발생: {str(e)}")
        return None, False 