import requests
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

class SearchRankChecker:
    def __init__(self, config_module):
        self.config = config_module
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """세션 설정 및 헤더 설정"""
        headers = {
            'User-Agent': self.config.SEARCH_SETTINGS['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
    
    def check_blog_rank(self, clinic_name, keywords):
        """네이버 블로그 검색 순위 체크"""
        results = []
        
        for keyword in keywords:
            print(f"블로그 검색 중: {keyword}")
            
            try:
                # 네이버 블로그 검색 URL
                search_url = f"https://search.naver.com/search.naver?where=blog&query={keyword}"
                
                response = self.session.get(search_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 블로그 검색 결과 찾기
                blog_items = soup.find_all('li', class_='bx')
                rank = 0
                found = False
                
                for item in blog_items:
                    rank += 1
                    
                    # 블로그 제목과 내용에서 치과명 확인
                    title_elem = item.find('a', class_='title_link')
                    content_elem = item.find('div', class_='dsc')
                    
                    if title_elem and content_elem:
                        title = title_elem.get_text(strip=True)
                        content = content_elem.get_text(strip=True)
                        
                        # 치과명이 포함되어 있는지 확인
                        if clinic_name in title or clinic_name in content:
                            results.append({
                                'clinic_name': clinic_name,
                                'keyword': keyword,
                                'search_type': '블로그',
                                'rank': rank,
                                'title': title,
                                'url': title_elem.get('href', ''),
                                'content': content[:100] + '...' if len(content) > 100 else content
                            })
                            found = True
                            break
                
                if not found:
                    results.append({
                        'clinic_name': clinic_name,
                        'keyword': keyword,
                        'search_type': '블로그',
                        'rank': '순위 밖',
                        'title': '',
                        'url': '',
                        'content': ''
                    })
                
                # 요청 간 지연
                time.sleep(self.config.SEARCH_SETTINGS['delay_between_requests'])
                
            except Exception as e:
                print(f"블로그 검색 중 오류 발생: {e}")
                results.append({
                    'clinic_name': clinic_name,
                    'keyword': keyword,
                    'search_type': '블로그',
                    'rank': '오류',
                    'title': '',
                    'url': '',
                    'content': str(e)
                })
        
        return results
    
    def save_results(self, results):
        """결과를 Excel 파일로 저장"""
        if not results:
            print("저장할 결과가 없습니다.")
            return
        
        # DataFrame 생성
        df = pd.DataFrame(results)
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config.OUTPUT_SETTINGS['filename_prefix']}{timestamp}.xlsx"
        filepath = os.path.join(self.config.OUTPUT_SETTINGS['output_dir'], filename)
        
        # Excel 파일로 저장
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='검색순위결과', index=False)
            
            # 워크시트 포맷팅
            worksheet = writer.sheets['검색순위결과']
            
            # 열 너비 자동 조정
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"결과가 저장되었습니다: {filepath}")
        return filepath
    
    def close(self):
        """리소스 정리"""
        self.session.close() 