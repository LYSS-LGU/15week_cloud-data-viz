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
    
    # Covid19 인도 데이터 추가
    covid_india = pd.read_csv(data_path + "Covid19-India.csv")
    covid_india['date'] = pd.to_datetime(covid_india['date'])
    
    # 제품 검사 데이터 추가
    product_inspection = pd.read_csv(data_path + "product_inspection.csv")
    product_inspection['date'] = pd.to_datetime(product_inspection['date'])
    
    return abnb_stock, ev_charge, medical_cost, co2_data, covid_india, product_inspection

# 메인 함수
def main():
    # 제목
    st.title("📊 종합 데이터 시각화 대시보드")
    st.markdown("##### 15주차 클라우드 기반 데이터 시각화 - 스트림릿 실습")
    
    # 데이터 로드
    try:
        abnb_stock, ev_charge, medical_cost, co2_data, covid_india, product_inspection = load_data()
        st.success("데이터 로드 완료! 📈")
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return
    
    # 사이드바 - 전체 설정
    st.sidebar.title("🎛️ 대시보드 설정")
    
    # 페이지 선택
    page = st.sidebar.selectbox(
        "분석할 데이터 선택",
        ["📊 전체 개요", "📈 ABNB 주식", "⚡ EV 충전", "🏥 의료비", "🌱 CO2 배출량", 
         "🦠 Covid-19 인도", "🏭 제품 검사", "🔧 스트림릿 구성요소"]
    )
    
    # 페이지별 렌더링
    if page == "📊 전체 개요":
        render_overview(abnb_stock, ev_charge, medical_cost, co2_data, covid_india, product_inspection)
    elif page == "📈 ABNB 주식":
        render_abnb_analysis(abnb_stock)
    elif page == "⚡ EV 충전":
        render_ev_analysis(ev_charge)
    elif page == "🏥 의료비":
        render_medical_analysis(medical_cost)
    elif page == "🌱 CO2 배출량":
        render_co2_analysis(co2_data)
    elif page == "🦠 Covid-19 인도":
        render_covid_analysis(covid_india)
    elif page == "🏭 제품 검사":
        render_product_inspection(product_inspection)
    elif page == "🔧 스트림릿 구성요소":
        render_streamlit_components()

def render_overview(abnb_stock, ev_charge, medical_cost, co2_data, covid_india, product_inspection):
    """전체 개요 페이지"""
    st.header("📊 데이터셋 전체 개요")
    
    # 첫 번째 줄 메트릭 카드
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
    
    # 두 번째 줄 메트릭 카드 추가
    col5, col6, _, _ = st.columns(4)
    
    with col5:
        st.metric(
            "🦠 Covid-19 인도 데이터",
            f"{len(covid_india):,}건",
            f"총 {covid_india['region'].nunique()} 지역"
        )
    
    with col6:
        st.metric(
            "🏭 제품 검사 데이터",
            f"{len(product_inspection):,}건",
            f"{product_inspection['inspection_step'].nunique()} 검사 단계"
        )
    
    st.divider()
    
    # 데이터셋 미리보기
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📈 ABNB Stock", "⚡ EV Charge", "🏥 Medical Cost", "🌱 CO2 Emissions", 
         "🦠 Covid-19", "🏭 Product Inspection"]
    )
    
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
    
    with tab5:
        st.subheader("Covid-19 인도 데이터 미리보기")
        st.dataframe(covid_india.head(), use_container_width=True)
        
        # 지역별 최신 확진자 수 상위 10개 지역 
        latest_date = covid_india['date'].max()
        latest_data = covid_india[covid_india['date'] == latest_date]
        top_regions = latest_data.nlargest(10, 'confirmed')
        
        fig = px.bar(top_regions, x='confirmed', y='region',
                     title=f'최신 확진자 수 상위 10개 지역 ({latest_date.strftime("%Y-%m-%d")})',
                     color='confirmed',
                     color_continuous_scale='Reds')
        fig.update_layout(xaxis_title='확진자 수', yaxis_title='지역')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab6:
        st.subheader("제품 검사 데이터 미리보기")
        st.dataframe(product_inspection.head(), use_container_width=True)
        
        # 검사 단계별 측정값 분포
        fig = px.box(product_inspection, x='inspection_step', y='value',
                     title='검사 단계별 측정값 분포')
        fig.add_hline(y=product_inspection['target'].iloc[0], line_dash="dash", 
                     line_color="green", annotation_text="Target")
        fig.add_hline(y=product_inspection['upper_spec'].iloc[0], line_dash="dash", 
                     line_color="red", annotation_text="Upper Spec")
        fig.add_hline(y=product_inspection['lower_spec'].iloc[0], line_dash="dash", 
                     line_color="red", annotation_text="Lower Spec")
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

