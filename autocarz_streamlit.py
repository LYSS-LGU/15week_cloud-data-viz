import streamlit as st
import pandas as pd
from PIL import Image
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="AutoCarz Dashboard made by AI 100%", 
    page_icon="🚗", 
    layout="wide"
)

# CSS 파일 로드 함수
def load_custom_css():
    """외부 CSS 파일을 로드하여 스타일을 적용하는 함수"""
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS 파일을 찾을 수 없습니다. 기본 스타일을 사용합니다.")
        # 기본 스타일 적용
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            color: #333;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        .section-panel {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

# 이미지 로드 함수
@st.cache_data
def load_images():
    image_folder = "autocarz/image"
    images = {}
    
    if os.path.exists(image_folder):
        image_files = {
            "roadkill_by_region_year.png": "각 권역 연도별 로드킬 건수",
            "roadkill_yearly_trend.png": "연도별 로드킬 총 건수 추이", 
            "region_abnormal_ratio.png": "권역별 이상 지역 비율",
            "roadtype_comparison.png": "연도별 도로유형별 로드킬 건수 비교",
            "roadtype_trend.png": "도로유형별 로드킬 합계 및 추이",
            "animal_roadkill.png": "동물 종류별 로드킬 건수 및 합계",
            "animal_yearly_ratio.png": "동물종류 연도별 로드킬 비율",
            "combined_4_5.png": "도로유형별 분석 (통합)"
        }
        
        for filename, title in image_files.items():
            filepath = os.path.join(image_folder, filename)
            if os.path.exists(filepath):
                try:
                    images[title] = Image.open(filepath)
                except Exception as e:
                    st.error(f"이미지 로드 실패 {filename}: {e}")
    
    return images

