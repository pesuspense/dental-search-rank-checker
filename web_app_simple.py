import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# 페이지 설정
st.set_page_config(
    page_title="치과 검색순위 체크",
    page_icon="🏥",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
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
            # 기본 치과 정보
            return [
                {
                    "name": "합청치과",
                    "address": "서울시 강남구",
                    "phone": "02-1234-5678",
                    "keywords": ["합청치과", "강남치과", "합청치과 강남점"]
                },
                {
                    "name": "홍대치과",
                    "address": "서울시 마포구",
                    "phone": "02-2345-6789",
                    "keywords": ["홍대치과", "마포치과", "홍대치과 마포점"]
                }
            ]
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

def main():
    # 헤더
    st.markdown('<h1 class="main-header">🏥 치과 검색순위 체크 시스템</h1>', unsafe_allow_html=True)
    
    st.success("✅ 웹앱이 성공적으로 로드되었습니다!")
    
    # 메뉴 선택
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["🏥 치과 관리", "📊 테스트"]
    )
    
    if menu == "🏥 치과 관리":
        clinic_management()
    elif menu == "📊 테스트":
        test_page()

def clinic_management():
    """치과 정보 관리"""
    st.header("🏥 치과 정보 관리")
    
    # 현재 치과 목록 로드
    clinics = load_clinics()
    
    # 탭 생성
    tab1, tab2 = st.tabs(["📋 치과 목록", "➕ 새 치과 추가"])
    
    with tab1:
        st.subheader("등록된 치과 목록")
        if clinics:
            for i, clinic in enumerate(clinics):
                with st.expander(f"{i+1}. {clinic['name']}", expanded=False):
                    st.write(f"**주소:** {clinic['address']}")
                    st.write(f"**전화:** {clinic['phone']}")
                    st.write(f"**키워드:** {', '.join(clinic['keywords'])}")
                    
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
                                        placeholder="미소치과\n강남치과\n미소치과 강남점")
            
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

def test_page():
    """테스트 페이지"""
    st.header("📊 테스트 페이지")
    
    st.info("이 페이지는 웹앱이 정상적으로 작동하는지 테스트하는 페이지입니다.")
    
    # 간단한 테스트 데이터
    test_data = {
        '치과명': ['합청치과', '홍대치과', '파미에치과'],
        '키워드': ['합청치과', '홍대치과', '파미에치과'],
        '순위': [1, 3, '순위 밖'],
        '검색타입': ['블로그', '블로그', '블로그']
    }
    
    df = pd.DataFrame(test_data)
    st.dataframe(df, use_container_width=True)
    
    # 차트 테스트
    st.subheader("📈 차트 테스트")
    chart_data = pd.DataFrame({
        '치과': ['합청치과', '홍대치과', '파미에치과'],
        '순위': [1, 3, 10]
    })
    st.bar_chart(chart_data.set_index('치과'))
    
    # 파일 다운로드 테스트
    st.subheader("📄 파일 다운로드 테스트")
    csv = df.to_csv(index=False)
    st.download_button(
        label="📄 CSV 다운로드",
        data=csv,
        file_name=f"테스트_결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main() 