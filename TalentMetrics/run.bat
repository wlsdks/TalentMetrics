@echo off
REM assets\css 폴더가 없으면 생성
if not exist "assets\css" (
    mkdir assets\css
)

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