# 🏥 치과 검색순위 체크 시스템

치과 거래처의 블로그 검색 노출 순위를 체크하는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **🔍 블로그 검색**: 네이버 블로그에서 치과별 검색 순위 확인
- **🏥 치과 관리**: 웹에서 직접 치과 정보 등록/수정/삭제
- **📊 결과 분석**: 검색 결과 통계 및 시각화
- **📄 파일 다운로드**: Excel/CSV 형태로 결과 다운로드

## 🛠️ 설치 및 실행

### 로컬 실행
```bash
# 가상환경 생성
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 패키지 설치
pip install -r requirements.txt

# 웹앱 실행
streamlit run web_app.py
```

### 웹 배포
1. GitHub에 코드 업로드
2. [Streamlit Cloud](https://share.streamlit.io/)에서 배포
3. 또는 [Heroku](https://heroku.com/) 사용

## 📁 프로젝트 구조

```
TDTEST/
├── web_app.py              # 메인 웹 애플리케이션
├── search_rank_checker.py  # 검색 순위 체크 클래스
├── config.py              # 설정 파일
├── requirements.txt       # Python 패키지 목록
├── README.md             # 프로젝트 설명
└── data/                 # 검색 결과 저장 폴더
```

## 🔧 설정

`config.py` 파일에서 다음 설정을 변경할 수 있습니다:
- 검색할 치과 정보
- 검색 키워드
- 기타 설정 옵션

## 📊 사용법

1. 웹앱 접속
2. "🏥 치과 관리"에서 검색할 치과 등록
3. "🔍 검색 실행"에서 검색 시작
4. 결과 확인 및 다운로드

## 🌐 웹 배포 방법

### Streamlit Cloud 배포
1. GitHub에 코드 업로드
2. [share.streamlit.io](https://share.streamlit.io/) 접속
3. GitHub 계정 연결
4. 저장소 선택 및 배포

### Heroku 배포
1. `Procfile` 생성
2. Heroku CLI 설치
3. 앱 생성 및 배포

## 📝 라이선스

이 프로젝트는 개인 및 상업적 용도로 자유롭게 사용할 수 있습니다.

## 🤝 기여

버그 리포트나 기능 제안은 언제든 환영합니다! 