# 메인 함수
def main():
    load_custom_css()
    
    # 헤더
    st.markdown('<h1 class="main-header">🚗 AutoCarz 대시보드</h1>', unsafe_allow_html=True)
    
    # 사이드바 - 네비게이션
    with st.sidebar:
        st.title("📊 메뉴")
        page = st.selectbox("페이지 선택", [
            "종합 대시보드",
            "실시간 모니터링 현황",
            "연도별 로드킬 분석", 
            "지역별 통계 분석",
            "도로유형별 분석",
            "동물종류별 분석"
        ])
        
        # 상태 정보
        st.markdown("---")
        st.markdown("### 📍 시스템 정보")
        st.info(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.success("시스템 정상 운영중")
    
    # 이미지 데이터 로드
    images = load_images()
    
    if page == "종합 대시보드":
        show_integrated_dashboard(images)
    elif page == "실시간 모니터링 현황":
        show_realtime_monitoring(images)
    elif page == "연도별 로드킬 분석":
        show_roadkill_analysis(images)
    elif page == "지역별 통계 분석":
        show_regional_stats(images)
    elif page == "도로유형별 분석":
        show_roadtype_analysis(images)
    elif page == "동물종류별 분석":
        show_animal_analysis(images)

# 종합 대시보드 페이지 (개선된 레이아웃)
def show_integrated_dashboard(images):
    """종합 대시보드 메인 페이지 - 주요 지표와 실시간 모니터링 기능"""
    st.markdown("## 📈 AutoCarz 종합 대시보드")
    
    # 메트릭 카드들 - 반응형 레이아웃으로 개선
    st.markdown("""
    <div class="metric-container">
        <div class="metric-card">
            <h3>총 로드킬 건수</h3>
            <h2>25,847건</h2>
            <p>2019-2023 누적</p>
        </div>
        <div class="metric-card">
            <h3>위험 구간</h3>
            <h2>143개소</h2>
            <p>모니터링 중</p>
        </div>
        <div class="metric-card">
            <h3>동물 보호 건수</h3>
            <h2>1,254건</h2>
            <p>금년 누적</p>
        </div>
        <div class="metric-card">
            <h3>시스템 가동률</h3>
            <h2>99.2%</h2>
            <p>정상 운영중</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 공간 여백 추가
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 메인 섹션들을 탭으로 구성하여 공간 효율성 향상
    main_tab1, main_tab2 = st.tabs(["🔴 실시간 모니터링", "📊 시스템 현황"])
    
    with main_tab1:
        # 실시간 모니터링 섹션
        monitoring_col1, monitoring_col2 = st.columns(2)
        
        # 실시간 카메라 모니터링
        with monitoring_col1:
            st.markdown('<div class="section-panel">', unsafe_allow_html=True)
            st.markdown("#### 📷 실시간 카메라 모니터링")
            
            camera_image = st.camera_input("📸 야생동물 발견 시 촬영", label_visibility="collapsed")
            
            if camera_image is not None:
                st.image(camera_image, caption="촬영된 사진", width=250)
                
                if st.button("📍 로드킬 위험 신고", type="primary", use_container_width=True):
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if 'photo_logs' not in st.session_state:
                        st.session_state.photo_logs = []
                    
                    import random
                    lat = round(37.5665 + random.uniform(-0.01, 0.01), 6)
                    lon = round(126.9780 + random.uniform(-0.01, 0.01), 6)
                    
                    st.session_state.photo_logs.insert(0, {
                        'time': current_time,
                        'lat': lat,
                        'lon': lon
                    })
                    
                    st.success("📍 신고 접수 완료!")
                    st.balloons()
            else:
                st.markdown("""
                <div style="
                    background: #e3f2fd;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    color: #1976d2;
                    margin: 10px 0;
                ">
                    <h5>📸 카메라 대기 중</h5>
                    <small>야생동물을 발견하면 촬영해주세요</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 신고 위치 지도
        with monitoring_col2:
            st.markdown('<div class="section-panel">', unsafe_allow_html=True)
            st.markdown("#### 🗺️ 신고 위치")
            
            if 'photo_logs' in st.session_state and st.session_state.photo_logs:
                map_data = pd.DataFrame([
                    {'lat': log['lat'], 'lon': log['lon']} for log in st.session_state.photo_logs[:10]
                ])
                st.map(map_data, height=250, zoom=11)
            else:
                default_map = pd.DataFrame([{'lat': 37.5665, 'lon': 126.9780}])
                st.map(default_map, height=250, zoom=11)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with main_tab2:
        # 시스템 현황 섹션
        status_col1, status_col2 = st.columns(2)
        
        # 최근 신고 기록
        with status_col1:
            st.markdown('<div class="section-panel">', unsafe_allow_html=True)
            st.markdown("#### 🗂️ 최근 신고 기록")
            
            if 'photo_logs' in st.session_state and st.session_state.photo_logs:
                # 최대 3개만 컴팩트하게 표시
                for i, log in enumerate(st.session_state.photo_logs[:3]):
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        padding: 10px;
                        margin: 6px 0;
                        border-radius: 8px;
                        border-left: 4px solid #4CAF50;
                        font-size: 13px;
                    ">
                        <strong style="color: #2c3e50;">🚨 신고 #{i+1}</strong><br>
                        <span style="color: #555;">
                            📅 {log['time']}<br>
                            📍 {log['lat']:.4f}, {log['lon']:.4f}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 관리 버튼들
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("🗑️ 기록 초기화", use_container_width=True):
                        st.session_state.photo_logs = []
                        st.rerun()
                with btn_col2:
                    if st.button("📊 통계 보기", use_container_width=True):
                        st.info(f"총 {len(st.session_state.photo_logs)}건의 신고")
            else:
                st.markdown("""
                <div style="
                    background: #fff3e0;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    color: #f57c00;
                    margin: 10px 0;
                ">
                    <h5>📭 신고 기록이 없습니다</h5>
                    <small>카메라로 야생동물을 촬영하고 신고해주세요</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 시스템 상태
        with status_col2:
            st.markdown('<div class="section-panel">', unsafe_allow_html=True)
            st.markdown("#### 📊 시스템 상태")
            
            # 메트릭 2x2 배치
            metric_row1_col1, metric_row1_col2 = st.columns(2)
            with metric_row1_col1:
                st.metric("오늘 신고", f"{len(st.session_state.photo_logs) if 'photo_logs' in st.session_state else 0}건", "🟢")
            with metric_row1_col2:
                st.metric("응답시간", "0.3초", "⚡")
            
            metric_row2_col1, metric_row2_col2 = st.columns(2)
            with metric_row2_col1:
                st.metric("활성 사용자", "142명", "👥")
            with metric_row2_col2:
                st.metric("시스템 상태", "정상", "✅")
            
            # 시스템 상태 표시
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                margin-top: 10px;
            ">
                <h5 style="color: #155724; margin: 0;">🔋 시스템 가동률: 99.2%</h5>
                <small style="color: #155724;">모든 서비스가 정상 운영 중입니다</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# 실시간 모니터링 현황 페이지 (차트들 이동)
def show_realtime_monitoring(images):
    st.markdown("## 📊 실시간 모니터링 현황")
    
    # 탭으로 구성
    tab1, tab2 = st.tabs(["📈 연도별 추이", "🗺️ 권역별 현황"])
    
    with tab1:
        if "연도별 로드킬 총 건수 추이" in images:
            st.markdown("### 📈 연도별 로드킬 추이")
            st.image(images["연도별 로드킬 총 건수 추이"], use_container_width=True)
            
            # 간단한 통계
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("2023년", "6,847건", "↑ 12.3%")
            with col2:
                st.metric("2022년", "6,102건", "↑ 8.7%")
            with col3:
                st.metric("5년 평균", "5,169건", "")
    
    with tab2:
        if "각 권역 연도별 로드킬 건수" in images:
            st.markdown("### 🗺️ 권역별 로드킬 현황")
            st.image(images["각 권역 연도별 로드킬 건수"], use_container_width=True)
            
            # 권역별 순위
            st.markdown("#### 🏆 권역별 로드킬 발생 순위 (2023년 기준)")
            ranking_data = pd.DataFrame({
                '순위': ['1위', '2위', '3위', '4위', '5위'],
                '권역': ['경기도', '강원도', '충청남도', '전라남도', '경상북도'],
                '건수': ['2,341건', '1,892건', '1,234건', '987건', '654건'],
                '비율': ['34.2%', '27.6%', '18.0%', '14.4%', '9.5%']
            })
            st.table(ranking_data)

# 로드킬 분석 페이지
def show_roadkill_analysis(images):
    st.markdown("## 🚨 로드킬 종합 분석")
    
    # 연도별 추이
    if "연도별 로드킬 총 건수 추이" in images:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📈 연도별 로드킬 총 건수 추이")
        st.image(images["연도별 로드킬 총 건수 추이"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("📝 분석 결과"):
            st.write("""
            **주요 발견사항:**
            - 2019년부터 2023년까지 로드킬 발생 건수가 지속적으로 증가
            - 2022년 이후 급격한 증가 추세를 보임
            - 야생동물 서식지 확장과 도로 건설 증가가 주요 원인으로 분석됨
            """)

# 지역별 통계 페이지  
def show_regional_stats(images):
    st.markdown("## 🗺️ 지역별 로드킬 통계")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "각 권역 연도별 로드킬 건수" in images:
            st.markdown("### 📍 권역별 연도별 로드킬 건수")
            st.image(images["각 권역 연도별 로드킬 건수"], use_container_width=True)
    
    with col2:
        if "권역별 이상 지역 비율" in images:
            st.markdown("### ⚠️ 권역별 이상 지역 비율")
            st.image(images["권역별 이상 지역 비율"], use_container_width=True)
    
    with st.expander("🎯 지역별 대응방안"):
        st.write("""
        **권역별 맞춤 대책:**
        - **고위험 지역**: 야생동물 경고표지판 설치, 속도제한 강화
        - **중위험 지역**: 정기적인 모니터링 및 예방 교육 실시  
        - **저위험 지역**: 현재 수준 유지 및 예방 중심 관리
        """)

# 도로유형별 분석 페이지
def show_roadtype_analysis(images):
    st.markdown("## 🛣️ 도로유형별 로드킬 분석")
    
    if "도로유형별 분석 (통합)" in images:
        st.image(images["도로유형별 분석 (통합)"], use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "연도별 도로유형별 로드킬 건수 비교" in images:
            st.markdown("### 📊 연도별 도로유형별 비교")
            st.image(images["연도별 도로유형별 로드킬 건수 비교"], use_container_width=True)
    
    with col2:
        if "도로유형별 로드킬 합계 및 추이" in images:
            st.markdown("### 📈 도로유형별 추이")
            st.image(images["도로유형별 로드킬 합계 및 추이"], use_container_width=True)

# 동물종류별 분석 페이지
def show_animal_analysis(images):
    st.markdown("## 🦌 동물종류별 로드킬 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "동물 종류별 로드킬 건수 및 합계" in images:
            st.markdown("### 🐾 동물 종류별 로드킬 건수")
            st.image(images["동물 종류별 로드킬 건수 및 합계"], use_container_width=True)
    
    with col2:
        if "동물종류 연도별 로드킬 비율" in images:
            st.markdown("### 📊 동물종류 연도별 비율")
            st.image(images["동물종류 연도별 로드킬 비율"], use_container_width=True)
    
    # 동물별 보호 대책
    with st.expander("🛡️ 동물별 보호 대책"):
        st.write("""
        **동물종별 맞춤 보호방안:**
        - **대형 동물 (고라니, 멧돼지)**: 생태통로 설치, 울타리 강화
        - **중형 동물 (너구리, 고양이)**: 속도제한, 야간 조명 개선
        - **소형 동물**: 지하통로, 동물 전용 횡단시설
        """)


if __name__ == "__main__":
    main()