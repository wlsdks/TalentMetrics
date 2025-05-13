import plotly.express as px
import streamlit as st

def create_bar_chart(df, category_col, value_col, color_scheme, title=""):
    if df is None or df.empty:
        return None
    
    # 상위 15개 항목만 표시 (데이터가 많을 경우)
    display_df = df.head(15) if len(df) > 15 else df
    
    is_gradient = not isinstance(color_scheme, list)
    
    fig = px.bar(
        display_df,
        x=category_col,
        y=value_col,
        color=value_col if is_gradient else None,
        color_continuous_scale=color_scheme if is_gradient else None,
        color_discrete_sequence=color_scheme if not is_gradient else None,
        template="plotly_white",
        title=title
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=80),
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Noto Sans KR, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"),
        title=dict(
            font=dict(size=18, color='#1f2937'),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=12, color='#6b7280'),
            tickangle=-30
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False,
            tickfont=dict(size=12, color='#6b7280')
        ),
        bargap=0.15,
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Noto Sans KR, sans-serif"
        )
    )
    
    fig.update_traces(
        selector=dict(type='bar'),
        texttemplate='%{y:,.0f}',
        textposition='auto',
        textfont=dict(
            size=10,
            family="Noto Sans KR, sans-serif",
            color="#4b5563"
        ),
        insidetextanchor='middle',
        cliponaxis=True,
        constraintext='both',
        hovertemplate='<b>%{x}</b><br><span style="color:#2563eb;font-weight:bold;">%{y:,.0f}</span><extra></extra>',
        marker=dict(
            line=dict(width=1, color='rgba(255, 255, 255, 0.8)'),
            opacity=0.9
        )
    )
    
    # 데이터가 많은 경우 안내 메시지
    annotation_msg = None
    
    # 그라데이션 효과를 위한 설정
    if is_gradient:
        max_value = display_df[value_col].max()
        min_value = display_df[value_col].min()
        normalized_values = [(val - min_value) / (max_value - min_value) if max_value > min_value else 0.5 for val in display_df[value_col]]
        
        # 커스텀 색상 설정
        fig.update_traces(
            marker_color=normalized_values,
            marker_colorscale=color_scheme
        )
    
    # Streamlit에서 안내 메시지 출력
    if annotation_msg:
        st.caption(annotation_msg)
    
    return fig