# 엑셀 파일을 로드하고 데이터를 처리하는 기능을 담당합니다:
import pandas as pd
import streamlit as st
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
import io
import random
from dummy.generate_demo_excel import generate_rich_demo_excel

def load_excel_file(uploaded_file):
    """
    업로드된 엑셀 파일을 로드하고 엑셀 객체와 시트 이름 목록을 반환합니다.
    """
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        return excel_file, sheet_names
    except Exception as e:
        st.error(f"엑셀 파일 로드 중 오류가 발생했습니다: {e}")
        return None, []

def read_sheet_data(excel_file, sheet_name):
    """
    선택한 시트의 데이터를 DataFrame으로 읽어옵니다.
    """
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        return df
    except Exception as e:
        st.error(f"시트 데이터 읽기 중 오류가 발생했습니다: {e}")
        return None

def suggest_columns(df):
    """
    데이터를 분석하여 적절한 카테고리 열과 값 열을 추천합니다.
    """
    if df is None or df.empty:
        return [], []
    
    # 숫자형 열과 문자열 열 구분
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 카디널리티(고유값 개수)가 낮은 열을 카테고리 열로 추천
    suggested_cat_cols = []
    for col in categorical_cols:
        if df[col].nunique() < len(df) * 0.5:  # 고유값이 전체 행의 50% 미만인 경우
            suggested_cat_cols.append(col)
    
    # 카테고리 열이 없으면 모든 문자열 열 사용
    if not suggested_cat_cols and categorical_cols:
        suggested_cat_cols = categorical_cols
    
    return suggested_cat_cols, numeric_cols

def process_data(df, category_col, value_col):
    """
    시각화를 위해 데이터를 처리합니다.
    """
    # 기본 검증
    if df is None or category_col is None or value_col is None:
        st.error("데이터 또는 선택한 열이 없습니다.")
        return None
    
    if category_col not in df.columns or value_col not in df.columns:
        st.error(f"선택한 열({category_col} 또는 {value_col})이 데이터프레임에 존재하지 않습니다.")
        return None
    
    # 카테고리 열과 값 열이 같은지 검증
    if category_col == value_col:
        st.error("카테고리 열과 값 열이 동일합니다. 서로 다른 열을 선택해주세요.")
        return None
    
    try:
        # 데이터 확인
        # st.info(f"열 정보: {category_col}(유형: {df[category_col].dtype}), {value_col}(유형: {df[value_col].dtype})")
        st.toast(f"열 정보: {category_col}(유형: {df[category_col].dtype}), {value_col}(유형: {df[value_col].dtype})", icon="ℹ️")
        
        # 오류 해결을 위한 방법 1: 데이터 직접 생성
        # 부서별 집계를 수동으로 수행
        categories = df[category_col].astype(str).unique()
        result_data = []
        
        for cat in categories:
            # 각 카테고리별로 값들을 필터링하고 합계 계산
            cat_values = df[df[category_col].astype(str) == cat][value_col]
            if not cat_values.empty:
                # 값이 숫자형인지 확인
                try:
                    sum_value = pd.to_numeric(cat_values, errors='coerce').sum()
                    result_data.append({
                        category_col: cat,
                        value_col: sum_value
                    })
                except:
                    # 숫자로 변환할 수 없는 경우 개수 사용
                    result_data.append({
                        category_col: cat,
                        value_col: len(cat_values)
                    })
        
        # 새 데이터프레임 생성
        result_df = pd.DataFrame(result_data)
        
        # 내림차순 정렬
        if not result_df.empty:
            result_df = result_df.sort_values(by=value_col, ascending=False)
        
        # st.success("데이터 처리 완료!")
        st.toast("데이터 처리 완료!", icon="✅")
        return result_df
        
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {str(e)}")
        st.write("카테고리 열 샘플:", df[category_col].head())
        st.write("값 열 샘플:", df[value_col].head())
        return None

def calculate_summary(df, value_col):
    """
    데이터의 요약 통계를 계산합니다.
    """
    if df is None or df.empty or value_col not in df.columns:
        return {
            "total_categories": 0,
            "total_value": 0,
            "avg_value": 0,
            "median_value": 0,
            "max_category": {},
            "min_category": {}
        }
    
    try:
        # 기본 통계 계산
        total_categories = len(df)
        
        # 값 열이 숫자형인지 확인
        if pd.api.types.is_numeric_dtype(df[value_col]):
            total_value = df[value_col].sum()
            avg_value = df[value_col].mean()
            median_value = df[value_col].median()
            
            # 최대/최소값 찾기
            max_idx = df[value_col].idxmax()
            min_idx = df[value_col].idxmin()
            
            max_category = df.loc[max_idx].to_dict()
            min_category = df.loc[min_idx].to_dict()
        else:
            # 숫자형이 아닌 경우 기본값 사용
            st.warning(f"{value_col} 열이 숫자형이 아니어서 통계를 계산할 수 없습니다.")
            total_value = 0
            avg_value = 0
            median_value = 0
            max_category = {}
            min_category = {}
        
        return {
            "total_categories": total_categories,
            "total_value": total_value,
            "avg_value": avg_value,
            "median_value": median_value,
            "max_category": max_category,
            "min_category": min_category
        }
    except Exception as e:
        st.error(f"요약 통계 계산 중 오류 발생: {str(e)}")
        return {
            "total_categories": total_categories if 'total_categories' in locals() else 0,
            "total_value": 0,
            "avg_value": 0,
            "median_value": 0,
            "max_category": {},
            "min_category": {}
        }

