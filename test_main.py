#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
from search_rank_checker import SearchRankChecker
import test_config

def print_banner():
    """프로그램 시작 배너 출력"""
    print("=" * 60)
    print("치과 거래처 검색노출 순위 체크 프로그램 - 테스트")
    print("=" * 60)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_config():
    """설정 파일 검증"""
    if not test_config.DENTAL_CLINICS:
        print("❌ 오류: test_config.py 파일에 치과 정보가 설정되지 않았습니다.")
        return False
    
    print(f"✅ 설정된 치과 수: {len(test_config.DENTAL_CLINICS)}개")
    for i, clinic in enumerate(test_config.DENTAL_CLINICS, 1):
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
        checker = SearchRankChecker(test_config)
        print("✅ 검색 순위 체커가 초기화되었습니다.")
    except Exception as e:
        print(f"❌ 검색 순위 체커 초기화 실패: {e}")
        return
    
    all_results = []
    
    try:
        # 각 치과에 대해 검색 순위 체크
        for i, clinic in enumerate(test_config.DENTAL_CLINICS, 1):
            print(f"\n🔍 [{i}/{len(test_config.DENTAL_CLINICS)}] {clinic['name']} 검색 중...")
            print("-" * 40)
            
            # 블로그 검색 순위 체크만 실행
            print("📝 블로그 검색 순위 체크 중...")
            blog_results = checker.check_blog_rank(clinic['name'], clinic['keywords'])
            all_results.extend(blog_results)
            
            print(f"✅ {clinic['name']} 검색 완료")
            print(f"📊 블로그 검색 결과: {len(blog_results)}개")
        
        # 결과 저장
        if all_results:
            print(f"\n💾 검색 결과 저장 중...")
            print(f"📊 총 결과 수: {len(all_results)}개")
            
            filepath = checker.save_results(all_results)
            
            # 결과 요약 출력
            print("\n📊 검색 결과 요약:")
            print("-" * 40)
            
            for clinic in test_config.DENTAL_CLINICS:
                clinic_results = [r for r in all_results if r['clinic_name'] == clinic['name']]
                
                print(f"\n🏥 {clinic['name']}:")
                
                # 블로그 결과
                blog_results = [r for r in clinic_results if r['search_type'] == '블로그']
                for result in blog_results:
                    rank_text = f"{result['rank']}위" if isinstance(result['rank'], int) else result['rank']
                    print(f"  📝 블로그 ({result['keyword']}): {rank_text}")
            
            print(f"\n✅ 모든 검색이 완료되었습니다!")
            print(f"📁 결과 파일: {filepath}")
        
        else:
            print("❌ 검색 결과가 없습니다.")
    
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 검색 중 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 리소스 정리
        checker.close()
        print("\n👋 프로그램을 종료합니다.")

if __name__ == "__main__":
    main() 