def render_covid_analysis(covid_india):
    """Covid-19 인도 데이터 분석 페이지"""
    st.header("🦠 Covid-19 인도 데이터 분석")
    
    # 필터링 옵션
    st.sidebar.subheader("📅 기간 및 지역 설정")
    
    # 날짜 필터
    start_date = st.sidebar.date_input("시작일", covid_india['date'].min().date())
    end_date = st.sidebar.date_input("종료일", covid_india['date'].max().date())
    
    # 지역 필터
    all_regions = covid_india['region'].unique()
    selected_regions = st.sidebar.multiselect(
        "지역 선택 (최대 10개)",
        all_regions,
        default=all_regions[:5]
    )
    
    # 데이터 필터링
    filtered_data = covid_india[
        (covid_india['date'].dt.date >= start_date) & 
        (covid_india['date'].dt.date <= end_date) &
        (covid_india['region'].isin(selected_regions))
    ]
    
    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)
    
    latest_date = filtered_data['date'].max()
    latest_data = filtered_data[filtered_data['date'] == latest_date]
    
    with col1:
        total_confirmed = latest_data['confirmed'].sum()
        st.metric("총 확진자", f"{total_confirmed:,}명")
    
    with col2:
        total_active = latest_data['active'].sum()
        st.metric("활성 환자", f"{total_active:,}명")
    
    with col3:
        total_cured = latest_data['cured'].sum()
        st.metric("완치자", f"{total_cured:,}명")
    
    with col4:
        total_deaths = latest_data['deaths'].sum()
        st.metric("사망자", f"{total_deaths:,}명")
    
    st.divider()
    
    # 시각화 탭
    tab1, tab2, tab3, tab4 = st.tabs(["📈 시계열 분석", "📊 지역별 비교", "🗺️ 현황 대시보드", "📊 증가율 분석"])
    
    with tab1:
        # 시계열 그래프
        st.subheader("시간에 따른 코로나19 추이")
        
        # 전체 인도 데이터 집계
        daily_total = filtered_data.groupby('date').agg({
            'confirmed': 'sum',
            'active': 'sum',
            'cured': 'sum',
            'deaths': 'sum'
        }).reset_index()
        
        # 메트릭 선택
        metric_option = st.selectbox(
            "표시할 지표 선택",
            ["모든 지표", "확진자", "활성 환자", "완치자", "사망자"]
        )
        
        if metric_option == "모든 지표":
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_total['date'], y=daily_total['confirmed'],
                                    mode='lines', name='확진자', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=daily_total['date'], y=daily_total['active'],
                                    mode='lines', name='활성 환자', line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=daily_total['date'], y=daily_total['cured'],
                                    mode='lines', name='완치자', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=daily_total['date'], y=daily_total['deaths'],
                                    mode='lines', name='사망자', line=dict(color='gray')))
            
            fig.update_layout(
                title='Covid-19 인도 전체 추이',
                xaxis_title='날짜',
                yaxis_title='인원수',
                hovermode='x unified',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            metric_map = {
                "확진자": "confirmed",
                "활성 환자": "active",
                "완치자": "cured",
                "사망자": "deaths"
            }
            selected_metric = metric_map[metric_option]
            
            fig = px.line(daily_total, x='date', y=selected_metric,
                         title=f'{metric_option} 추이')
            st.plotly_chart(fig, use_container_width=True)
        
        # 일일 신규 확진자
        daily_total['daily_new'] = daily_total['confirmed'].diff().fillna(0)
        
        fig2 = px.bar(daily_total, x='date', y='daily_new',
                     title='일일 신규 확진자 수')
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # 지역별 비교
        st.subheader("지역별 코로나19 현황 비교")
        
        # 최신 데이터로 지역별 비교
        latest_by_region = latest_data.sort_values('confirmed', ascending=False)
        
        # 상위 지역 시각화
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(latest_by_region.head(10), x='confirmed', y='region',
                         title='확진자 수 상위 10개 지역',
                         color='confirmed',
                         color_continuous_scale='Reds')
            fig1.update_layout(yaxis_title='지역', xaxis_title='확진자 수')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 치명률 계산
            latest_by_region['fatality_rate'] = (
                latest_by_region['deaths'] / latest_by_region['confirmed'] * 100
            ).round(2)
            
            top_fatality = latest_by_region[latest_by_region['confirmed'] > 100].nlargest(10, 'fatality_rate')
            
            fig2 = px.bar(top_fatality, x='fatality_rate', y='region',
                         title='치명률 상위 10개 지역 (확진자 100명 이상)',
                         color='fatality_rate',
                         color_continuous_scale='OrRd')
            fig2.update_layout(yaxis_title='지역', xaxis_title='치명률 (%)')
            st.plotly_chart(fig2, use_container_width=True)
        
        # 지역별 시계열 비교
        st.subheader("선택된 지역 시계열 비교")
        
        fig3 = px.line(filtered_data, x='date', y='confirmed', color='region',
                      title='지역별 확진자 추이')
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        # 현황 대시보드
        st.subheader("📊 종합 현황 대시보드")
        
        # 파이 차트
        col1, col2 = st.columns(2)
        
        with col1:
            # 상태별 분포
            status_data = {
                '활성 환자': latest_data['active'].sum(),
                '완치자': latest_data['cured'].sum(),
                '사망자': latest_data['deaths'].sum()
            }
            
            fig1 = px.pie(values=list(status_data.values()), names=list(status_data.keys()),
                         title='현재 상태별 분포',
                         color_discrete_map={'활성 환자': 'orange', '완치자': 'green', '사망자': 'gray'})
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 지역별 확진자 분포
            top_regions_pie = latest_by_region.head(7).copy()
            others_sum = latest_by_region.iloc[7:]['confirmed'].sum()
            
            if others_sum > 0:
                others_row = pd.DataFrame({'region': ['기타'], 'confirmed': [others_sum]})
                top_regions_pie = pd.concat([top_regions_pie[['region', 'confirmed']], others_row])
            
            fig2 = px.pie(top_regions_pie, values='confirmed', names='region',
                         title='지역별 확진자 분포')
            st.plotly_chart(fig2, use_container_width=True)
        
        # 히트맵 - 지역별 지표
        st.subheader("지역별 주요 지표 히트맵")
        
        heatmap_data = latest_by_region[['region', 'confirmed', 'active', 'cured', 'deaths']].set_index('region')
        heatmap_data = heatmap_data.head(15)  # 상위 15개 지역만
        
        # 정규화
        heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
        
        fig3 = px.imshow(heatmap_normalized.T,
                        labels=dict(x="지역", y="지표", color="정규화 값"),
                        y=['확진자', '활성 환자', '완치자', '사망자'],
                        color_continuous_scale='YlOrRd',
                        title='지역별 주요 지표 히트맵 (정규화)')
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        # 증가율 분석
        st.subheader("📈 증가율 분석")
        
        # 전체 증가율 계산
        daily_total['growth_rate'] = daily_total['confirmed'].pct_change() * 100
        daily_total['ma7_growth'] = daily_total['growth_rate'].rolling(window=7).mean()
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=daily_total['date'], y=daily_total['growth_rate'],
                                 mode='lines', name='일일 증가율', line=dict(color='lightblue')))
        fig1.add_trace(go.Scatter(x=daily_total['date'], y=daily_total['ma7_growth'],
                                 mode='lines', name='7일 이동평균', line=dict(color='blue', width=2)))
        fig1.add_hline(y=0, line_dash="dash", line_color="red")
        
        fig1.update_layout(
            title='확진자 증가율 추이',
            xaxis_title='날짜',
            yaxis_title='증가율 (%)',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # 주간 통계
        st.subheader("주간 통계")
        
        # 주간 데이터 집계
        weekly_data = daily_total.set_index('date').resample('W').agg({
            'confirmed': 'last',
            'daily_new': 'sum',
            'active': 'last',
            'cured': 'last',
            'deaths': 'last'
        }).reset_index()
        
        weekly_data['weekly_new'] = weekly_data['confirmed'].diff().fillna(0)
        
        fig2 = px.bar(weekly_data, x='date', y='weekly_new',
                     title='주간 신규 확진자 수')
        st.plotly_chart(fig2, use_container_width=True)

def render_product_inspection(product_inspection):
    """제품 검사 데이터 분석 페이지"""
    st.header("🏭 제품 검사 품질 관리 분석")
    
    # 필터링 옵션
    st.sidebar.subheader("⚙️ 검사 설정")
    
    # 날짜 범위 필터
    start_date = st.sidebar.date_input("시작일", product_inspection['date'].min().date())
    end_date = st.sidebar.date_input("종료일", product_inspection['date'].max().date())
    
    # 검사 단계 필터
    all_steps = product_inspection['inspection_step'].unique()
    selected_steps = st.sidebar.multiselect(
        "검사 단계 선택",
        all_steps,
        default=all_steps
    )
    
    # 데이터 필터링
    filtered_data = product_inspection[
        (product_inspection['date'].dt.date >= start_date) & 
        (product_inspection['date'].dt.date <= end_date) &
        (product_inspection['inspection_step'].isin(selected_steps))
    ]
    
    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_inspections = len(filtered_data)
        st.metric("총 검사 수", f"{total_inspections:,}건")
    
    with col2:
        avg_value = filtered_data['value'].mean()
        st.metric("평균 측정값", f"{avg_value:.2f}")
    
    with col3:
        # 스펙 내 비율 계산
        within_spec = filtered_data[
            (filtered_data['value'] >= filtered_data['lower_spec']) & 
            (filtered_data['value'] <= filtered_data['upper_spec'])
        ]
        spec_rate = len(within_spec) / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
        st.metric("스펙 내 비율", f"{spec_rate:.1f}%")
    
    with col4:
        # Cp 계산 (공정능력지수)
        std_dev = filtered_data['value'].std()
        if std_dev > 0:
            usl = filtered_data['upper_spec'].iloc[0]
            lsl = filtered_data['lower_spec'].iloc[0]
            cp = (usl - lsl) / (6 * std_dev)
            st.metric("Cp (공정능력)", f"{cp:.2f}")
        else:
            st.metric("Cp (공정능력)", "N/A")
    
    st.divider()
    
    # 시각화 탭
    tab1, tab2, tab3, tab4 = st.tabs(["📊 관리도", "📈 통계 분석", "🎯 공정능력", "📉 트렌드 분석"])
    
    with tab1:
        # 관리도 (Control Chart)
        st.subheader("📊 SPC 관리도")
        
        # 검사 단계 선택
        step_for_chart = st.selectbox("관리도를 볼 검사 단계 선택", selected_steps)
        step_data = filtered_data[filtered_data['inspection_step'] == step_for_chart].copy()
        
        if len(step_data) > 0:
            # 통계 계산
            mean_val = step_data['value'].mean()
            std_val = step_data['value'].std()
            ucl = mean_val + 3 * std_val  # Upper Control Limit
            lcl = mean_val - 3 * std_val  # Lower Control Limit
            
            # 관리도 그리기
            fig = go.Figure()
            
            # 측정값
            fig.add_trace(go.Scatter(
                x=step_data['date'], y=step_data['value'],
                mode='lines+markers',
                name='측정값',
                line=dict(color='blue'),
                marker=dict(size=6)
            ))
            
            # 중심선
            fig.add_hline(y=mean_val, line_dash="solid", line_color="green", 
                         annotation_text=f"평균: {mean_val:.2f}")
            
            # 관리한계선
            fig.add_hline(y=ucl, line_dash="dash", line_color="red", 
                         annotation_text=f"UCL: {ucl:.2f}")
            fig.add_hline(y=lcl, line_dash="dash", line_color="red", 
                         annotation_text=f"LCL: {lcl:.2f}")
            
            # 스펙 한계선
            fig.add_hline(y=step_data['upper_spec'].iloc[0], line_dash="dot", 
                         line_color="orange", annotation_text="Upper Spec")
            fig.add_hline(y=step_data['lower_spec'].iloc[0], line_dash="dot", 
                         line_color="orange", annotation_text="Lower Spec")
            fig.add_hline(y=step_data['target'].iloc[0], line_dash="dashdot", 
                         line_color="darkgreen", annotation_text="Target")
            
            fig.update_layout(
                title=f'{step_for_chart} 단계 SPC 관리도',
                xaxis_title='날짜',
                yaxis_title='측정값',
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 이상점 검출
            out_of_control = step_data[(step_data['value'] > ucl) | (step_data['value'] < lcl)]
            out_of_spec = step_data[
                (step_data['value'] > step_data['upper_spec']) | 
                (step_data['value'] < step_data['lower_spec'])
            ]
            
            col1, col2 = st.columns(2)
            with col1:
                st.error(f"⚠️ 관리한계 이탈: {len(out_of_control)}건")
                if len(out_of_control) > 0:
                    st.dataframe(out_of_control[['date', 'value']], use_container_width=True)
            
            with col2:
                st.warning(f"⚠️ 스펙 이탈: {len(out_of_spec)}건")
                if len(out_of_spec) > 0:
                    st.dataframe(out_of_spec[['date', 'value']], use_container_width=True)
    
    with tab2:
        # 통계 분석
        st.subheader("📈 통계 분석")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 히스토그램
            fig1 = px.histogram(filtered_data, x='value', nbins=30,
                               title='측정값 분포',
                               color='inspection_step')
            
            # 스펙 라인 추가
            fig1.add_vline(x=filtered_data['upper_spec'].iloc[0], line_dash="dash", 
                          line_color="red", annotation_text="USL")
            fig1.add_vline(x=filtered_data['lower_spec'].iloc[0], line_dash="dash", 
                          line_color="red", annotation_text="LSL")
            fig1.add_vline(x=filtered_data['target'].iloc[0], line_dash="dash", 
                          line_color="green", annotation_text="Target")
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 박스 플롯
            fig2 = px.box(filtered_data, x='inspection_step', y='value',
                         title='검사 단계별 측정값 분포')
            
            # 스펙 라인 추가
            fig2.add_hline(y=filtered_data['upper_spec'].iloc[0], line_dash="dash", 
                          line_color="red", annotation_text="USL")
            fig2.add_hline(y=filtered_data['lower_spec'].iloc[0], line_dash="dash", 
                          line_color="red", annotation_text="LSL")
            fig2.add_hline(y=filtered_data['target'].iloc[0], line_dash="dash", 
                          line_color="green", annotation_text="Target")
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # 기술통계
        st.subheader("기술통계")
        
        stats_df = filtered_data.groupby('inspection_step')['value'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(3)
        
        # 스펙 내 비율 추가
        for step in stats_df.index:
            step_data = filtered_data[filtered_data['inspection_step'] == step]
            within = step_data[
                (step_data['value'] >= step_data['lower_spec']) & 
                (step_data['value'] <= step_data['upper_spec'])
            ]
            stats_df.loc[step, '스펙내비율(%)'] = len(within) / len(step_data) * 100 if len(step_data) > 0 else 0
        
        st.dataframe(stats_df, use_container_width=True)
    
    with tab3:
        # 공정능력 분석
        st.subheader("🎯 공정능력 분석")
        
        # 검사 단계별 공정능력 계산
        capability_data = []
        
        for step in selected_steps:
            step_data = filtered_data[filtered_data['inspection_step'] == step]
            
            if len(step_data) > 0:
                mean_val = step_data['value'].mean()
                std_val = step_data['value'].std()
                
                if std_val > 0:
                    usl = step_data['upper_spec'].iloc[0]
                    lsl = step_data['lower_spec'].iloc[0]
                    target = step_data['target'].iloc[0]
                    
                    # Cp: 공정능력지수
                    cp = (usl - lsl) / (6 * std_val)
                    
                    # Cpk: 편향된 공정능력지수
                    cpu = (usl - mean_val) / (3 * std_val)
                    cpl = (mean_val - lsl) / (3 * std_val)
                    cpk = min(cpu, cpl)
                    
                    # Cpm: 목표치 대비 공정능력
                    cpm = cp / np.sqrt(1 + ((mean_val - target) / std_val) ** 2)
                    
                    capability_data.append({
                        '검사단계': step,
                        'Cp': round(cp, 3),
                        'Cpk': round(cpk, 3),
                        'Cpm': round(cpm, 3),
                        '평균': round(mean_val, 3),
                        '표준편차': round(std_val, 3)
                    })
        
        if capability_data:
            capability_df = pd.DataFrame(capability_data)
            
            # 공정능력 지표 표시
            st.dataframe(capability_df, use_container_width=True)
            
            # 공정능력 시각화
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(capability_df, x='검사단계', y=['Cp', 'Cpk'],
                             title='공정능력지수 비교',
                             barmode='group')
                fig1.add_hline(y=1.33, line_dash="dash", line_color="green", 
                              annotation_text="목표 수준 (1.33)")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # 공정능력 등급 판정
                def get_capability_grade(cpk):
                    if cpk >= 1.67:
                        return "매우 우수", "green"
                    elif cpk >= 1.33:
                        return "우수", "lightgreen"
                    elif cpk >= 1.00:
                        return "보통", "yellow"
                    elif cpk >= 0.67:
                        return "개선 필요", "orange"
                    else:
                        return "즉시 개선", "red"
                
                grades = []
                colors = []
                for cpk in capability_df['Cpk']:
                    grade, color = get_capability_grade(cpk)
                    grades.append(grade)
                    colors.append(color)
                
                capability_df['등급'] = grades
                
                fig2 = px.scatter(capability_df, x='Cp', y='Cpk', 
                                 text='검사단계', size='표준편차',
                                 color='등급',
                                 title='공정능력 매트릭스',
                                 color_discrete_map={
                                     "매우 우수": "green",
                                     "우수": "lightgreen",
                                     "보통": "yellow",
                                     "개선 필요": "orange",
                                     "즉시 개선": "red"
                                 })
                fig2.update_traces(textposition='top center')
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        # 트렌드 분석
        st.subheader("📉 트렌드 및 패턴 분석")
        
        # 이동평균 계산
        for step in selected_steps:
            step_data = filtered_data[filtered_data['inspection_step'] == step].copy()
            step_data = step_data.sort_values('date')
            step_data['ma7'] = step_data['value'].rolling(window=7, min_periods=1).mean()
            step_data['ma30'] = step_data['value'].rolling(window=30, min_periods=1).mean()
            
            fig = go.Figure()
            
            # 실제값
            fig.add_trace(go.Scatter(x=step_data['date'], y=step_data['value'],
                                    mode='markers', name='실제값',
                                    marker=dict(size=4, color='lightblue')))
            
            # 이동평균
            fig.add_trace(go.Scatter(x=step_data['date'], y=step_data['ma7'],
                                    mode='lines', name='7일 이동평균',
                                    line=dict(color='blue', width=2)))
            
            fig.add_trace(go.Scatter(x=step_data['date'], y=step_data['ma30'],
                                    mode='lines', name='30일 이동평균',
                                    line=dict(color='darkblue', width=2)))
            
            # 스펙 라인
            fig.add_hline(y=step_data['upper_spec'].iloc[0], line_dash="dash", 
                         line_color="red", annotation_text="USL")
            fig.add_hline(y=step_data['lower_spec'].iloc[0], line_dash="dash", 
                         line_color="red", annotation_text="LSL")
            fig.add_hline(y=step_data['target'].iloc[0], line_dash="dash", 
                         line_color="green", annotation_text="Target")
            
            fig.update_layout(
                title=f'{step} 단계 트렌드 분석',
                xaxis_title='날짜',
                yaxis_title='측정값',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # 상관관계 분석 (여러 검사 단계가 있을 경우)
        if len(selected_steps) > 1:
            st.subheader("검사 단계 간 상관관계")
            
            # 피벗 테이블 생성
            pivot_data = filtered_data.pivot_table(
                index='date', 
                columns='inspection_step', 
                values='value'
            )
            
            # 상관계수 계산
            correlation = pivot_data.corr()
            
            # 히트맵
            fig = px.imshow(correlation,
                           labels=dict(x="검사 단계", y="검사 단계", color="상관계수"),
                           color_continuous_scale='RdBu_r',
                           title='검사 단계 간 상관관계 히트맵')
            st.plotly_chart(fig, use_container_width=True)

def render_co2_analysis(co2_data):
    """CO2 배출량 분석 페이지 - 기존 함수 찾아서 추가"""
    st.header("🌱 CO2 배출량 데이터 분석")
    
    # 필터링 옵션
    st.sidebar.subheader("🚗 차량 필터")
    
    # 제조사 필터
    makes = st.sidebar.multiselect(
        "제조사 선택",
        co2_data['Make'].unique(),
        default=co2_data['Make'].value_counts().head(5).index.tolist()
    )
    
    # 연료 타입 필터
    fuel_types = st.sidebar.multiselect(
        "연료 타입",
        co2_data['Fuel Type'].unique() if 'Fuel Type' in co2_data.columns else [],
        default=co2_data['Fuel Type'].unique() if 'Fuel Type' in co2_data.columns else []
    )
    
    # 데이터 필터링
    filtered_data = co2_data[co2_data['Make'].isin(makes)]
    if 'Fuel Type' in co2_data.columns and fuel_types:
        filtered_data = filtered_data[filtered_data['Fuel Type'].isin(fuel_types)]
    
    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_co2 = filtered_data['CO2 Emissions(g/km)'].mean()
        st.metric("평균 CO2 배출량", f"{avg_co2:.1f} g/km")
    
    with col2:
        min_co2 = filtered_data['CO2 Emissions(g/km)'].min()
        st.metric("최소 CO2 배출량", f"{min_co2:.1f} g/km")
    
    with col3:
        max_co2 = filtered_data['CO2 Emissions(g/km)'].max()
        st.metric("최대 CO2 배출량", f"{max_co2:.1f} g/km")
    
    with col4:
        total_vehicles = len(filtered_data)
        st.metric("차량 수", f"{total_vehicles:,}대")
    
    # 시각화
    tab1, tab2, tab3 = st.tabs(["📊 제조사별 분석", "🔥 연료 타입별 분석", "📈 상세 분석"])
    
    with tab1:
        # 제조사별 평균 CO2 배출량
        make_avg = filtered_data.groupby('Make')['CO2 Emissions(g/km)'].mean().sort_values()
        
        fig1 = px.bar(x=make_avg.values, y=make_avg.index,
                     title='제조사별 평균 CO2 배출량',
                     labels={'x': 'CO2 배출량 (g/km)', 'y': '제조사'},
                     color=make_avg.values,
                     color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig1, use_container_width=True)
        
        # 제조사별 차량 수
        make_count = filtered_data['Make'].value_counts()
        
        fig2 = px.pie(values=make_count.values, names=make_count.index,
                     title='제조사별 차량 분포')
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        if 'Fuel Type' in co2_data.columns:
            # 연료 타입별 CO2 배출량
            fuel_avg = filtered_data.groupby('Fuel Type')['CO2 Emissions(g/km)'].mean().sort_values()
            
            fig3 = px.bar(fuel_avg, title='연료 타입별 평균 CO2 배출량',
                         labels={'value': 'CO2 배출량 (g/km)', 'index': '연료 타입'})
            st.plotly_chart(fig3, use_container_width=True)
            
            # 연료 타입별 분포
            fig4 = px.box(filtered_data, x='Fuel Type', y='CO2 Emissions(g/km)',
                         title='연료 타입별 CO2 배출량 분포')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("연료 타입 정보가 없습니다.")
    
    with tab3:
        # 상세 분석
        st.subheader("CO2 배출량 분포")
        
        fig5 = px.histogram(filtered_data, x='CO2 Emissions(g/km)', nbins=30,
                           title='CO2 배출량 히스토그램')
        st.plotly_chart(fig5, use_container_width=True)
        
        # 상위/하위 차량
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌿 친환경 차량 TOP 10")
            top_eco = filtered_data.nsmallest(10, 'CO2 Emissions(g/km)')[['Make', 'Model', 'CO2 Emissions(g/km)']] if 'Model' in filtered_data.columns else filtered_data.nsmallest(10, 'CO2 Emissions(g/km)')[['Make', 'CO2 Emissions(g/km)']]
            st.dataframe(top_eco, use_container_width=True)
        
        with col2:
            st.subheader("🚨 고배출 차량 TOP 10")
            top_polluters = filtered_data.nlargest(10, 'CO2 Emissions(g/km)')[['Make', 'Model', 'CO2 Emissions(g/km)']] if 'Model' in filtered_data.columns else filtered_data.nlargest(10, 'CO2 Emissions(g/km)')[['Make', 'CO2 Emissions(g/km)']]
            st.dataframe(top_polluters, use_container_width=True)

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