import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os
import json
from search_rank_checker import SearchRankChecker
import config

# 페이지 설정
st.set_page_config(
    page_title="치과 검색순위 체크",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 웹 배포를 위한 설정
def get_search_checker():
    """검색 체커를 생성"""
    try:
        return SearchRankChecker(config)
    except Exception as e:
        st.error(f"검색 체커 초기화 오류: {e}")
        return None

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .clinic-card {
        background-color: #f0f2f6;
        color: #222;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .result-table {
        margin-top: 1rem;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_clinics():
    """치과 정보 로드"""
    try:
        if os.path.exists('clinics.json'):
            with open('clinics.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # config.py에서 기본 정보 로드
            return config.DENTAL_CLINICS
    except Exception as e:
        st.error(f"치과 정보 로드 오류: {e}")
        return []

def save_clinics(clinics):
    """치과 정보 저장"""
    try:
        with open('clinics.json', 'w', encoding='utf-8') as f:
            json.dump(clinics, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"저장 중 오류: {e}")
        return False

def clinic_management():
    """치과 정보 관리"""
    st.header("🏥 치과 정보 관리")
    
    # 현재 치과 목록 로드
    clinics = load_clinics()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📋 치과 목록", "➕ 새 치과 추가", "✏️ 치과 수정"])
    
    with tab1:
        st.subheader("등록된 치과 목록")
        if clinics:
            for i, clinic in enumerate(clinics):
                with st.expander(f"{i+1}. {clinic['name']}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**주소:** {clinic['address']}")
                        st.write(f"**전화:** {clinic['phone']}")
                        st.write(f"**키워드:** {', '.join(clinic['keywords'])}")
                    with col2:
                        if st.button(f"삭제", key=f"del_{i}", type="secondary"):
                            clinics.pop(i)
                            if save_clinics(clinics):
                                st.success("치과가 삭제되었습니다.")
                                st.rerun()
        else:
            st.info("등록된 치과가 없습니다.")
    
    with tab2:
        st.subheader("새 치과 추가")
        with st.form("add_clinic"):
            name = st.text_input("치과명 *", placeholder="예: 미소치과")
            address = st.text_input("주소 *", placeholder="예: 서울시 강남구 테헤란로 123")
            phone = st.text_input("전화번호", placeholder="예: 02-1234-5678")
            keywords_input = st.text_area("검색 키워드 (한 줄에 하나씩) *", 
                                        placeholder="미소치과\n강남치과\n미소치과 강남점\n강남 미소치과")
            
            submitted = st.form_submit_button("치과 추가", type="primary")
            if submitted:
                if name and address and keywords_input.strip():
                    keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]
                    new_clinic = {
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "keywords": keywords
                    }
                    clinics.append(new_clinic)
                    if save_clinics(clinics):
                        st.success(f"'{name}' 치과가 추가되었습니다!")
                        st.rerun()
                else:
                    st.error("치과명, 주소, 키워드는 필수 입력 항목입니다.")
    
    with tab3:
        st.subheader("치과 정보 수정")
        if clinics:
            clinic_names = [clinic['name'] for clinic in clinics]
            selected_clinic_name = st.selectbox("수정할 치과 선택", clinic_names)
            
            if selected_clinic_name:
                selected_clinic = next((c for c in clinics if c['name'] == selected_clinic_name), None)
                if selected_clinic:
                    with st.form("edit_clinic"):
                        name = st.text_input("치과명", value=selected_clinic['name'])
                        address = st.text_input("주소", value=selected_clinic['address'])
                        phone = st.text_input("전화번호", value=selected_clinic['phone'])
                        keywords_input = st.text_area("검색 키워드 (한 줄에 하나씩)", 
                                                    value='\n'.join(selected_clinic['keywords']))
                        
                        submitted = st.form_submit_button("수정 저장", type="primary")
                        if submitted:
                            if name and address and keywords_input.strip():
                                keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]
                                selected_clinic.update({
                                    "name": name,
                                    "address": address,
                                    "phone": phone,
                                    "keywords": keywords
                                })
                                if save_clinics(clinics):
                                    st.success(f"'{name}' 치과 정보가 수정되었습니다!")
                                    st.rerun()
                            else:
                                st.error("치과명, 주소, 키워드는 필수 입력 항목입니다.")
        else:
            st.info("수정할 치과가 없습니다.")

def main():
    # 헤더
    st.markdown('<h1 class="main-header">🏥 치과 검색순위 체크 시스템</h1>', unsafe_allow_html=True)
    
    # 메뉴 선택
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["🔍 검색 실행", "🏥 치과 관리", "📊 이전 결과"]
    )
    
    if menu == "🔍 검색 실행":
        search_page()
    elif menu == "🏥 치과 관리":
        clinic_management()
    elif menu == "📊 이전 결과":
        show_previous_results()

