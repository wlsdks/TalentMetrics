import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

def calculate_hr_metrics(df, category_col=None, headcount_col=None, budget_col=None, 
                        date_col=None, gender_col=None, age_col=None):
    """
    HR 관련 주요 지표들을 계산합니다.
    """
    metrics = {}
    
    try:
        # 기본 인력 지표
        if headcount_col and headcount_col in df.columns:
            metrics['total_headcount'] = df[headcount_col].sum()
            metrics['avg_headcount'] = df[headcount_col].mean()
            metrics['max_headcount'] = df[headcount_col].max()
            metrics['min_headcount'] = df[headcount_col].min()
        
        # 부서별 인력 분포
        if category_col and headcount_col:
            dept_distribution = df.groupby(category_col)[headcount_col].agg(['sum', 'mean', 'count'])
            metrics['department_distribution'] = dept_distribution.to_dict()
        
        # 성별 분포
        if gender_col and headcount_col:
            gender_dist = df.groupby(gender_col)[headcount_col].sum()
            total = gender_dist.sum()
            gender_ratio = (gender_dist / total * 100).round(2)
            metrics['gender_distribution'] = gender_ratio.to_dict()
        
        # 연령대 분포
        if age_col and headcount_col:
            # 연령대 구분
            df['age_group'] = pd.cut(df[age_col], 
                                   bins=[0, 20, 30, 40, 50, 60, 100],
                                   labels=['20대 이하', '20대', '30대', '40대', '50대', '60대 이상'])
            age_dist = df.groupby('age_group')[headcount_col].sum()
            total = age_dist.sum()
            age_ratio = (age_dist / total * 100).round(2)
            metrics['age_distribution'] = age_ratio.to_dict()
        
        # 예산 관련 지표
        if budget_col and headcount_col:
            # 인당 비용
            df['cost_per_head'] = df[budget_col] / df[headcount_col]
            metrics['avg_cost_per_head'] = df['cost_per_head'].mean()
            metrics['total_budget'] = df[budget_col].sum()
            
            # 부서별 예산 효율성
            if category_col:
                dept_efficiency = df.groupby(category_col).agg({
                    budget_col: 'sum',
                    headcount_col: 'sum'
                })
                dept_efficiency['cost_per_head'] = dept_efficiency[budget_col] / dept_efficiency[headcount_col]
                metrics['department_efficiency'] = dept_efficiency.to_dict()
        
        # 시계열 분석
        if date_col and headcount_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                
                # 월별 추세
                monthly_trend = df.groupby(df[date_col].dt.to_period('M'))[headcount_col].sum()
                metrics['monthly_trend'] = monthly_trend.to_dict()
                
                # 분기별 추세
                quarterly_trend = df.groupby(df[date_col].dt.to_period('Q'))[headcount_col].sum()
                metrics['quarterly_trend'] = quarterly_trend.to_dict()
                
                # 연도별 추세
                yearly_trend = df.groupby(df[date_col].dt.to_period('Y'))[headcount_col].sum()
                metrics['yearly_trend'] = yearly_trend.to_dict()
                
                # 성장률 계산
                if len(yearly_trend) > 1:
                    growth_rates = yearly_trend.pct_change() * 100
                    metrics['yearly_growth_rates'] = growth_rates.to_dict()
            except Exception as e:
                st.warning(f"시계열 분석 중 오류 발생: {str(e)}")
        
        # 다양성 지표
        if gender_col and age_col:
            # 성별-연령대 교차 분석
            diversity_matrix = pd.crosstab(df[gender_col], df['age_group'], values=df[headcount_col], aggfunc='sum')
            metrics['diversity_matrix'] = diversity_matrix.to_dict()
        
        return metrics
    
    except Exception as e:
        st.error(f"HR 지표 계산 중 오류 발생: {str(e)}")
        return {}

def calculate_turnover_rate(df, date_col, headcount_col, category_col=None):
    """
    이직률을 계산합니다.
    """
    try:
        if date_col not in df.columns or headcount_col not in df.columns:
            return None
        
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 전체 이직률
        total_turnover = df.groupby(df[date_col].dt.to_period('M'))[headcount_col].sum()
        avg_headcount = total_turnover.mean()
        
        # 부서별 이직률
        if category_col:
            dept_turnover = df.groupby([category_col, df[date_col].dt.to_period('M')])[headcount_col].sum()
            dept_avg = dept_turnover.groupby(category_col).mean()
            
            return {
                'total_turnover_rate': (total_turnover / avg_headcount * 100).round(2).to_dict(),
                'department_turnover_rates': (dept_turnover / dept_avg * 100).round(2).to_dict()
            }
        
        return {
            'total_turnover_rate': (total_turnover / avg_headcount * 100).round(2).to_dict()
        }
    
    except Exception as e:
        st.error(f"이직률 계산 중 오류 발생: {str(e)}")
        return None

def calculate_workforce_planning(df, headcount_col, budget_col=None, category_col=None):
    """
    인력 계획 관련 지표를 계산합니다.
    """
    try:
        metrics = {}
        
        # 현재 인력 수준
        current_headcount = df[headcount_col].sum()
        metrics['current_headcount'] = current_headcount
        
        # 부서별 인력 계획
        if category_col:
            dept_planning = df.groupby(category_col)[headcount_col].agg(['sum', 'mean', 'std'])
            metrics['department_planning'] = dept_planning.to_dict()
        
        # 예산 기반 인력 계획
        if budget_col:
            avg_cost_per_head = df[budget_col].sum() / current_headcount
            metrics['avg_cost_per_head'] = avg_cost_per_head
            
            # 부서별 예산 효율성
            if category_col:
                dept_efficiency = df.groupby(category_col).agg({
                    budget_col: 'sum',
                    headcount_col: 'sum'
                })
                dept_efficiency['cost_per_head'] = dept_efficiency[budget_col] / dept_efficiency[headcount_col]
                metrics['department_efficiency'] = dept_efficiency.to_dict()
        
        return metrics
    
    except Exception as e:
        st.error(f"인력 계획 지표 계산 중 오류 발생: {str(e)}")
        return {}
