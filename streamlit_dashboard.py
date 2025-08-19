# 스트림릿 종합 데이터 시각화 대시보드
# 작성일: 2025년 8월 19일
# 15주차 클라우드 기반 데이터 시각화 - 스트림릿 구성 요소 실습

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="데이터 시각화 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
.stMetric {
    background-color: #f0f2f6;
    border: 1px solid #e6e9ef;
    padding: 0.5rem;
    border-radius: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

# 데이터 로드 함수
@st.cache_data
def load_data():
    """데이터 로드 및 전처리 함수"""
    data_path = "dataset/"
    
    # ABNB 주식 데이터
    abnb_stock = pd.read_csv(data_path + "ABNB_stock.csv")
    abnb_stock['Date'] = pd.to_datetime(abnb_stock['Date'])
    
    # EV 충전 데이터
    ev_charge = pd.read_csv(data_path + "EV_charge.csv")
    
    # 의료비 데이터
    medical_cost = pd.read_csv(data_path + "medical_cost.csv")
    
    # CO2 배출량 데이터
    co2_data = pd.read_csv(data_path + "CO2_Emissions.csv")
    
    return abnb_stock, ev_charge, medical_cost, co2_data

# 메인 함수
def main():
    # 제목
    st.title("📊 종합 데이터 시각화 대시보드")
    st.markdown("##### 15주차 클라우드 기반 데이터 시각화 - 스트림릿 실습")
    
    # 데이터 로드
    try:
        abnb_stock, ev_charge, medical_cost, co2_data = load_data()
        st.success("데이터 로드 완료! 📈")
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return
    
    # 사이드바 - 전체 설정
    st.sidebar.title("🎛️ 대시보드 설정")
    
    # 페이지 선택
    page = st.sidebar.selectbox(
        "분석할 데이터 선택",
        ["📊 전체 개요", "📈 ABNB 주식", "⚡ EV 충전", "🏥 의료비", "🌱 CO2 배출량", "🔧 스트림릿 구성요소"]
    )
    
    # 페이지별 렌더링
    if page == "📊 전체 개요":
        render_overview(abnb_stock, ev_charge, medical_cost, co2_data)
    elif page == "📈 ABNB 주식":
        render_abnb_analysis(abnb_stock)
    elif page == "⚡ EV 충전":
        render_ev_analysis(ev_charge)
    elif page == "🏥 의료비":
        render_medical_analysis(medical_cost)
    elif page == "🌱 CO2 배출량":
        render_co2_analysis(co2_data)
    elif page == "🔧 스트림릿 구성요소":
        render_streamlit_components()

def render_overview(abnb_stock, ev_charge, medical_cost, co2_data):
    """전체 개요 페이지"""
    st.header("📊 데이터셋 전체 개요")
    
    # 메트릭 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📈 ABNB 주식 데이터",
            f"{len(abnb_stock):,}일",
            f"최신가: ${abnb_stock['Close'].iloc[-1]:.2f}"
        )
    
    with col2:
        st.metric(
            "⚡ EV 충전 세션",
            f"{len(ev_charge):,}건",
            f"총 {ev_charge['kwhTotal'].sum():,.0f} kWh"
        )
    
    with col3:
        st.metric(
            "🏥 의료비 데이터",
            f"{len(medical_cost):,}명",
            f"평균 ${medical_cost['charges'].mean():,.0f}"
        )
    
    with col4:
        st.metric(
            "🌱 CO2 배출량 데이터",
            f"{len(co2_data):,}대",
            f"평균 {co2_data['CO2 Emissions(g/km)'].mean():.0f} g/km"
        )
    
    st.divider()
    
    # 데이터셋 미리보기
    tab1, tab2, tab3, tab4 = st.tabs(["📈 ABNB Stock", "⚡ EV Charge", "🏥 Medical Cost", "🌱 CO2 Emissions"])
    
    with tab1:
        st.subheader("ABNB 주식 데이터 미리보기")
        st.dataframe(abnb_stock.head(), use_container_width=True)
        
        # 간단한 차트
        fig = px.line(abnb_stock, x='Date', y='Close', title='ABNB 주가 추이')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("EV 충전 데이터 미리보기")
        st.dataframe(ev_charge.head(), use_container_width=True)
        
        # 플랫폼별 분포
        platform_counts = ev_charge['platform'].value_counts()
        fig = px.pie(values=platform_counts.values, names=platform_counts.index, 
                     title='플랫폼별 충전 세션 분포')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("의료비 데이터 미리보기")
        st.dataframe(medical_cost.head(), use_container_width=True)
        
        # 흡연 여부별 의료비
        fig = px.box(medical_cost, x='smoker', y='charges', 
                     title='흡연 여부별 의료비 분포')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("CO2 배출량 데이터 미리보기")
        st.dataframe(co2_data.head(), use_container_width=True)
        
        # 제조사별 평균 CO2 배출량
        make_co2_avg = co2_data.groupby('Make')['CO2 Emissions(g/km)'].mean().sort_values().head(10)
        fig = px.bar(x=make_co2_avg.values, y=make_co2_avg.index, 
                     title='친환경 제조사 TOP 10 (낮은 CO2 배출량)',
                     color=make_co2_avg.values,
                     color_continuous_scale='RdYlGn_r')
        fig.update_layout(xaxis_title='평균 CO2 배출량 (g/km)', yaxis_title='제조사')
        st.plotly_chart(fig, use_container_width=True)

