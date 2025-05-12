import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from io import BytesIO

def generate_rich_demo_excel():
    """
    다양한 시트와 컬럼을 포함한 풍부한 HR 데모 데이터를 생성하여 BytesIO로 반환합니다.
    """
    np.random.seed(42)
    random.seed(42)

    # 1. 부서별 채용 현황 데이터
    departments = [
        '개발팀', '마케팅', '영업', '인사팀', '고객지원', 'IT지원', 
        '디자인', '연구개발', '재무', '법무', '운영', '제품관리',
        '프로젝트관리', '품질관리', '경영지원', '전략기획', 'CS', 'QA', 'R&D', '기획'
    ]
    headcounts = np.round(np.maximum(1, np.random.normal(15, 7, len(departments)))).astype(int)
    avg_salary = 5200
    budgets = headcounts * avg_salary * (0.85 + 0.3 * np.random.random(len(departments)))
    budgets = np.round(budgets, -1)
    hiring_rates = np.round(np.random.uniform(0.6, 1.3, len(departments)), 2)
    managers = [f"{random.choice(['김','이','박','최','정','강','조','윤','장','임'])}{random.choice(['민준','서연','도윤','서현','예준','지우'])}" for _ in departments]
    df_departments = pd.DataFrame({
        '부서': departments,
        '인원수': headcounts,
        '채용예산(만원)': budgets,
        '채용율': hiring_rates,
        '부서장': managers
    })

    # 2. 직무별 채용 현황 데이터
    roles = [
        '백엔드개발자', '프론트엔드개발자', '데이터분석가', '데이터엔지니어',
        'HR매니저', '마케팅전문가', '디자이너', '영업담당자', '고객서비스담당자',
        '품질관리자', '제품관리자', '프로젝트매니저', '연구원', '재무분석가',
        '법무담당자', '전략기획자', '운영담당자', 'DevOps엔지니어', 'QA엔지니어',
        '시스템관리자', 'AI엔지니어', 'UX디자이너', 'PM', '테스터'
    ]
    role_headcounts = np.round(np.maximum(1, np.random.normal(8, 4, len(roles)))).astype(int)
    role_budgets = role_headcounts * (avg_salary * 0.8 + avg_salary * 0.5 * np.random.random(len(roles)))
    role_budgets = np.round(role_budgets, -1)
    role_levels = np.random.choice(['주니어', '시니어', '매니저', '임원'], len(roles))
    df_roles = pd.DataFrame({
        '직무': roles,
        '채용인원': role_headcounts,
        '직무별예산(만원)': role_budgets,
        '직무레벨': role_levels
    })

    # 3. 월별 채용 추이 데이터
    months = pd.date_range(start='2023-07-01', periods=18, freq='M')
    monthly_hires = np.round(np.maximum(5, 30 + 12 * np.sin(np.arange(18) * np.pi / 6) + np.random.normal(0, 4, 18))).astype(int)
    monthly_budget = np.round(monthly_hires * avg_salary * (0.8 + 0.4 * np.random.random(18)), -1)
    df_monthly = pd.DataFrame({
        '월': [d.strftime('%Y-%m') for d in months],
        '채용인원': monthly_hires,
        '월별예산(만원)': monthly_budget
    })

    # 4. 지역별 채용 현황 데이터
    locations = [
        '서울', '부산', '인천', '대구', '광주', '대전', 
        '울산', '세종', '경기', '강원', '충북', '충남',
        '전북', '전남', '경북', '경남', '제주', '해외'
    ]
    location_hires = np.round(np.maximum(1, np.random.normal(12, 7, len(locations)))).astype(int)
    location_budget = np.round(location_hires * avg_salary * (0.7 + 0.5 * np.random.random(len(locations))), -1)
    df_locations = pd.DataFrame({
        '지역': locations,
        '채용인원': location_hires,
        '지역예산(만원)': location_budget
    })

    # 5. 개인별 상세 데이터 (500명)
    n_samples = 500
    first_names = [
        '민준', '서연', '도윤', '서현', '예준', '지우', '하준', '하은', '주원', '민서',
        '지호', '지민', '지윤', '준서', '유준', '예은', '건우', '지아', '현우', '서윤',
        '유진', '승민', '수빈', '예린', '준영', '수민', '지원', '하윤', '유빈', '재원'
    ]
    last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '신', '서', '권', '황', '안', '송', '전', '홍']
    names = [f'{random.choice(last_names)}{random.choice(first_names)}' for _ in range(n_samples)]
    today = datetime.now()
    hire_dates = [today - timedelta(days=random.randint(1, 540)) for _ in range(n_samples)]
    hire_dates = [d.strftime('%Y-%m-%d') for d in hire_dates]
    emp_departments = [random.choice(departments) for _ in range(n_samples)]
    emp_roles = [random.choice(roles) for _ in range(n_samples)]
    emp_locations = [random.choice(locations) for _ in range(n_samples)]
    salaries = np.round(np.random.uniform(3800, 8000, n_samples), -1)
    genders = np.random.choice(['남', '여'], n_samples)
    age_groups = np.random.choice(['20대', '30대', '40대', '50대', '60대'], n_samples, p=[0.25, 0.35, 0.25, 0.1, 0.05])
    years_exp = np.random.randint(0, 31, n_samples)
    edu_levels = np.random.choice(['고졸', '전문학사', '학사', '석사', '박사'], n_samples, p=[0.1, 0.15, 0.5, 0.2, 0.05])
    df_employees = pd.DataFrame({
        '이름': names,
        '입사일': hire_dates,
        '부서': emp_departments,
        '직무': emp_roles,
        '지역': emp_locations,
        '연봉(만원)': salaries,
        '성별': genders,
        '연령대': age_groups,
        '경력(년)': years_exp,
        '학력': edu_levels
    })

    # 6. 추가: 부서-직무 매핑 데이터
    mapping_rows = []
    for dept in departments:
        for _ in range(random.randint(2, 6)):
            mapping_rows.append({
                '부서': dept,
                '직무': random.choice(roles),
                '필요인원': random.randint(1, 8)
            })
    df_dept_role_map = pd.DataFrame(mapping_rows)

    # 엑셀 파일로 변환 (BytesIO)
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df_departments.to_excel(writer, sheet_name='부서별채용현황', index=False)
        df_roles.to_excel(writer, sheet_name='직무별채용현황', index=False)
        df_monthly.to_excel(writer, sheet_name='월별채용추이', index=False)
        df_locations.to_excel(writer, sheet_name='지역별채용현황', index=False)
        df_employees.to_excel(writer, sheet_name='채용상세데이터', index=False)
        df_dept_role_map.to_excel(writer, sheet_name='부서-직무매핑', index=False)
    excel_buffer.seek(0)
    return excel_buffer 