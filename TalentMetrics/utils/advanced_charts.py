# 고급 차트와 시각화 함수를 정의합니다:
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st

def create_sunburst_chart(df, category_col, value_col, second_level_col=None, color_scheme=None):
    """
    선버스트 차트를 생성합니다. 계층 구조를 표현할 때 유용합니다.
    두 번째 레벨 열이 없으면 단일 레벨로 표현합니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 두 번째 레벨이 없으면 가상의 루트 노드 생성
        if second_level_col is None or second_level_col not in df.columns:
            # 단일 레벨 선버스트
            fig = px.sunburst(
                df,
                names=category_col,
                values=value_col,
                color=value_col,
                color_continuous_scale=color_scheme if not isinstance(color_scheme, list) else 'Blues',
            )
        else:
            # 두 레벨 선버스트
            fig = px.sunburst(
                df,
                path=[second_level_col, category_col],  # 계층 구조 지정
                values=value_col,
                color=value_col,
                color_continuous_scale=color_scheme if not isinstance(color_scheme, list) else 'Blues',
            )
        
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_showscale=False
        )
        
        return fig
    except Exception as e:
        st.error(f"선버스트 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_radar_chart(df, category_col, metrics_cols, color_scheme=None):
    """
    레이더 차트를 생성합니다. 여러 측정값을 다각적으로 비교할 때 유용합니다.
    metrics_cols은 비교할 측정값 열 이름의 리스트입니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 최대 5개 카테고리만 선택 (너무 많으면 가독성이 떨어짐)
        top_categories = df[category_col].unique()[:5]
        filtered_df = df[df[category_col].isin(top_categories)]
        
        # 각 카테고리별로 데이터 정규화 (0~1 사이)
        normalized_df = pd.DataFrame()
        
        for col in metrics_cols:
            if col in df.columns:
                max_val = df[col].max()
                min_val = df[col].min()
                if max_val > min_val:
                    normalized_df[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    normalized_df[col] = df[col] / max_val if max_val > 0 else df[col]
        
        # 레이더 차트 생성
        fig = go.Figure()
        
        for i, category in enumerate(top_categories):
            category_data = normalized_df[filtered_df[category_col] == category]
            
            if not category_data.empty:
                values = [category_data[col].iloc[0] for col in metrics_cols if col in category_data.columns]
                
                # 그래프에서 첫 번째 값을 마지막에 다시 추가하여 폐곘된 도형 생성
                values.append(values[0])
                labels = metrics_cols + [metrics_cols[0]]
                
                # 색상 설정
                if isinstance(color_scheme, list) and len(color_scheme) > i:
                    line_color = color_scheme[i]
                else:
                    line_color = None  # 기본 색상 사용
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=labels,
                    fill='toself',
                    name=category,
                    line=dict(color=line_color)
                ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.error(f"레이더 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_bubble_chart(df, x_col, y_col, size_col, category_col, color_scheme=None):
    """
    버블 차트를 생성합니다. 세 가지 변수(x, y, 크기)를 동시에 시각화할 때 유용합니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 모든 필요한 열이 있는지 확인
        if not all(col in df.columns for col in [x_col, y_col, size_col, category_col]):
            missing_cols = [col for col in [x_col, y_col, size_col, category_col] if col not in df.columns]
            st.warning(f"버블 차트에 필요한 열이 없습니다: {', '.join(missing_cols)}")
            return None
        
        # 버블 차트 생성
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            size=size_col,
            color=category_col,
            hover_name=category_col,
            color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None,
            size_max=50,  # 최대 버블 크기
            opacity=0.7
        )
        
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title=x_col,
            yaxis_title=y_col
        )
        
        # 버블 크기를 설명하는 텍스트 추가
        fig.update_layout(
            annotations=[
                dict(
                    x=0.99,
                    y=0.01,
                    xref="paper",
                    yref="paper",
                    text=f"버블 크기: {size_col}",
                    showarrow=False,
                    font=dict(size=10),
                    bgcolor="rgba(255, 255, 255, 0.5)",
                    bordercolor="gray",
                    borderwidth=1
                )
            ]
        )
        
        return fig
    except Exception as e:
        st.error(f"버블 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_timeline_chart(df, date_col, value_col, category_col=None, color_scheme=None):
    """
    타임라인 차트를 생성합니다. 시간에 따른 추세를 보여줄 때 유용합니다.
    category_col이 제공되면 카테고리별로 선을 그립니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 날짜 열이 있는지 확인
        if date_col not in df.columns:
            st.warning(f"타임라인 차트에 필요한 날짜 열({date_col})이 없습니다.")
            return None
        
        # 날짜 형식 변환 (문자열이면 날짜로 변환)
        chart_df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(chart_df[date_col]):
            try:
                chart_df[date_col] = pd.to_datetime(chart_df[date_col])
            except:
                # 변환 실패 시 문자열 그대로 사용
                pass
        
        # 타임라인 차트 생성
        if category_col and category_col in df.columns:
            # 카테고리별 타임라인
            fig = px.line(
                chart_df,
                x=date_col,
                y=value_col,
                color=category_col,
                markers=True,
                color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None
            )
        else:
            # 단일 타임라인
            fig = px.line(
                chart_df,
                x=date_col,
                y=value_col,
                markers=True,
                color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None
            )
            
            # 영역 채우기 추가
            fig.add_trace(
                px.area(
                    chart_df, 
                    x=date_col, 
                    y=value_col
                ).data[0]
            )
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="기간",
            yaxis_title=value_col
        )
        
        return fig
    except Exception as e:
        st.error(f"타임라인 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_boxplot(df, category_col, value_col, color_scheme=None):
    """
    상자 그림(Box Plot)을 생성합니다. 데이터 분포를 비교할 때 유용합니다.
    """
    if df is None or df.empty:
        return None
    
    try:
        # 필요한 열이 있는지 확인
        if not all(col in df.columns for col in [category_col, value_col]):
            missing_cols = [col for col in [category_col, value_col] if col not in df.columns]
            st.warning(f"상자 그림에 필요한 열이 없습니다: {', '.join(missing_cols)}")
            return None
        
        # 상자 그림 생성
        fig = px.box(
            df,
            x=category_col,
            y=value_col,
            color=category_col,
            color_discrete_sequence=color_scheme if isinstance(color_scheme, list) else None,
            points="all"  # 모든 데이터 포인트 표시
        )
        
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title=category_col,
            yaxis_title=value_col,
            showlegend=False
        )
        
        return fig
    except Exception as e:
        st.error(f"상자 그림 생성 중 오류 발생: {str(e)}")
        return None

def create_sankey_diagram(df, source_col, target_col, value_col, color_scheme=None):
    """
    생키 다이어그램을 생성합니다. 흐름과 관계를 시각화할 때 유용합니다.
    예: 부서 간 이동, 채용 경로 등
    """
    if df is None or df.empty:
        return None
    
    try:
        # 필요한 열이 있는지 확인
        if not all(col in df.columns for col in [source_col, target_col, value_col]):
            missing_cols = [col for col in [source_col, target_col, value_col] if col not in df.columns]
            st.warning(f"생키 다이어그램에 필요한 열이 없습니다: {', '.join(missing_cols)}")
            return None
        
        # 모든 고유 노드(source와 target의 합집합) 찾기
        all_nodes = pd.concat([df[source_col], df[target_col]]).unique()
        
        # 노드에 인덱스 할당
        node_indices = {node: i for i, node in enumerate(all_nodes)}
        
        # 생키 다이어그램 데이터 준비
        sources = [node_indices[source] for source in df[source_col]]
        targets = [node_indices[target] for target in df[target_col]]
        values = df[value_col].tolist()
        
        # 색상 생성
        if isinstance(color_scheme, list):
            node_colors = color_scheme[:len(all_nodes)] if len(color_scheme) >= len(all_nodes) else color_scheme * (len(all_nodes) // len(color_scheme) + 1)
            node_colors = node_colors[:len(all_nodes)]
        else:
            # 기본 색상 사용
            node_colors = ['rgba(31, 119, 180, 0.8)'] * len(all_nodes)
        
        # 생키 다이어그램 생성
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=node_colors
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color='rgba(100, 100, 100, 0.2)'
            )
        )])
        
        fig.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=30, b=20),
            font=dict(size=12)
        )
        
        return fig
    except Exception as e:
        st.error(f"생키 다이어그램 생성 중 오류 발생: {str(e)}")
        return None

