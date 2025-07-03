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
        """네이버 블로그 검색 순위 체크 (인기글/일반글 모두)"""
        results = []
        for keyword in keywords:
            print(f"블로그 검색 중: {keyword}")
            try:
                search_url = f"https://search.naver.com/search.naver?where=blog&query={keyword}"
                response = self.session.get(search_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                     # 1. 인기글 영역
                popular_section = soup.find(
                    'section',
                    class_='sc_new sp_nreview _fe_view_root _prs_ugB_bsR'
                )
                popular_found = False
                if popular_section:
                    blog_items = popular_section.select('ul.lst_view > li.bx')
                    rank = 0
                    for item in blog_items:
                        rank += 1
                        # 인기글의 제목과 요약 텍스트
                        title_elem   = item.select_one('.title_area a.title_link')
                        content_elem = item.select_one('.dsc_area a.dsc_link')
                        if title_elem and content_elem:
                            title   = title_elem.get_text(strip=True)
                            content = content_elem.get_text(strip=True)
                            if clinic_name in title or clinic_name in content:
                                results.append({
                                    'clinic_name': clinic_name,
                                    'keyword': keyword,
                                    'search_type': '블로그',
                                    'search_area': '인기글',
                                    'rank': rank,
                                    'title': title,
                                    'url': title_elem.get('href', ''),
                                    'content': content[:100] + '...' if len(content) > 100 else content
                                })
                                popular_found = True
                                break
                    if not popular_found:
                        results.append({
                            'clinic_name': clinic_name,
                            'keyword': keyword,
                            'search_type': '블로그',
                            'search_area': '인기글',
                            'rank': '순위 밖',
                            'title': '',
                            'url': '',
                            'content': ''
                        })


                # 2. 일반 블로그 영역
                normal_section = soup.find('section', class_='sc_new sp_ntotal _sp_ntotal _prs_web_gen _fe_root_web_gend')
                normal_found = False
                if normal_section:
                    blog_items = normal_section.select('ul.lst_total > li.bx')
                    rank = 0
                    for item in blog_items:
                        rank += 1
                        title_elem = item.select_one('a.link_tit')
                        content_elem = item.select_one('a.api_txt_lines.total_dsc')
                        if title_elem and content_elem:
                            title = title_elem.get_text(strip=True)
                            content = content_elem.get_text(strip=True)
                            if clinic_name in title or clinic_name in content:
                                results.append({
                                    'clinic_name': clinic_name,
                                    'keyword': keyword,
                                    'search_type': '블로그',
                                    'search_area': '일반',
                                    'rank': rank,
                                    'title': title,
                                    'url': title_elem.get('href', ''),
                                    'content': content[:100] + '...' if len(content) > 100 else content
                                })
                                normal_found = True
                                break
                    if not normal_found:
                        results.append({
                            'clinic_name': clinic_name,
                            'keyword': keyword,
                            'search_type': '블로그',
                            'search_area': '일반',
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
                    'search_area': '오류',
                    'rank': '오류',
                    'title': '',
                    'url': '',
                    'content': str(e)
                })
        return results

    def check_web_rank(self, clinic_name, keywords):
        """네이버 웹 검색 순위 체크"""
        results = []
        for keyword in keywords:
            print(f"웹 검색 중: {keyword}")
            try:
                search_url = f"https://search.naver.com/search.naver?query={keyword}"
                response = self.session.get(search_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # 1) '웹(통합)' 결과가 들어있는 section
                section = soup.select_one('section.sc_new.sp_ntotal')
                # 2) 그 안의 <ul class="lst_total"> 이하 항목들
                web_items = section.select('ul.lst_total > li.bx') if section else []

                rank = 0
                found = False

                for item in web_items:
                    # 광고/특집 블록 건너뛰기: 
                    # (예: 별도 클래스가 붙어있다면 continue)
                    if item.select_one('.api_sponsor') or item.select_one('.btn_save'):
                        continue

                    rank += 1

                    # 제목 추출: <a class="link_tit"> 또는 <a class="link_tit" href=…>
                    title_elem = item.select_one('a.link_tit')
                    # 요약/본문 추출: <div class="api_txt_lines total_dsc">…
                    content_elem = item.select_one('div.total_dsc_wrap .api_txt_lines')

                    if title_elem:
                        title   = title_elem.get_text(strip=True)
                        url     = title_elem['href']
                        content = content_elem.get_text(strip=True) if content_elem else ''

                        # 클리닉명 포함 여부 체크
                        if clinic_name in title or clinic_name in content:
                            results.append({
                                'clinic_name': clinic_name,
                                'keyword': keyword,
                                'search_type': '웹',
                                'search_area': '일반',
                                'rank': rank,
                                'title': title,
                                'url': url,
                                'content': (content[:100] + '...') if len(content) > 100 else content
                            })
                            found = True
                            break

                if not found:
                    results.append({
                        'clinic_name': clinic_name,
                        'keyword': keyword,
                        'search_type': '웹',
                        'search_area': '일반',
                        'rank': '순위 밖',
                        'title': '',
                        'url': '',
                        'content': ''
                    })

                time.sleep(self.config.SEARCH_SETTINGS['delay_between_requests'])

            except Exception as e:
                print(f"웹 검색 중 오류 발생: {e}")
                results.append({
                    'clinic_name': clinic_name,
                    'keyword': keyword,
                    'search_type': '웹',
                    'search_area': '오류',
                    'rank': '오류',
                    'title': '',
                    'url': '',
                    'content': str(e)
                })

        return results


    from bs4 import BeautifulSoup
    import time

    def check_place_rank(self, clinic_name, keywords):
        """네이버 플레이스 검색 순위 체크"""
        results = []
        for keyword in keywords:
            print(f"플레이스 검색 중: {keyword}")
            try:
                search_url = f"https://search.naver.com/search.naver?where=place&query={keyword}"
                response = self.session.get(search_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # 실제 리스트 아이템
                place_items = soup.select('ul.zPw6U > li.DWs4Q')
                rank = 0
                found = False

                for item in place_items:
                    # 광고 배너 제거: '광고' 레이블이 있는 경우 스킵
                    if item.select_one('.place_ad_label_text'):
                        continue

                    rank += 1

                    # 제목 요소
                    title_a = item.select_one('div.LYTmB > a.place_bluelink')
                    title = title_a.get_text(strip=True) if title_a else ''

                    # 링크
                    url = title_a['href'] if title_a and title_a.has_attr('href') else ''

                    # 주소 요소
                    addr_span = item.select_one('div.w32a4 span.Pb4bU')
                    address = addr_span.get_text(strip=True) if addr_span else ''

                    # 치과명 매칭
                    if clinic_name in title or clinic_name in address:
                        results.append({
                            'clinic_name':   clinic_name,
                            'keyword':       keyword,
                            'search_type':   '플레이스',
                            'search_area':   '일반',
                            'rank':          rank,
                            'title':         title,
                            'url':           url,
                            'content':       address,
                        })
                        found = True
                        break

                if not found:
                    results.append({
                        'clinic_name': clinic_name,
                        'keyword':     keyword,
                        'search_type': '플레이스',
                        'search_area': '일반',
                        'rank':        '순위 밖',
                        'title':       '',
                        'url':         '',
                        'content':     '',
                    })

                time.sleep(self.config.SEARCH_SETTINGS['delay_between_requests'])

            except Exception as e:
                print(f"플레이스 검색 중 오류 발생: {e}")
                results.append({
                    'clinic_name': clinic_name,
                    'keyword':     keyword,
                    'search_type': '플레이스',
                    'search_area': '오류',
                    'rank':        '오류',
                    'title':       '',
                    'url':         '',
                    'content':     str(e),
                })

        return results


    def check_all_ranks(self, clinic_name, keywords, search_types=None):
        """모든 검색 유형에 대한 순위 체크"""
        if search_types is None:
            search_types = ['블로그', '웹', '플레이스']
        
        all_results = []
        
        if '블로그' in search_types:
            blog_results = self.check_blog_rank(clinic_name, keywords)
            all_results.extend(blog_results)
        
        if '웹' in search_types:
            web_results = self.check_web_rank(clinic_name, keywords)
            all_results.extend(web_results)
        
        if '플레이스' in search_types:
            place_results = self.check_place_rank(clinic_name, keywords)
            all_results.extend(place_results)
        
        return all_results
    
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