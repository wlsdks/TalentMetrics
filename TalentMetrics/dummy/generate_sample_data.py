# 샘플 데이터 생성을 위한 파일 -> python generate_sample_data.py 명령어 실행하기 -> 실행되면 프로젝트 폴더에 hr_sample_data.xlsx 파일 생성됨
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 엑셀 파일 생성을 위한 함수
def generate_hr_sample_data():
    """HR 채용 샘플 데이터를 생성하고 엑셀 파일로 저장합니다."""
    
    # 시드 설정 (동일한 결과를 얻기 위함)
    np.random.seed(42)
    random.seed(42)
    
    # 1. 부서별 채용 현황 데이터
    departments = [
        '개발팀', '마케팅', '영업', '인사팀', '고객지원', 'IT지원', 
        '디자인', '연구개발', '재무', '법무', '운영', '제품관리',
        '프로젝트관리', '품질관리', '경영지원', '전략기획'
    ]
    
    # 인원수 생성 (평균 10, 표준편차 5의 정규분포 기반)
    headcounts = np.round(np.maximum(1, np.random.normal(10, 5, len(departments)))).astype(int)
    
    # 예산 데이터 생성 (인원수 * 평균 연봉 + 랜덤 변동)
    avg_salary = 5000  # 가정된 평균 연봉 (단위: 만원)
    budgets = headcounts * avg_salary * (0.9 + 0.2 * np.random.random(len(departments)))
    budgets = np.round(budgets, -1)  # 10만원 단위로 반올림
    
    # 부서별 채용율 (예산 대비 실제 사용 비율)
    hiring_rates = np.round(np.random.uniform(0.7, 1.2, len(departments)), 2)
    
    # 1. 부서별 채용 현황 데이터프레임 생성
    df_departments = pd.DataFrame({
        '부서': departments,
        '인원수': headcounts,
        '채용예산(만원)': budgets,
        '채용율': hiring_rates
    })
    
    # 2. 직무별 채용 현황 데이터
    roles = [
        '백엔드개발자', '프론트엔드개발자', '데이터분석가', '데이터엔지니어',
        'HR매니저', '마케팅전문가', '디자이너', '영업담당자', '고객서비스담당자',
        '품질관리자', '제품관리자', '프로젝트매니저', '연구원', '재무분석가',
        '법무담당자', '전략기획자', '운영담당자', 'DevOps엔지니어', 'QA엔지니어',
        '시스템관리자'
    ]
    
    # 직무별 인원 및 예산 데이터 생성
    role_headcounts = np.round(np.maximum(1, np.random.normal(5, 3, len(roles)))).astype(int)
    role_budgets = role_headcounts * (avg_salary * 0.8 + avg_salary * 0.4 * np.random.random(len(roles)))
    role_budgets = np.round(role_budgets, -1)  # 10만원 단위로 반올림
    
    # 2. 직무별 채용 현황 데이터프레임 생성
    df_roles = pd.DataFrame({
        '직무': roles,
        '채용인원': role_headcounts,
        '직무별예산(만원)': role_budgets
    })
    
    # 3. 월별 채용 추이 데이터 생성
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    monthly_hires = np.round(np.maximum(5, 20 + 10 * np.sin(np.arange(12) * np.pi / 6) + np.random.normal(0, 3, 12))).astype(int)
    
    df_monthly = pd.DataFrame({
        '월': [d.strftime('%Y-%m') for d in months],
        '채용인원': monthly_hires
    })
    
    # 4. 지역별 채용 현황 데이터
    locations = [
        '서울', '부산', '인천', '대구', '광주', '대전', 
        '울산', '세종', '경기', '강원', '충북', '충남',
        '전북', '전남', '경북', '경남', '제주'
    ]
    
    location_hires = np.round(np.maximum(1, np.random.normal(8, 6, len(locations)))).astype(int)
    
    df_locations = pd.DataFrame({
        '지역': locations,
        '채용인원': location_hires
    })
    
    # 5. 상세 채용 데이터 (개인별 데이터)
    # 샘플 데이터 크기
    n_samples = 100
    
    # 이름 생성 (가상 데이터)
    first_names = [
        '민준', '서연', '도윤', '서현', '예준', '지우', '하준', '하은', '주원', '민서',
        '지호', '지민', '지윤', '준서', '유준', '예은', '건우', '지아', '현우', '서윤',
        '유진', '승민', '수빈', '예린', '준영', '수민', '지원', '하윤', '유빈', '재원'
    ]
    
    last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '신', '서', '권', '황', '안', '송', '전', '홍']
    
    # 랜덤 이름 생성
    names = [f'{random.choice(last_names)}{random.choice(first_names)}' for _ in range(n_samples)]
    
    # 날짜 생성 (최근 180일 동안의 랜덤 날짜)
    today = datetime.now()
    hire_dates = [today - timedelta(days=random.randint(1, 180)) for _ in range(n_samples)]
    hire_dates = [d.strftime('%Y-%m-%d') for d in hire_dates]
    
    # 부서, 직무, 지역 랜덤 할당
    emp_departments = [random.choice(departments) for _ in range(n_samples)]
    emp_roles = [random.choice(roles) for _ in range(n_samples)]
    emp_locations = [random.choice(locations) for _ in range(n_samples)]
    
    # 연봉 생성 (4000만원 ~ 6000만원 사이의 랜덤값)
    salaries = np.round(np.random.uniform(4000, 6000, n_samples), -1)
    
    # 성별 생성
    genders = np.random.choice(['남', '여'], n_samples)
    
    # 연령대 생성
    age_groups = np.random.choice(['20대', '30대', '40대', '50대'], n_samples, p=[0.3, 0.4, 0.2, 0.1])
    
    # 개인별 상세 데이터 생성
    df_employees = pd.DataFrame({
        '이름': names,
        '입사일': hire_dates,
        '부서': emp_departments,
        '직무': emp_roles,
        '지역': emp_locations,
        '연봉(만원)': salaries,
        '성별': genders,
        '연령대': age_groups
    })
    
    # 엑셀 파일 생성
    with pd.ExcelWriter('hr_sample_data.xlsx') as writer:
        df_departments.to_excel(writer, sheet_name='부서별채용현황', index=False)
        df_roles.to_excel(writer, sheet_name='직무별채용현황', index=False)
        df_monthly.to_excel(writer, sheet_name='월별채용추이', index=False)
        df_locations.to_excel(writer, sheet_name='지역별채용현황', index=False)
        df_employees.to_excel(writer, sheet_name='채용상세데이터', index=False)
    
    print("샘플 HR 데이터가 'hr_sample_data.xlsx' 파일로 생성되었습니다.")

if __name__ == "__main__":
    generate_hr_sample_data()