# 치과 거래처 검색노출 순위 체크 프로그램 설정 파일

# 검색할 치과 거래처 정보
DENTAL_CLINICS = [
    {
        "name": "파미에치과",
        "address": "서울시 마포구 양화로 151 욱도빌딩 4층 연세파미에치과",
        "phone": "02-3142-2828",
        "keywords": ["합청치과", "홍대치과", "파미에치과"]
    },
    # 추가 치과 정보를 여기에 입력하세요
    # {
    #     "name": "다른치과",
    #     "address": "서울시 서초구", 
    #     "phone": "02-9876-5432",
    #     "keywords": ["다른치과", "서초치과"]
    # }
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