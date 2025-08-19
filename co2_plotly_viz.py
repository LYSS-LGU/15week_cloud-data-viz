# C:\githome\15week_cloud-data-viz\co2_plotly_viz.py
# CO2 배출량 데이터 Plotly 시각화 예제
# 환경 친화적 차량 분석 대시보드

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 데이터 로드
co2_data = pd.read_csv("dataset/CO2_Emissions.csv")

print("🌱 CO2 배출량 데이터 기본 정보")
print(f"총 차량 수: {len(co2_data):,}대")
print(f"제조사 수: {co2_data['Make'].nunique()}개")
print(f"평균 CO2 배출량: {co2_data['CO2 Emissions(g/km)'].mean():.1f} g/km")

# 1. 🌟 인터랙티브 버블 차트 - 엔진 크기 vs CO2 배출량 vs 연비
print("\n🎨 생성 중: 인터랙티브 버블 차트...")

# 상위 제조사만 선택 (가독성을 위해)
top_makes = co2_data['Make'].value_counts().head(15).index
filtered_data = co2_data[co2_data['Make'].isin(top_makes)].copy()

# 버블 차트 생성
fig_bubble = px.scatter(
    filtered_data,
    x='Engine Size(L)',
    y='CO2 Emissions(g/km)',
    size='Fuel Consumption Comb (mpg)',  # 버블 크기: 연비 (역설적으로 큰 것이 좋음)
    color='Make',  # 색상: 제조사별
    hover_data={
        'Model': True,
        'Vehicle Class': True,
        'Cylinders': True,
        'Fuel Consumption Comb (mpg)': ':.1f'
    },
    title='🌍 차량별 환경 성능 분석: 엔진 크기 vs CO2 배출량 vs 연비',
    labels={
        'Engine Size(L)': '🔧 엔진 크기 (L)',
        'CO2 Emissions(g/km)': '🌱 CO2 배출량 (g/km)',
        'Make': '🏭 제조사'
    },
    size_max=20,
    color_discrete_sequence=px.colors.qualitative.Set3
)

# 친환경 기준선 추가
fig_bubble.add_hline(
    y=200, 
    line_dash="dash", 
    line_color="red",
    annotation_text="🚨 친환경 기준선 (200g/km)",
    annotation_position="top right"
)

# 효율적인 엔진 크기 기준선
fig_bubble.add_vline(
    x=2.0,
    line_dash="dot",
    line_color="green",
    annotation_text="💚 효율적 엔진 크기 (2.0L)",
    annotation_position="top left"
)

# 레이아웃 개선
fig_bubble.update_layout(
    title={
        'text': '🌍 차량별 환경 성능 분석<br><sub>버블 크기: 연비 (mpg) | 색상: 제조사 | 위치: 엔진크기 vs CO2배출량</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='🔧 엔진 크기 (L)',
    yaxis_title='🌱 CO2 배출량 (g/km)',
    font=dict(size=12),
    plot_bgcolor='rgba(240,248,255,0.8)',  # 연한 하늘색 배경
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.01
    ),
    width=1200,
    height=700
)

# 축 스타일링
fig_bubble.update_xaxes(
    gridcolor='lightgray',
    gridwidth=1,
    showgrid=True
)
fig_bubble.update_yaxes(
    gridcolor='lightgray',
    gridwidth=1,
    showgrid=True
)

# 차트 표시
fig_bubble.show()

# 2. 🎯 제조사별 환경 성능 랭킹 차트
print("\n🏆 생성 중: 제조사별 환경 성능 랭킹...")

# 제조사별 통계 계산 (최소 5대 이상인 제조사만)
make_stats = co2_data.groupby('Make').agg({
    'CO2 Emissions(g/km)': ['mean', 'count'],
    'Fuel Consumption Comb (mpg)': 'mean',
    'Engine Size(L)': 'mean'
}).round(2)

make_stats.columns = ['평균_CO2', '차량수', '평균_연비', '평균_엔진크기']
make_stats = make_stats[make_stats['차량수'] >= 5].sort_values('평균_CO2')

# 환경 점수 계산 (CO2는 낮을수록, 연비는 높을수록 좋음)
make_stats['환경점수'] = (
    (300 - make_stats['평균_CO2']) * 0.6 +  # CO2 비중 60%
    (make_stats['평균_연비'] * 3) * 0.4     # 연비 비중 40%
).round(1)

