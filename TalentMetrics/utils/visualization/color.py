import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional, Union

def get_color_scheme(style: str) -> Tuple[Union[List[str], str], str, str]:
    """
    스타일 이름에 따라 적절한 색상 스킴을 반환합니다.
    
    Args:
        style (str): 대시보드 스타일 이름
        
    Returns:
        Tuple[Union[List[str], str], str, str]: 
            - 색상 스킴 (리스트 또는 문자열)
            - 배경색
            - 텍스트 색상
    """
    if style == "다크 테마":
        return [
            "#9089fc", "#818cf8", "#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#312e81"
        ], "#1a1a2e", "#e2e8f0"
    elif style == "모던 블루":
        return [
            "#dbeafe", "#bfdbfe", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"
        ], "#f1f5f9", "#1e293b"
    elif style == "미니멀리스트":
        return [
            "#f9fafb", "#f3f4f6", "#e5e7eb", "#d1d5db", "#9ca3af", "#6b7280", "#4b5563"
        ], "#ffffff", "#111827"
    elif style == "HR 특화":
        return [
            "#ccfbf1", "#99f6e4", "#5eead4", "#2dd4bf", "#14b8a6", "#0d9488", "#0f766e"
        ], "#ecfeff", "#134e4a"
    else:
        # 기본 색상 스킴
        return [
            "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a"
        ], "#ffffff", "#1f2937"