def render_abnb_analysis(abnb_stock):
    """ABNB 주식 분석 페이지"""
    st.header("📈 ABNB 주식 데이터 분석")
    
    # 필터링 옵션
    st.sidebar.subheader("📅 기간 설정")
    start_date = st.sidebar.date_input("시작일", abnb_stock['Date'].min().date())
    end_date = st.sidebar.date_input("종료일", abnb_stock['Date'].max().date())
    
    # 데이터 필터링
    filtered_data = abnb_stock[
        (abnb_stock['Date'].dt.date >= start_date) & 
        (abnb_stock['Date'].dt.date <= end_date)
    ]
    
    # 캔들스틱 차트
    fig = go.Figure(data=go.Candlestick(
        x=filtered_data['Date'],
        open=filtered_data['Open'],
        high=filtered_data['High'],
        low=filtered_data['Low'],
        close=filtered_data['Close']
    ))
    
    fig.update_layout(
        title='ABNB 주가 캔들스틱 차트',
        xaxis_title='날짜',
        yaxis_title='주가 ($)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 거래량과 주가 상관관계
    col1, col2 = st.columns(2)
    
    with col1:
        fig_volume = px.bar(filtered_data, x='Date', y='Volume', 
                           title='일별 거래량')
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        # 일일 수익률 계산
        filtered_data = filtered_data.copy()
        filtered_data['Daily_Return'] = filtered_data['Close'].pct_change() * 100
        
        fig_return = px.line(filtered_data, x='Date', y='Daily_Return',
                            title='일일 수익률 (%)')
        fig_return.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_return, use_container_width=True)

