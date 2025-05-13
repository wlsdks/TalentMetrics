import plotly.graph_objects as go

def create_correlation_heatmap(df, numeric_columns):
    corr_matrix = df[numeric_columns].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    fig.update_layout(
        title="상관관계 분석",
        xaxis_title="변수",
        yaxis_title="변수"
    )
    return fig 