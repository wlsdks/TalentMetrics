# TalentMetrics
인재 관련 메트릭을 확인할 수 있는 도구

## macOS 설치 방법
1. 파이썬 설치
링크 : https://www.python.org/downloads/ (3.11 버전으로 받아야함 최신 x: pandas 문제)

2. 가상 환경 설정
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 가상 환경이 활성화된 상태에서 실행
```bash
streamlit run app.py
```

## Windows 설치 방법
1. 파이썬 설치
링크 : https://www.python.org/downloads/ (3.11 버전으로 받아야함 최신 x: pandas 문제)
   - 설치 시 "Add Python to PATH" 옵션 체크

2. 가상 환경 설정
   - PowerShell이나 Command Prompt(cmd)를 실행
   - 프로젝트 폴더로 이동 후 다음 명령어들을 순서대로 실행:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
   - 가상환경이 활성화되면 터미널 앞에 (venv)가 표시됩니다

3. 가상 환경이 활성화된 상태에서 실행
```bash
streamlit run app.py
```
   - 첫 실행 시 Streamlit의 환영 메시지가 표시됩니다
   - 이메일 입력은 선택사항이므로 Enter를 눌러 건너뛰셔도 됩니다

## 주의사항
- Python 3.11 버전을 사용해야 합니다 (최신 버전은 pandas 호환성 문제가 있을 수 있음)
- 가상환경이 활성화된 상태에서만 실행해야 합니다