def render_ev_analysis(ev_charge):
    """EV 충전 분석 페이지"""
    st.header("⚡ 전기차 충전 패턴 분석")
    
    # 필터링 옵션
    st.sidebar.subheader("🔧 필터 설정")
    min_kwh = st.sidebar.slider("최소 충전량 (kWh)", 0.0, float(ev_charge['kwhTotal'].max()), 0.0)
    selected_platform = st.sidebar.multiselect(
        "플랫폼 선택",
        ev_charge['platform'].unique(),
        default=ev_charge['platform'].unique()
    )
    
    # 데이터 필터링
    filtered_data = ev_charge[
        (ev_charge['kwhTotal'] >= min_kwh) &
        (ev_charge['platform'].isin(selected_platform))
    ]
    
    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 세션 수", f"{len(filtered_data):,}")
    with col2:
        st.metric("총 충전량", f"{filtered_data['kwhTotal'].sum():,.1f} kWh")
    with col3:
        st.metric("평균 충전량", f"{filtered_data['kwhTotal'].mean():.2f} kWh")
    with col4:
        st.metric("평균 충전시간", f"{filtered_data['chargeTimeHrs'].mean():.2f} 시간")
    
    # 시각화
    tab1, tab2, tab3 = st.tabs(["📊 기본 분석", "⏰ 시간 패턴", "📍 위치 분석"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(filtered_data, x='kwhTotal', nbins=30,
                               title='충전량 분포')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.scatter(filtered_data, x='chargeTimeHrs', y='kwhTotal',
                             color='platform', title='충전시간 vs 충전량')
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # 요일별 패턴
        weekdays = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        weekday_data = []
        for day in weekdays:
            count = filtered_data[day].sum()
            weekday_data.append({'Day': day, 'Sessions': count})
        
        weekday_df = pd.DataFrame(weekday_data)
        fig3 = px.bar(weekday_df, x='Day', y='Sessions',
                     title='요일별 충전 세션 수')
        st.plotly_chart(fig3, use_container_width=True)
        
        # 시간대별 패턴
        hourly_data = filtered_data['startTime'].value_counts().sort_index().reset_index()
        hourly_data.columns = ['Hour', 'Sessions']
        
        fig4 = px.line(hourly_data, x='Hour', y='Sessions',
                      title='시간대별 충전 시작 패턴', markers=True)
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        # 위치별 통계
        location_stats = filtered_data.groupby('locationId').agg({
            'kwhTotal': ['sum', 'mean', 'count']
        }).round(2)
        
        location_stats.columns = ['총_충전량', '평균_충전량', '세션_수']
        location_stats = location_stats.sort_values('세션_수', ascending=False)
        
        st.subheader("위치별 충전 통계 (상위 20개)")
        st.dataframe(location_stats.head(20), use_container_width=True)

def render_medical_analysis(medical_cost):
    """의료비 분석 페이지"""
    st.header("🏥 의료비 영향 요인 분석")
    
    # 필터링 옵션
    st.sidebar.subheader("👥 인구통계학적 필터")
    age_range = st.sidebar.slider("나이 범위", 18, 64, (18, 64))
    gender_filter = st.sidebar.multiselect("성별", ['male', 'female'], default=['male', 'female'])
    smoker_filter = st.sidebar.multiselect("흡연 여부", ['yes', 'no'], default=['yes', 'no'])
    region_filter = st.sidebar.multiselect(
        "지역", medical_cost['region'].unique(), default=medical_cost['region'].unique()
    )
    
    # 데이터 필터링
    filtered_data = medical_cost[
        (medical_cost['age'].between(age_range[0], age_range[1])) &
        (medical_cost['sex'].isin(gender_filter)) &
        (medical_cost['smoker'].isin(smoker_filter)) &
        (medical_cost['region'].isin(region_filter))
    ]
    
    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_cost = filtered_data['charges'].mean()
        st.metric("평균 의료비", f"${avg_cost:,.0f}")
    with col2:
        median_cost = filtered_data['charges'].median()
        st.metric("중앙값", f"${median_cost:,.0f}")
    with col3:
        total_patients = len(filtered_data)
        st.metric("환자 수", f"{total_patients:,}명")
    with col4:
        smoker_ratio = filtered_data['smoker'].value_counts().get('yes', 0) / len(filtered_data) * 100
        st.metric("흡연자 비율", f"{smoker_ratio:.1f}%")
    
    # 시각화 탭
    tab1, tab2, tab3, tab4 = st.tabs(["📊 분포 분석", "🔍 요인 분석", "📈 상관관계", "🎯 예측"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(filtered_data, x='charges', nbins=30,
                               title='의료비 분포')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.histogram(filtered_data, x='age', nbins=20,
                               title='나이 분포')
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # 흡연 여부별 의료비
        fig3 = px.box(filtered_data, x='smoker', y='charges', color='smoker',
                     title='흡연 여부별 의료비 분포')
        st.plotly_chart(fig3, use_container_width=True)
        
        # 나이 vs 의료비
        fig4 = px.scatter(filtered_data, x='age', y='charges', color='smoker',
                         size='bmi', title='나이 vs 의료비 (흡연 여부별)',
                         hover_data=['sex', 'children', 'region'])
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        # BMI vs 의료비
        fig5 = px.scatter(filtered_data, x='bmi', y='charges', color='sex',
                         facet_col='smoker', title='BMI vs 의료비 (성별 및 흡연 여부별)',
                         trendline='ols')
        st.plotly_chart(fig5, use_container_width=True)
    
    with tab4:
        st.subheader("🤖 간단한 의료비 예측")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            input_age = st.number_input("나이", 18, 100, 30)
            input_sex = st.selectbox("성별", ['male', 'female'])
        
        with col2:
            input_bmi = st.number_input("BMI", 15.0, 50.0, 25.0)
            input_children = st.number_input("자녀 수", 0, 10, 0)
        
        with col3:
            input_smoker = st.selectbox("흡연 여부", ['no', 'yes'])
            input_region = st.selectbox("지역", medical_cost['region'].unique())
        
        if st.button("의료비 예측하기", type="primary"):
            # 간단한 규칙 기반 예측
            base_cost = 3000
            age_factor = input_age * 50
            bmi_factor = max(0, (input_bmi - 30) * 200)
            smoking_factor = 20000 if input_smoker == 'yes' else 0
            children_factor = input_children * 500
            
            predicted_cost = base_cost + age_factor + bmi_factor + smoking_factor + children_factor
            
            st.success(f"예상 의료비: ${predicted_cost:,.0f}")
            
            # 유사 데이터와 비교
            similar_data = filtered_data[
                (abs(filtered_data['age'] - input_age) <= 5) &
                (filtered_data['sex'] == input_sex) &
                (filtered_data['smoker'] == input_smoker)
            ]
            
            if len(similar_data) > 0:
                avg_similar = similar_data['charges'].mean()
                st.info(f"유사한 조건의 평균 의료비: ${avg_similar:,.0f}")

def render_streamlit_components():
    """스트림릿 구성요소 실습 페이지"""
    st.header("🔧 스트림릿 구성요소 실습")
    
    # 텍스트 요소
    st.subheader("📝 텍스트 출력 요소")
    
    with st.expander("텍스트 요소 예제 보기"):
        st.title("제목 (st.title)")
        st.header("헤더 (st.header)")
        st.subheader("서브헤더 (st.subheader)")
        
        st.markdown("""
        **마크다운 텍스트 (st.markdown)**
        - :red[빨간색] 텍스트
        - :blue[파란색] 텍스트
        - :green[초록색] 텍스트
        """)
        
        st.text("일반 텍스트 (st.text)")
        
        st.code("""
        # 코드 블록 (st.code)
        import streamlit as st
        st.write("Hello, Streamlit!")
        """, language='python')
    
    st.divider()
    
    # 입력 위젯
    st.subheader("🎛️ 사용자 입력 위젯")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**버튼 및 선택**")
        if st.button("클릭하세요!"):
            st.balloons()
        
        checkbox_val = st.checkbox("체크박스")
        if checkbox_val:
            st.write("체크되었습니다!")
        
        radio_val = st.radio("라디오 버튼", ["옵션 1", "옵션 2", "옵션 3"])
        st.write(f"선택: {radio_val}")
    
    with col2:
        st.write("**선택 및 입력**")
        selectbox_val = st.selectbox("선택박스", ["선택 1", "선택 2", "선택 3"])
        
        multiselect_val = st.multiselect("다중 선택", ["A", "B", "C", "D"])
        st.write(f"선택된 항목: {multiselect_val}")
        
        text_val = st.text_input("텍스트 입력", placeholder="여기에 입력하세요")
        if text_val:
            st.write(f"입력값: {text_val}")
    
    with col3:
        st.write("**숫자 및 범위**")
        number_val = st.number_input("숫자 입력", 0, 100, 50)
        st.write(f"숫자: {number_val}")
        
        slider_val = st.slider("슬라이더", 0, 100, 25)
        st.write(f"슬라이더 값: {slider_val}")
        
        range_val = st.slider("범위 슬라이더", 0, 100, (20, 80))
        st.write(f"범위: {range_val}")
    
    st.divider()
    
    # 데이터 표시
    st.subheader("📊 데이터 표시 요소")
    
    # 샘플 데이터 생성
    sample_data = pd.DataFrame({
        '이름': ['김철수', '이영희', '박민수', '정지원'],
        '나이': [25, 30, 35, 28],
        '점수': [85, 92, 78, 88],
        '등급': ['B', 'A', 'C', 'B']
    })
    
    tab1, tab2, tab3 = st.tabs(["📋 표", "📈 메트릭", "💾 JSON"])
    
    with tab1:
        st.write("**정적 테이블 (st.table)**")
        st.table(sample_data)
        
        st.write("**인터랙티브 데이터프레임 (st.dataframe)**")
        st.dataframe(sample_data, use_container_width=True)
    
    with tab2:
        st.write("**메트릭 카드 (st.metric)**")
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("평균 점수", f"{sample_data['점수'].mean():.1f}", "3.2")
        
        with metric_col2:
            st.metric("총 인원", f"{len(sample_data)}명", "1")
        
        with metric_col3:
            st.metric("최고 점수", f"{sample_data['점수'].max()}", "5")
    
    with tab3:
        st.write("**JSON 데이터 (st.json)**")
        
        json_data = {
            "project": "Streamlit Dashboard",
            "version": "1.0.0",
            "author": "Data Scientist",
            "features": [
                "Interactive Widgets",
                "Data Visualization",
                "Real-time Updates"
            ],
            "config": {
                "theme": "light",
                "layout": "wide"
            }
        }
        
        st.json(json_data)
    
    st.divider()
    
    # 레이아웃
    st.subheader("📐 레이아웃 구성")
    
    with st.expander("컬럼 레이아웃 예제"):
        layout_col1, layout_col2, layout_col3 = st.columns([2, 1, 1])
        
        with layout_col1:
            st.write("**넓은 컬럼 (2:1:1 비율)**")
            st.info("이 컬럼은 다른 컬럼의 2배 크기입니다.")
        
        with layout_col2:
            st.write("**컬럼 2**")
            st.success("성공!")
        
        with layout_col3:
            st.write("**컬럼 3**")
            st.warning("주의!")
    
    # 상태 관리 예제
    st.subheader("🔄 상태 관리 (Session State)")
    
    with st.expander("카운터 예제"):
        if 'counter' not in st.session_state:
            st.session_state.counter = 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("+ 1"):
                st.session_state.counter += 1
        
        with col2:
            st.write(f"**카운트: {st.session_state.counter}**")
        
        with col3:
            if st.button("리셋"):
                st.session_state.counter = 0

# 애플리케이션 실행
if __name__ == "__main__":
    main()