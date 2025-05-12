#!/bin/bash
echo "HR 대시보드 프로그램을 시작합니다..."
echo

# 가상환경이 있는지 확인
if [ ! -d "venv" ]; then
    echo "초기 설정을 진행합니다..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 앱 실행
streamlit run app.py