def search_page():
    """검색 페이지"""
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 검색 설정")
        
        # 검색 설정
        st.subheader("검색 설정")
        delay = st.slider("요청 간 지연시간 (초)", 1, 5, 2)
        
        # 검색 유형 선택
        st.subheader("🔍 검색 유형")
        search_types = st.multiselect(
            "검색할 유형 선택 (복수 선택 가능)",
            ["블로그", "웹", "플레이스"],
            default=["블로그"]  # 기본값: 블로그만
        )
        
        # 치과 정보 표시 및 선택
        st.subheader("📋 등록된 치과")
        clinics = load_clinics()
        clinic_names = [clinic['name'] for clinic in clinics]
        if clinics:
            selected_clinics = st.multiselect(
                "검색할 치과 선택 (복수 선택 가능)",
                clinic_names,
                default=clinic_names  # 기본값: 전체 선택
            )
            for i, clinic in enumerate(clinics, 1):
                with st.expander(f"{i}. {clinic['name']}"):
                    st.write(f"**주소:** {clinic['address']}")
                    st.write(f"**전화:** {clinic['phone']}")
                    st.write(f"**키워드:** {', '.join(clinic['keywords'])}")
        else:
            st.warning("설정된 치과가 없습니다.")
            st.info("'🏥 치과 관리' 메뉴에서 치과를 추가해주세요.")
        
        # 실행 버튼
        st.markdown("---")
        if st.button("🚀 검색 시작", type="primary", use_container_width=True):
            st.session_state.run_search = True
            st.session_state.delay = delay
            st.session_state.selected_clinics = selected_clinics if clinics else []
            st.session_state.search_types = search_types
    
    # 메인 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 검색 결과")
        
        # 검색 실행
        if 'run_search' in st.session_state and st.session_state.run_search:
            run_search_process(st.session_state.delay, st.session_state.selected_clinics, st.session_state.search_types)
            st.session_state.run_search = False
    
    with col2:
        st.header("📈 통계")
        show_statistics()

def show_previous_results():
    """이전 결과 보기"""
    st.header("📊 이전 검색 결과")
    
    # data 폴더에서 Excel 파일 찾기
    if os.path.exists('data'):
        excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
        excel_files.sort(reverse=True)  # 최신 파일부터
        
        if excel_files:
            selected_file = st.selectbox("결과 파일 선택", excel_files)
            if selected_file:
                file_path = os.path.join('data', selected_file)
                try:
                    df = pd.read_excel(file_path)
                    st.subheader(f"📋 {selected_file}")
                    
                    # 통계 정보
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("총 결과", len(df))
                    with col2:
                        found_results = len(df[df['rank'] != '순위 밖'])
                        st.metric("순위 내 결과", found_results)
                    with col3:
                        if len(df) > 0:
                            avg_rank = df[df['rank'].apply(lambda x: isinstance(x, int))]['rank'].mean()
                            st.metric("평균 순위", f"{avg_rank:.1f}" if not pd.isna(avg_rank) else "N/A")
                    
                    # 결과 테이블
                    st.dataframe(df, use_container_width=True)
                    
                    # 다운로드 버튼
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📄 CSV 다운로드",
                        data=csv,
                        file_name=selected_file.replace('.xlsx', '.csv'),
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"파일 읽기 오류: {e}")
        else:
            st.info("이전 검색 결과가 없습니다.")
    else:
        st.info("결과 폴더가 없습니다.")

