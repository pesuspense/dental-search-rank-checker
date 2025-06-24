# 테스트용 설정 파일

# 검색할 치과 거래처 정보
DENTAL_CLINICS = [
    {
        "name": "테스트치과",
        "address": "서울시 강남구",
        "phone": "02-1234-5678",
        "keywords": ["치과", "강남치과"]
    }
]

# 검색 설정
SEARCH_SETTINGS = {
    "max_pages": 5,  # 검색할 최대 페이지 수
    "delay_between_requests": 1,  # 요청 간 지연 시간 (초)
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 결과 파일 설정
OUTPUT_SETTINGS = {
    "output_dir": "data",
    "filename_prefix": "테스트_검색순위_",
    "include_timestamp": True
}

# 네이버 검색 설정
NAVER_SETTINGS = {
    "blog_search_url": "https://search.naver.com/search.naver",
    "place_search_url": "https://search.naver.com/search.naver"
} 