def create_gauge_chart(value, min_val, max_val, title="", color_scheme=None):
    """
    게이지 차트를 생성합니다. KPI 또는 목표 달성도를 보여줄 때 유용합니다.
    """
    try:
        # 진행률 계산 (0-1 사이 값)
        if max_val > min_val:
            progress = (value - min_val) / (max_val - min_val)
        else:
            progress = 0.5  # 기본값
        
        # 진행률이 0-1 범위를 벗어나면 조정
        progress = max(0, min(1, progress))
        
        # 색상 설정
        if isinstance(color_scheme, list) and len(color_scheme) >= 3:
            color = color_scheme[1]  # 중간 색상 사용
        else:
            # 진행률에 따른 색상 결정
            if progress < 0.3:
                color = "red"
            elif progress < 0.7:
                color = "orange"
            else:
                color = "green"
        
        # 게이지 차트 생성
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [min_val, max_val]},
                "bar": {"color": color},
                "steps": [
                    {"range": [min_val, min_val + (max_val - min_val) * 0.3], "color": "lightgray"},
                    {"range": [min_val + (max_val - min_val) * 0.3, min_val + (max_val - min_val) * 0.7], "color": "gray"}
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": max_val * 0.8
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        return fig
    except Exception as e:
        st.error(f"게이지 차트 생성 중 오류 발생: {str(e)}")
        return None

def create_wordcloud(df, text_col, weight_col=None, max_words=100, color_scheme=None):
    """
    워드 클라우드를 생성합니다. 텍스트 데이터에서 단어 빈도를 시각화할 때 유용합니다.
    """
    try:
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud
        import io
        
        if df is None or df.empty or text_col not in df.columns:
            return None
        
        # 텍스트 데이터 결합
        all_text = ' '.join(df[text_col].astype(str).fillna('').tolist())
        
        # 가중치가 있는 경우 단어별 가중치 계산
        if weight_col and weight_col in df.columns:
            # 단어별 가중치 계산
            word_weights = {}
            for i, row in df.iterrows():
                words = str(row[text_col]).split()
                for word in words:
                    if word in word_weights:
                        word_weights[word] += row[weight_col]
                    else:
                        word_weights[word] = row[weight_col]
            
            # 워드 클라우드 생성
            wc = WordCloud(
                width=800, 
                height=400, 
                max_words=max_words, 
                background_color='white'
            ).generate_from_frequencies(word_weights)
        else:
            # 단순 텍스트 기반 워드 클라우드
            wc = WordCloud(
                width=800, 
                height=400, 
                max_words=max_words, 
                background_color='white'
            ).generate(all_text)
        
        # 이미지 저장
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        
        # 이미지를 바이트로 변환
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        
        return buf
    except Exception as e:
        st.error(f"워드 클라우드 생성 중 오류 발생: {str(e)}")
        return None

def create_calendar_heatmap(df, date_col, value_col, color_scheme=None):
    """
    캘린더 히트맵을 생성합니다. 날짜별 값을 시각화할 때 유용합니다.
    """
    try:
        import matplotlib.pyplot as plt
        import calmap
        import io
        
        if df is None or df.empty or not all(col in df.columns for col in [date_col, value_col]):
            return None
        
        # 날짜 데이터 확인 및 변환
        chart_df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(chart_df[date_col]):
            try:
                chart_df[date_col] = pd.to_datetime(chart_df[date_col])
            except:
                st.warning("날짜 데이터를 변환할 수 없습니다.")
                return None
        
        # 날짜별 데이터로 변환
        date_series = chart_df.set_index(date_col)[value_col]
        
        # 연도 확인
        years = date_series.index.year.unique()
        
        # 모든 연도에 대한 캘린더 맵 생성
        fig, axes = plt.subplots(len(years), 1, figsize=(10, 2 * len(years)))
        
        if len(years) == 1:
            axes = [axes]
        
        for i, year in enumerate(sorted(years)):
            calmap.yearplot(date_series, year=year, ax=axes[i], cmap='Blues')
            axes[i].set_title(f"{year}년")
        
        fig.tight_layout()
        
        # 이미지를 바이트로 변환
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        
        return buf
    except Exception as e:
        st.error(f"캘린더 히트맵 생성 중 오류 발생: {str(e)}")
        return None