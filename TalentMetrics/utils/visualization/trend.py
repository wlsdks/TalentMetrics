import plotly.graph_objects as go

def create_trend_chart(trend_data, title="추세 분석"):
    fig = go.Figure()
    if trend_data:
        for period, data in trend_data.items():
            fig.add_trace(go.Scatter(
                x=data.index.astype(str),
                y=data.values,
                name=period,
                mode='lines+markers'
            ))
    fig.update_layout(
        title=title,
        xaxis_title="기간",
        yaxis_title="값",
        hovermode="x unified"
    )
    return fig 