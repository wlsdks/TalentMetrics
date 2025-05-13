import plotly.graph_objects as go

def create_outlier_chart(df, column, outliers):
    fig = go.Figure()
    normal_data = df[~df.index.isin(outliers.index)]
    fig.add_trace(go.Scatter(
        x=normal_data.index,
        y=normal_data[column],
        mode='markers',
        name='정상 데이터',
        marker=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=outliers.index,
        y=outliers[column],
        mode='markers',
        name='이상치',
        marker=dict(
            color='red',
            size=10,
            symbol='x'
        )
    ))
    fig.update_layout(
        title=f"{column} 이상치 분석",
        xaxis_title="인덱스",
        yaxis_title=column,
        hovermode="closest"
    )
    return fig 