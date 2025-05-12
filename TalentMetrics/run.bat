@echo off
echo TalentMetrics - HR 대시보드 프로그램을 시작합니다...
echo.

REM 가상환경이 있는지 확인
if not exist "venv" (
    echo 초기 설정을 진행합니다...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM 앱 실행
streamlit run app.py

pause