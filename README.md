# TalentMetrics

인재 관련 메트릭을 시각적으로 분석할 수 있는 HR 데이터 대시보드 도구입니다.

---

## 주요 기능

- 엑셀 기반 HR 데이터 업로드 및 다양한 메트릭 시각화
- 이직률, 근속연수, 조직별/직무별 분석 등 다양한 HR 인사이트 제공
- Plotly, Matplotlib, Seaborn 기반의 고급 시각화
- Streamlit 기반의 웹 대시보드

---

## 폴더 구조

```
TalentMetrics/
├── app.py                # 메인 앱
├── requirements.txt      # 필수 패키지 목록
├── run.sh                # macOS/Linux 실행 스크립트
├── run.bat               # Windows 실행 스크립트
├── dummy/                # 샘플 데이터 및 생성 스크립트
│   ├── hr_sample_data.xlsx
│   └── generate_demo_excel.py 등
├── utils/                # 데이터 처리, 시각화, UI 모듈
├── assets/css/           # 커스텀 스타일 파일
```

---

## 설치 및 실행 방법

### 1. Python 3.11 설치

- [공식 다운로드 링크](https://www.python.org/downloads/)
- **반드시 3.11 버전 사용 (최신 버전은 pandas 호환성 문제 있음)**
- Windows: 설치 시 "Add Python to PATH" 체크

---

### 2. (권장) 자동 실행 스크립트 사용

#### Windows

1. `TalentMetrics` 폴더로 이동
2. `run.bat` 파일을 더블클릭하거나, PowerShell/cmd에서 아래 명령어 실행:
   ```
   cd TalentMetrics
   run.bat
   ```
   - 최초 실행 시 가상환경 및 패키지 자동 설치
   - 이후에도 동일하게 실행 가능

#### macOS/Linux

1. 터미널에서 `TalentMetrics` 폴더로 이동
2. 아래 명령어 실행:
   ```
   ./run.sh
   ```
   - 최초 실행 시 가상환경 및 패키지 자동 설치
   - 실행 권한이 없을 경우: `chmod +x run.sh`

---

### 3. 수동 설치 및 실행 (원리 이해용)

#### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd TalentMetrics
streamlit run app.py
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd TalentMetrics
streamlit run app.py
```

---

## 샘플 데이터로 바로 시작하기

- `TalentMetrics/dummy/hr_sample_data.xlsx` 파일을 업로드하여 바로 기능을 체험할 수 있습니다.
- 직접 데이터를 생성하고 싶다면 `dummy/generate_demo_excel.py` 실행

---

## 주요 의존성

- pandas==2.1.4
- openpyxl, streamlit, plotly, matplotlib, seaborn, numpy, wordcloud, calmap, scipy, statsmodels, scikit-learn, xlsxwriter

(자세한 버전은 `requirements.txt` 참고)

---

## 기타 안내 및 FAQ

- **가상환경 필수**: 항상 가상환경(venv) 활성화 후 실행
- **실행 후**: 자동으로 브라우저가 열리며, `http://localhost:8501`에서 대시보드 확인
- **Streamlit 환영 메시지**: 이메일 입력은 건너뛰어도 무방
- **커스텀 스타일**: `assets/css/` 내 CSS 파일로 UI 커스터마이징 가능

---

## 문의 및 기여

- 개선 제안, 버그 제보, PR 환영합니다!

## 라이선스 고지

이 프로젝트는 아래 오픈소스 라이브러리를 사용하며, 모두 상업적/업무용 환경에서 자유롭게 사용할 수 있는 라이선스(BSD, MIT, Apache 2.0 등)를 따릅니다.

- pandas: BSD 3-Clause License
- openpyxl: MIT License
- streamlit: Apache License 2.0
- plotly: MIT License
- matplotlib: PSF 및 BSD 스타일 License
- seaborn: BSD License
- numpy: BSD License
- wordcloud: MIT License
- calmap: MIT License
- scipy: BSD License
- statsmodels: BSD License
- scikit-learn: BSD License
- xlsxwriter: BSD License

각 라이브러리의 상세 라이선스 내용은 공식 문서 및 저장소를 참고해 주세요.