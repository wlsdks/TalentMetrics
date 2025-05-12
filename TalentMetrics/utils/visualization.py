# 다양한 차트와 시각화 함수를 정의합니다:
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np
from scipy.stats import gaussian_kde

def get_color_scheme(style):
    """
    선택한 스타일에 따른 색상 스키마를 반환합니다.
    """
    if style == "다크 테마":
        return px.colors.sequential.Plasma, "#121212", "white"
    elif style == "모던 블루":
        return px.colors.sequential.Blues, "#f8f9fa", "#0f52ba"
    elif style == "미니멀리스트":
        return px.colors.sequential.Greys, "white", "#333333"
    elif style == "HR 특화":
        return px.colors.sequential.Teal, "#f0f8ff", "#006064"
    else:  # 기본 대시보드
        return px.colors.qualitative.Plotly, "white", "#333333"

def create_bar_chart(df, category_col, value_col, color_scheme, title=""):
    """
    막대 차트를 생성합니다.
    """
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
        coloraxis_showscale=False
    )
    
    # 바 위에 값 표시
    fig.update_traces(
        texttemplate='%{y}',
        textposition='outside'
    )
    
    return fig

def create_pie_chart(df, category_col, value_col, color_scheme, title=""):
    """
    파이 차트를 생성합니다.
    """
    if df is None or df.empty:
        return None
    
    # 데이터가 충분한지 확인
    if len(df) < 2:
        st.warning("파이 차트를 그리기 위한 데이터가 충분하지 않습니다.")
        return None
    
    try:
        fig = px.pie(
            df,
            names=category_col,
            values=value_col,
            color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None,
            hole=0.4,
            title=title
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        return fig
    except Exception as e:
        st.error(f"파이 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_treemap(df, category_col, value_col, color_scheme, title=""):
    """
    트리맵 차트를 생성합니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 데이터 확인 및 디버깅
        st.write("트리맵 데이터 확인:", df.head(2))
        st.write(f"카테고리 열: {category_col}, 값 열: {value_col}")
        
        # 데이터 복사 및 타입 변환
        chart_df = df.copy()
        chart_df[category_col] = chart_df[category_col].astype(str)
        
        # go.Treemap을 사용하여 직접 트리맵 생성
        fig = go.Figure()
        
        fig.add_trace(go.Treemap(
            labels=chart_df[category_col].tolist(),
            values=chart_df[value_col].tolist(),
            parents=[""] * len(chart_df),  # 모든 항목이 루트에 직접 연결
            marker=dict(
                colors=chart_df[value_col].tolist(),
                colorscale="Blues"
            ),
            textinfo="label+value"
        ))
        
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            title=title
        )
        
        return fig
    except Exception as e:
        st.error(f"트리맵 생성 중 오류 발생: {str(e)}")
        # 오류 발생 시 간단한 막대 차트로 대체
        try:
            simple_fig = px.bar(
                df,
                x=category_col,
                y=value_col,
                title=title + " (트리맵 생성 실패, 막대 차트로 대체)"
            )
            return simple_fig
        except:
            return None

def create_comparison_chart(data, category_col, value_col, color_scheme):
    """
    두 카테고리 비교 차트를 생성합니다.
    """
    if "error" in data:
        return None
    
    try:
        # 비교 데이터 준비
        compare_df = pd.DataFrame({
            category_col: [data["category1"]["name"], data["category2"]["name"]],
            value_col: [data["category1"]["value"], data["category2"]["value"]]
        })
        
        colors = [color_scheme[1], color_scheme[5]] if isinstance(color_scheme, list) and len(color_scheme) > 5 else ["blue", "orange"]
        
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
            showlegend=False
        )
        
        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside'
        )
        
        return fig
    except Exception as e:
        st.error(f"비교 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_bullet_chart(df, category_col, value_col, avg_value, color_scheme):
    """
    불릿 차트를 생성합니다 (평균 대비 각 카테고리 성과).
    """
    if df is None or df.empty:
        return None, False
    
    try:
        # 데이터프레임이 너무 크면 상위 N개만 사용
        if len(df) > 15:
            chart_df = df.head(15)
            is_truncated = True
        else:
            chart_df = df
            is_truncated = False
        
        fig = go.Figure()
        
        # 각 카테고리에 대한 바
        for i, (_, row) in enumerate(chart_df.iterrows()):
            category = row[category_col]
            value = row[value_col]
            
            color_idx = i % len(color_scheme) if isinstance(color_scheme, list) else 0
            bar_color = color_scheme[color_idx] if isinstance(color_scheme, list) else "blue"
            
            fig.add_trace(go.Bar(
                y=[category],
                x=[value],
                orientation='h',
                name=category,
                marker=dict(color=bar_color),
                showlegend=False
            ))
        
        # 평균선
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
            height=max(350, len(chart_df) * 30),  # 데이터 수에 따라 높이 조정
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title=value_col,
            yaxis_title=category_col
        )
        
        return fig, is_truncated
    except Exception as e:
        st.error(f"불릿 차트 생성 중 오류 발생: {str(e)}")
        return None, False

def create_heatmap(df, category_col, value_col, color_scheme):
    """
    히트맵을 생성합니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 데이터 준비
        categories = df[category_col].tolist()
        values = df[value_col].tolist()
        
        # 값 범위 계산
        min_val = min(values)
        max_val = max(values)
        
        # 컬러맵 생성
        if isinstance(color_scheme, list) and len(color_scheme) >= 3:
            colorscale = [[0, color_scheme[0]], [0.5, color_scheme[len(color_scheme)//2]], [1, color_scheme[-1]]]
        else:
            colorscale = [[0, "lightblue"], [0.5, "blue"], [1, "darkblue"]]
        
        fig = go.Figure(go.Heatmap(
            z=[values],
            x=categories,
            colorscale=colorscale,
            zmin=min_val,
            zmax=max_val,
            showscale=True
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=80),
            xaxis=dict(tickangle=-45)
        )
        
        return fig
    except Exception as e:
        st.error(f"히트맵 생성 중 오류 발생: {str(e)}")
        return None

def create_trend_chart(trend_data, title="추세 분석"):
    """
    시계열 추세를 시각화합니다.
    """
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

def create_outlier_chart(df, column, outliers):
    """
    이상치를 시각화합니다.
    """
    fig = go.Figure()
    
    # 정상 데이터
    normal_data = df[~df.index.isin(outliers.index)]
    fig.add_trace(go.Scatter(
        x=normal_data.index,
        y=normal_data[column],
        mode='markers',
        name='정상 데이터',
        marker=dict(color='blue')
    ))
    
    # 이상치
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

def create_correlation_heatmap(df, numeric_columns):
    """
    수치형 열들 간의 상관관계를 히트맵으로 시각화합니다.
    """
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

def create_distribution_chart(df, column, bins=30):
    """
    데이터의 분포를 시각화하는 히스토그램과 커널 밀도 추정을 생성합니다.
    
    Args:
        df (pd.DataFrame): 데이터프레임
        column (str): 분포를 시각화할 열 이름
        bins (int): 히스토그램의 구간 수
        
    Returns:
        plotly.graph_objects.Figure: 분포 차트
    """
    try:
        # 기본 통계량 계산
        mean_val = df[column].mean()
        median_val = df[column].median()
        std_val = df[column].std()
        
        # 히스토그램과 커널 밀도 추정 생성
        fig = go.Figure()
        
        # 히스토그램 추가
        fig.add_trace(go.Histogram(
            x=df[column],
            name='히스토그램',
            nbinsx=bins,
            opacity=0.7,
            histnorm='probability density'
        ))
        
        # 커널 밀도 추정 추가
        kde_x = np.linspace(df[column].min(), df[column].max(), 100)
        kde_y = df[column].plot.kde().get_lines()[0].get_ydata()
        
        fig.add_trace(go.Scatter(
            x=kde_x,
            y=kde_y,
            name='커널 밀도',
            line=dict(width=2)
        ))
        
        # 평균선 추가
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="red",
            annotation_text="평균",
            annotation_position="top right"
        )
        
        # 중앙값선 추가
        fig.add_vline(
            x=median_val,
            line_dash="dash",
            line_color="green",
            annotation_text="중앙값",
            annotation_position="top left"
        )
        
        # 레이아웃 설정
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