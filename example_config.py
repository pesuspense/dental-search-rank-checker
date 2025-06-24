# 치과 거래처 검색노출 순위 체크 프로그램 - 예시 설정 파일
# 이 파일을 config.py로 복사하여 사용하세요.

# 검색할 치과 거래처 정보
DENTAL_CLINICS = [
    {
        "name": "미소치과",
        "address": "서울시 강남구 테헤란로 123",
        "phone": "02-1234-5678",
        "keywords": ["미소치과", "강남치과", "미소치과 강남점", "강남 미소치과"]
    },
    {
        "name": "하얀치과",
        "address": "서울시 서초구 서초대로 456",
        "phone": "02-9876-5432",
        "keywords": ["하얀치과", "서초치과", "하얀치과 서초점", "서초 하얀치과"]
    },
    {
        "name": "스마일치과",
        "address": "서울시 마포구 홍대로 789",
        "phone": "02-5555-1234",
        "keywords": ["스마일치과", "마포치과", "스마일치과 마포점", "마포 스마일치과"]
    }
]

# 검색 설정
SEARCH_SETTINGS = {
    "max_pages": 10,  # 검색할 최대 페이지 수
    "delay_between_requests": 2,  # 요청 간 지연 시간 (초)
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 결과 파일 설정
OUTPUT_SETTINGS = {
    "output_dir": "data",
    "filename_prefix": "치과_검색순위_",
    "include_timestamp": True
}

# 네이버 검색 설정
NAVER_SETTINGS = {
    "blog_search_url": "https://search.naver.com/search.naver",
    "place_search_url": "https://search.naver.com/search.naver"
}

# 사용법:
# 1. 이 파일을 config.py로 복사
# 2. DENTAL_CLINICS 리스트에 실제 치과 정보 입력
# 3. keywords 리스트에 검색할 키워드들 입력
# 4. python main.py 실행 