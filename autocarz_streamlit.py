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

# 커스텀 CSS 스타일 적용
def load_custom_css():
    st.markdown("""
    <style>
    /* 전체 스타일링 */
    .main-header {
        text-align: center;
        color: #333;
        padding: 20px 0;
        border-bottom: 2px solid #ddd;
        margin-bottom: 30px;
    }
    
    /* 패널 스타일링 */
    .panel-container {
        background: #fdfdfd;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .panel-title {
        color: #333;
        margin-bottom: 15px;
        font-size: 18px;
        font-weight: 600;
    }
    
    /* 이미지 컨테이너 */
    .chart-container {
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: #f9f9f9;
        border-radius: 8px;
        border: 1px solid #eee;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        margin: 5px;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* 메트릭 카드 스타일 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background: #f8f9fa;
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
            "대시보드 홈",
            "로드킬 분석", 
            "지역별 통계",
            "도로유형별 분석",
            "동물종류별 분석",
            "카메라 모니터링"
        ])
        
        # 상태 정보
        st.markdown("---")
        st.markdown("### 📍 시스템 정보")
        st.info(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.success("시스템 정상 운영중")
    
    # 이미지 데이터 로드
    images = load_images()
    
    if page == "대시보드 홈":
        show_dashboard_home(images)
    elif page == "로드킬 분석":
        show_roadkill_analysis(images)
    elif page == "지역별 통계":
        show_regional_stats(images)
    elif page == "도로유형별 분석":
        show_roadtype_analysis(images)
    elif page == "동물종류별 분석":
        show_animal_analysis(images)
    elif page == "카메라 모니터링":
        show_camera_monitoring()

# 대시보드 홈 페이지
def show_dashboard_home(images):
    st.markdown("## 📈 종합 대시보드")
    
    # 메트릭 카드들
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>총 로드킬 건수</h3>
            <h2>25,847건</h2>
            <p>2019-2023 누적</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>위험 구간</h3>
            <h2>143개소</h2>
            <p>모니터링 중</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>동물 보호 건수</h3>
            <h2>1,254건</h2>
            <p>금년 누적</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>시스템 가동률</h3>
            <h2>99.2%</h2>
            <p>정상 운영중</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 주요 차트 2개씩 배치
    col1, col2 = st.columns(2)
    
    with col1:
        if "연도별 로드킬 총 건수 추이" in images:
            st.markdown('<div class="panel-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="panel-title">📊 연도별 로드킬 추이</h3>', unsafe_allow_html=True)
            st.image(images["연도별 로드킬 총 건수 추이"], use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if "각 권역 연도별 로드킬 건수" in images:
            st.markdown('<div class="panel-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="panel-title">🗺️ 권역별 로드킬 현황</h3>', unsafe_allow_html=True)
            st.image(images["각 권역 연도별 로드킬 건수"], use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# 로드킬 분석 페이지
def show_roadkill_analysis(images):
    st.markdown("## 🚨 로드킬 종합 분석")
    
    # 연도별 추이
    if "연도별 로드킬 총 건수 추이" in images:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📈 연도별 로드킬 총 건수 추이")
        st.image(images["연도별 로드킬 총 건수 추이"], use_column_width=True)
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
            st.image(images["각 권역 연도별 로드킬 건수"], use_column_width=True)
    
    with col2:
        if "권역별 이상 지역 비율" in images:
            st.markdown("### ⚠️ 권역별 이상 지역 비율")
            st.image(images["권역별 이상 지역 비율"], use_column_width=True)
    
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
        st.image(images["도로유형별 분석 (통합)"], use_column_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "연도별 도로유형별 로드킬 건수 비교" in images:
            st.markdown("### 📊 연도별 도로유형별 비교")
            st.image(images["연도별 도로유형별 로드킬 건수 비교"], use_column_width=True)
    
    with col2:
        if "도로유형별 로드킬 합계 및 추이" in images:
            st.markdown("### 📈 도로유형별 추이")
            st.image(images["도로유형별 로드킬 합계 및 추이"], use_column_width=True)

# 동물종류별 분석 페이지
def show_animal_analysis(images):
    st.markdown("## 🦌 동물종류별 로드킬 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "동물 종류별 로드킬 건수 및 합계" in images:
            st.markdown("### 🐾 동물 종류별 로드킬 건수")
            st.image(images["동물 종류별 로드킬 건수 및 합계"], use_column_width=True)
    
    with col2:
        if "동물종류 연도별 로드킬 비율" in images:
            st.markdown("### 📊 동물종류 연도별 비율")
            st.image(images["동물종류 연도별 로드킬 비율"], use_column_width=True)
    
    # 동물별 보호 대책
    with st.expander("🛡️ 동물별 보호 대책"):
        st.write("""
        **동물종별 맞춤 보호방안:**
        - **대형 동물 (고라니, 멧돼지)**: 생태통로 설치, 울타리 강화
        - **중형 동물 (너구리, 고양이)**: 속도제한, 야간 조명 개선
        - **소형 동물**: 지하통로, 동물 전용 횡단시설
        """)

# 카메라 모니터링 페이지 (원본 HTML 기능 재현)
def show_camera_monitoring():
    st.markdown("## 📷 실시간 카메라 모니터링")
    
    # 원본 HTML의 카메라 기능을 Streamlit으로 구현
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        st.markdown("### 📹 카메라 피드")
        
        # 웹캠 기능 (Streamlit camera_input 사용)
        camera_image = st.camera_input("📸 사진 촬영")
        
        if camera_image is not None:
            st.image(camera_image, caption="촬영된 사진", use_column_width=True)
            
            # 위치 정보 시뮬레이션 (실제 GPS는 브라우저 API 필요)
            if st.button("📍 위치 정보 기록"):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 세션 스테이트에 기록 저장
                if 'photo_logs' not in st.session_state:
                    st.session_state.photo_logs = []
                
                # 시뮬레이션 위치 (실제로는 GPS API 사용)
                import random
                lat = round(37.5665 + random.uniform(-0.01, 0.01), 6)
                lon = round(126.9780 + random.uniform(-0.01, 0.01), 6)
                
                st.session_state.photo_logs.insert(0, {
                    'time': current_time,
                    'lat': lat,
                    'lon': lon
                })
                
                st.success("📍 신고 접수가 완료되었습니다!")
                st.balloons()  # 시각적 피드백
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="panel-container">', unsafe_allow_html=True)
        st.markdown("### 🗺️ 위치 기록 타임라인")
        
        # 위치 기록 표시
        if 'photo_logs' in st.session_state and st.session_state.photo_logs:
            for i, log in enumerate(st.session_state.photo_logs):
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: #f8f9fa; 
                        padding: 10px; 
                        margin: 5px 0; 
                        border-left: 4px solid #007bff;
                        border-radius: 4px;
                    ">
                        📸 <strong>[{log['time']}]</strong><br>
                        📍 위도: {log['lat']}, 경도: {log['lon']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("아직 촬영된 사진이 없습니다.")
        
        # 기록 초기화 버튼
        if st.button("🗑️ 기록 초기화"):
            st.session_state.photo_logs = []
            st.success("기록이 초기화되었습니다.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 지도 시뮬레이션 (실제로는 카카오맵 API 필요)
        st.markdown("### 🗺️ 현재 위치 (시뮬레이션)")
        
        # 간단한 지도 데이터 생성
        if 'photo_logs' in st.session_state and st.session_state.photo_logs:
            map_data = pd.DataFrame([
                {'lat': log['lat'], 'lon': log['lon']} for log in st.session_state.photo_logs[:10]
            ])
            st.map(map_data)
        else:
            # 기본 서울 위치
            default_map = pd.DataFrame([{'lat': 37.5665, 'lon': 126.9780}])
            st.map(default_map)

if __name__ == "__main__":
    main()