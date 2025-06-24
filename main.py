#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
from search_rank_checker import SearchRankChecker
import config

def print_banner():
    """프로그램 배너 출력"""
    print("=" * 60)
    print("🏥 치과 거래처 검색노출 순위 체크 프로그램")
    print("=" * 60)
    print("네이버 블로그, 웹, 플레이스 검색에서 치과 순위를 체크합니다.")
    print()

def check_config():
    """설정 파일 검증"""
    if not config.DENTAL_CLINICS:
        print("❌ 오류: config.py 파일에 치과 정보가 설정되지 않았습니다.")
        print("config.py 파일의 DENTAL_CLINICS 리스트에 치과 정보를 추가해주세요.")
        return False
    
    print(f"✅ 설정된 치과 수: {len(config.DENTAL_CLINICS)}개")
    for i, clinic in enumerate(config.DENTAL_CLINICS, 1):
        print(f"  {i}. {clinic['name']} - {clinic['address']}")
    print()
    return True

def main():
    """메인 실행 함수"""
    print_banner()
    
    # 설정 파일 검증
    if not check_config():
        return
    
    # 검색 순위 체커 초기화
    try:
        checker = SearchRankChecker(config)
        print("✅ 검색 순위 체커가 초기화되었습니다.")
    except Exception as e:
        print(f"❌ 검색 순위 체커 초기화 실패: {e}")
        return
    
    all_results = []
    
    try:
        # 각 치과에 대해 검색 순위 체크
        for i, clinic in enumerate(config.DENTAL_CLINICS, 1):
            print(f"\n🔍 [{i}/{len(config.DENTAL_CLINICS)}] {clinic['name']} 검색 중...")
            print("-" * 40)
            
            # 모든 검색 유형에 대한 순위 체크 (블로그, 웹, 플레이스)
            print("📝 모든 검색 유형 순위 체크 중...")
            search_results = checker.check_all_ranks(clinic['name'], clinic['keywords'])
            all_results.extend(search_results)
            
            print(f"✅ {clinic['name']} 검색 완료")
        
        # 결과 저장
        if all_results:
            print(f"\n💾 검색 결과 저장 중...")
            filepath = checker.save_results(all_results)
            
            # 결과 요약 출력
            print("\n📊 검색 결과 요약:")
            print("-" * 40)
            
            for clinic in config.DENTAL_CLINICS:
                clinic_results = [r for r in all_results if r['clinic_name'] == clinic['name']]
                
                print(f"\n🏥 {clinic['name']}:")
                
                # 검색 유형별 결과
                search_types = {}
                for result in clinic_results:
                    search_type = result['search_type']
                    if search_type not in search_types:
                        search_types[search_type] = []
                    search_types[search_type].append(result)
                
                for search_type, results in search_types.items():
                    print(f"  🔍 {search_type}:")
                    for result in results:
                        rank_text = f"{result['rank']}위" if isinstance(result['rank'], int) else result['rank']
                        area_text = f"({result['search_area']})" if result['search_area'] != '일반' else ""
                        print(f"    - {result['keyword']}: {rank_text} {area_text}")
            
            print(f"\n✅ 모든 검색이 완료되었습니다!")
            print(f"📁 결과 파일: {filepath}")
        
        else:
            print("❌ 검색 결과가 없습니다.")
    
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 검색 중 오류가 발생했습니다: {e}")
    finally:
        # 리소스 정리
        checker.close()
        print("\n👋 프로그램을 종료합니다.")

if __name__ == "__main__":
    main() 