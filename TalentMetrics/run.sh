#!/bin/bash
echo "TalentMetrics - HR 대시보드 프로그램을 시작합니다..."
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

# 필요한 디렉토리 확인 및 생성
if [ ! -d "assets/css" ]; then
    mkdir -p assets/css
fi

# 필요한 CSS 파일 복사
cp -n assets/css/style.css assets/css/style.css.bak 2>/dev/null || true
cp -n assets/css/modern_style.css assets/css/modern_style.css.bak 2>/dev/null || true

# 앱 실행
streamlit run app.py