# 상위 20개 제조사 선택
top_20_makes = make_stats.head(20)

# 컬러 스케일 생성 (친환경 순)
colors = px.colors.sample_colorscale(
    'RdYlGn', 
    [i/len(top_20_makes) for i in range(len(top_20_makes))]
)

# 가로 막대 차트 생성
fig_ranking = go.Figure()

fig_ranking.add_trace(go.Bar(
    y=top_20_makes.index,
    x=top_20_makes['평균_CO2'],
    orientation='h',
    marker=dict(
        color=colors,
        line=dict(color='black', width=1)
    ),
    text=[f"{co2:.0f}g/km<br>{mpg:.1f}mpg" 
          for co2, mpg in zip(top_20_makes['평균_CO2'], top_20_makes['평균_연비'])],
    textposition='outside',
    hovertemplate=
    '<b>%{y}</b><br>' +
    '🌱 평균 CO2: %{x:.1f} g/km<br>' +
    '⛽ 평균 연비: %{customdata[0]:.1f} mpg<br>' +
    '🚗 차량 수: %{customdata[1]:.0f}대<br>' +
    '🏆 환경점수: %{customdata[2]:.1f}점<br>' +
    '<extra></extra>',
    customdata=np.column_stack((
        top_20_makes['평균_연비'], 
        top_20_makes['차량수'],
        top_20_makes['환경점수']
    ))
))

# 레이아웃 설정
fig_ranking.update_layout(
    title={
        'text': '🏆 제조사별 환경 친화 랭킹 TOP 20<br><sub>낮은 CO2 배출량 순위 (평균 기준)</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='🌱 평균 CO2 배출량 (g/km)',
    yaxis_title='🏭 자동차 제조사',
    plot_bgcolor='rgba(240,255,240,0.8)',  # 연한 녹색 배경
    paper_bgcolor='white',
    font=dict(size=11),
    width=1000,
    height=800,
    margin=dict(l=150)  # 왼쪽 여백 증가 (제조사명을 위해)
)

# 친환경 기준선 추가
fig_ranking.add_vline(
    x=200,
    line_dash="dash",
    line_color="red",
    annotation_text="친환경 기준 (200g/km)",
    annotation_position="top"
)

fig_ranking.add_vline(
    x=150,
    line_dash="dot",
    line_color="green",
    annotation_text="우수 기준 (150g/km)",
    annotation_position="top"
)

# 축 스타일링
fig_ranking.update_xaxes(
    gridcolor='lightgray',
    gridwidth=1,
    showgrid=True,
    range=[120, max(top_20_makes['평균_CO2']) + 20]
)

# 차트 표시
fig_ranking.show()

# 3. 📊 차량 클래스별 CO2 분포 박스플롯
print("\n📦 생성 중: 차량 클래스별 CO2 분포...")

fig_box = px.box(
    co2_data,
    x='Vehicle Class',
    y='CO2 Emissions(g/km)',
    color='Vehicle Class',
    title='📊 차량 클래스별 CO2 배출량 분포 분석',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 친환경 기준선 추가
fig_box.add_hline(
    y=200,
    line_dash="dash",
    line_color="red",
    annotation_text="친환경 기준선"
)

fig_box.update_layout(
    title={
        'text': '📊 차량 클래스별 CO2 배출량 분포<br><sub>박스플롯으로 보는 클래스별 환경 성능</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 16}
    },
    xaxis_title='🚗 차량 클래스',
    yaxis_title='🌱 CO2 배출량 (g/km)',
    showlegend=False,
    plot_bgcolor='rgba(255,248,240,0.8)',
    paper_bgcolor='white',
    width=1100,
    height=600
)

fig_box.update_xaxes(tickangle=45)
fig_box.show()

print("\n✨ 시각화 완성!")
print("\n🌟 주요 인사이트:")
print(f"• 가장 친환경적인 제조사: {top_20_makes.index[0]} (평균 {top_20_makes.iloc[0]['평균_CO2']:.1f} g/km)")
print(f"• 친환경 기준(200g/km) 이하 제조사: {len(top_20_makes[top_20_makes['평균_CO2'] < 200])}개")
print(f"• 엔진 크기와 CO2 배출량은 강한 양의 상관관계")
print(f"• 하이브리드 차량들이 확연히 낮은 CO2 배출량을 보임")