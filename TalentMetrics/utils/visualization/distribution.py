import plotly.graph_objects as go
import numpy as np
import streamlit as st

def create_distribution_chart(df, column, bins=30):
    try:
        mean_val = df[column].mean()
        median_val = df[column].median()
        std_val = df[column].std()
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[column],
            name='히스토그램',
            nbinsx=bins,
            opacity=0.7,
            histnorm='probability density'
        ))
        kde_x = np.linspace(df[column].min(), df[column].max(), 100)
        kde_y = df[column].plot.kde().get_lines()[0].get_ydata()
        fig.add_trace(go.Scatter(
            x=kde_x,
            y=kde_y,
            name='커널 밀도',
            line=dict(width=2)
        ))
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="red",
            annotation_text="평균",
            annotation_position="top right"
        )
        fig.add_vline(
            x=median_val,
            line_dash="dash",
            line_color="green",
            annotation_text="중앙값",
            annotation_position="top left"
        )
        fig.update_layout(
            title=f"{column} 분포",
            xaxis_title=column,
            yaxis_title="밀도",
            showlegend=True,
            height=400,
            annotations=[
                dict(
                    x=0.02,
                    y=0.98,
                    xref="paper",
                    yref="paper",
                    text=f"평균: {mean_val:.2f}<br>중앙값: {median_val:.2f}<br>표준편차: {std_val:.2f}",
                    showarrow=False,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="black",
                    borderwidth=1,
                    borderpad=4
                )
            ]
        )
        return fig
    except Exception as e:
        st.error(f"분포 차트 생성 중 오류 발생: {str(e)}")
        return None 