def run_search_process(delay, selected_clinic_names=None, search_types=None):
    """검색 프로세스 실행"""
    clinics = load_clinics()
    if not clinics:
        st.error("설정된 치과가 없습니다. '🏥 치과 관리' 메뉴에서 치과를 추가해주세요.")
        return
    
    # 선택된 치과만 필터링
    if selected_clinic_names is not None:
        clinics = [clinic for clinic in clinics if clinic['name'] in selected_clinic_names]
    if not clinics:
        st.warning("선택된 치과가 없습니다.")
        return
    
    # 검색 유형 확인
    if not search_types:
        st.warning("검색할 유형을 선택해주세요.")
        return
    
    # 진행 상황 표시
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 검색 순위 체커 초기화
        status_text.text("🔧 검색 순위 체커 초기화 중...")
        checker = get_search_checker()
        if checker is None:
            st.error("검색 체커 초기화에 실패했습니다.")
            return
            
        progress_bar.progress(10)
        
        all_results = []
        total_clinics = len(clinics)
        
        # 각 치과에 대해 검색
        for i, clinic in enumerate(clinics):
            progress = 10 + (i / total_clinics) * 80
            progress_bar.progress(int(progress))
            
            # 치과 카드 표시
            with st.container():
                st.markdown(f"""
                <div class="clinic-card">
                    <h3>🏥 {clinic['name']}</h3>
                    <p><strong>주소:</strong> {clinic['address']}</p>
                    <p><strong>키워드:</strong> {', '.join(clinic['keywords'])}</p>
                    <p><strong>검색 유형:</strong> {', '.join(search_types)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            status_text.text(f"🔍 {clinic['name']} 검색 중... ({', '.join(search_types)})")
            
            # 선택된 검색 유형에 따라 검색 수행
            search_results = checker.check_all_ranks(clinic['name'], clinic['keywords'], search_types)
            all_results.extend(search_results)
            
            # 실시간 결과 표시
            if search_results:
                df_temp = pd.DataFrame(search_results)
                st.dataframe(df_temp, use_container_width=True)
            
            time.sleep(delay)
        
        # 결과 저장
        progress_bar.progress(90)
        status_text.text("💾 결과 저장 중...")
        
        if all_results:
            filepath = checker.save_results(all_results)
            progress_bar.progress(100)
            status_text.text("✅ 검색 완료!")
            
            # 성공 메시지
            st.success(f"검색이 완료되었습니다! 결과 파일: {filepath}")
            
            # 결과 요약 표시
            show_search_summary(all_results)
            
            # 세션에 결과 저장
            st.session_state.search_results = all_results
            st.session_state.result_filepath = filepath
        
        else:
            st.warning("검색 결과가 없습니다.")
        
        # 리소스 정리
        checker.close()
        
    except Exception as e:
        st.error(f"검색 중 오류가 발생했습니다: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ 오류 발생")

def show_search_summary(results):
    """검색 결과 요약 표시"""
    st.subheader("📋 검색 결과 요약")
    
    if not results:
        st.info("검색 결과가 없습니다.")
        return
    
    df = pd.DataFrame(results)
    
    # 통계 정보
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("총 검색 결과", len(results))
    
    with col2:
        found_results = len(df[df['rank'] != '순위 밖'])
        st.metric("순위 내 결과", found_results)
    
    with col3:
        if len(results) > 0:
            avg_rank = df[df['rank'].apply(lambda x: isinstance(x, int))]['rank'].mean()
            st.metric("평균 순위", f"{avg_rank:.1f}" if not pd.isna(avg_rank) else "N/A")
    
    # 검색 유형별 통계
    st.subheader("🔍 검색 유형별 결과")
    search_type_counts = df['search_type'].value_counts()
    st.bar_chart(search_type_counts)
    
    # 결과 테이블
    st.subheader("📊 상세 결과")
    st.dataframe(df, use_container_width=True)
    
    # Excel 다운로드 버튼
    if st.button("📥 Excel 파일 다운로드", type="secondary"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 CSV 파일 다운로드",
            data=csv,
            file_name=f"치과_검색순위_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def show_statistics():
    """통계 정보 표시"""
    if 'search_results' in st.session_state:
        results = st.session_state.search_results
        df = pd.DataFrame(results)
        
        # 치과별 결과 수
        st.subheader("🏥 치과별 결과")
        clinic_counts = df['clinic_name'].value_counts()
        st.bar_chart(clinic_counts)
        
        # 검색 유형별 결과 수
        st.subheader("🔍 검색 유형별 결과")
        search_type_counts = df['search_type'].value_counts()
        st.bar_chart(search_type_counts)
        
        # 키워드별 결과 수
        st.subheader("🔑 키워드별 결과")
        keyword_counts = df['keyword'].value_counts()
        st.bar_chart(keyword_counts)
        
        # 순위 분포
        st.subheader("📈 순위 분포")
        rank_counts = df['rank'].value_counts()
        st.bar_chart(rank_counts)
    else:
        st.info("검색을 실행하면 통계가 표시됩니다.")

if __name__ == "__main__":
    main() 