def generate_comparison_data(df, category_col, value_col, cat1, cat2):
    """
    두 카테고리 간의 비교 데이터를 생성합니다.
    """
    if df is None or df.empty:
        return {"error": "데이터가 없습니다"}
    
    try:
        # 해당 카테고리 찾기
        cat1_data = df[df[category_col] == cat1]
        cat2_data = df[df[category_col] == cat2]
        
        if cat1_data.empty or cat2_data.empty:
            return {"error": "선택한 카테고리를 찾을 수 없습니다"}
        
        cat1_value = cat1_data[value_col].values[0]
        cat2_value = cat2_data[value_col].values[0]
        
        # 차이와 비율 계산
        diff = cat1_value - cat2_value
        percent_diff = (diff / cat2_value) * 100 if cat2_value != 0 else 0
        
        # 평균과 비교
        avg_value = df[value_col].mean()
        cat1_vs_avg = ((cat1_value - avg_value) / avg_value) * 100 if avg_value != 0 else 0
        cat2_vs_avg = ((cat2_value - avg_value) / avg_value) * 100 if avg_value != 0 else 0
        
        return {
            "category1": {
                "name": cat1,
                "value": cat1_value,
                "vs_avg": cat1_vs_avg
            },
            "category2": {
                "name": cat2,
                "value": cat2_value,
                "vs_avg": cat2_vs_avg
            },
            "diff": diff,
            "percent_diff": percent_diff
        }
    except Exception as e:
        st.error(f"비교 데이터 생성 중 오류 발생: {str(e)}")
        return {"error": f"비교 데이터 생성 중 오류 발생: {str(e)}"}

def create_demo_data():
    """
    풍부한 HR 데모 데이터를 생성하여 BytesIO로 반환합니다.
    """
    return generate_rich_demo_excel()

def validate_data(df):
    """
    데이터프레임의 유효성을 검사합니다.
    
    Args:
        df (pd.DataFrame): 검사할 데이터프레임
        
    Returns:
        tuple: (is_valid, message)
            - is_valid (bool): 데이터가 유효한지 여부
            - message (str): 검증 결과 메시지
    """
    if df is None or df.empty:
        return False, "데이터가 비어있습니다."
    
    # 필수 열 확인
    required_columns = ['부서', '인원수']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"필수 열이 누락되었습니다: {', '.join(missing_columns)}"
    
    # 데이터 타입 검사
    if not pd.api.types.is_numeric_dtype(df['인원수']):
        return False, "'인원수' 열은 숫자형이어야 합니다."
    
    # 음수 값 검사
    if (df['인원수'] < 0).any():
        return False, "인원수에 음수 값이 포함되어 있습니다."
    
    # 결측치 검사
    missing_values = df.isnull().sum()
    if missing_values.any():
        return False, f"결측치가 있습니다:\n{missing_values[missing_values > 0]}"
    
    # 중복 행 검사
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        return False, f"중복된 행이 {duplicates}개 있습니다."
    
    return True, "데이터가 유효합니다."

def preprocess_data(df):
    """
    데이터 전처리를 수행합니다.
    """
    if df is None or df.empty:
        return None
    
    # 결측치 처리
    df = df.ffill().bfill()
    
    # 중복 제거
    df = df.drop_duplicates()
    
    # 문자열 데이터 정규화
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.lower()
    
    return df

def detect_outliers(df, column):
    """
    특정 열의 이상치를 감지합니다.
    """
    if not pd.api.types.is_numeric_dtype(df[column]):
        return []
    
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

def calculate_trends(df, date_col, value_col):
    """
    시계열 데이터의 추세를 계산합니다.
    """
    if date_col not in df.columns or value_col not in df.columns:
        return None
    
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        
        # 월별 추세
        monthly_trend = df.groupby(df[date_col].dt.to_period('M'))[value_col].mean()
        
        # 분기별 추세
        quarterly_trend = df.groupby(df[date_col].dt.to_period('Q'))[value_col].mean()
        
        # 연도별 추세
        yearly_trend = df.groupby(df[date_col].dt.to_period('Y'))[value_col].mean()
        
        return {
            'monthly': monthly_trend,
            'quarterly': quarterly_trend,
            'yearly': yearly_trend
        }
    except Exception as e:
        st.error(f"추세 계산 중 오류 발생: {str(e)}")
        return None