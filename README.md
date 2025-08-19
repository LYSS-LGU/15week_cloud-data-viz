# 15주차 클라우드 기반 데이터 시각화

## 📚 Plotly 고급 시각화 학습 정리 (CO2 분석 프로젝트)

### 🎯 학습 목표
- **Plotly Express vs Graph Objects** 차이점 이해 및 활용
- **인터랙티브 차트** 구현 기법 습득
- **다중 서브플롯** 구성 및 레이아웃 설계
- **고급 스타일링** 및 사용자 경험 최적화

---

### 📊 1. Plotly Express 기본 활용

#### 버블 차트 (Scatter Plot)
```python
# 3차원 데이터를 2D로 효과적 표현
fig_bubble = px.scatter(
    data, 
    x='Engine Size(L)', 
    y='CO2 Emissions(g/km)',
    size='Fuel Consumption Comb (mpg)',  # 버블 크기
    color='Make',                        # 색상 구분
    hover_data=['Model', 'Vehicle Class'], # 호버 정보
    size_max=20                          # 최대 버블 크기
)
```
**학습 포인트**: 3개 이상의 변수를 동시에 시각화하는 효과적인 방법

#### 박스플롯 분포 분석
```python
fig_box = px.box(
    data, 
    x='Vehicle Class', 
    y='CO2 Emissions(g/km)',
    color='Vehicle Class'  # 카테고리별 색상
)
```
**학습 포인트**: 범주형 데이터의 분포와 이상치를 한 번에 파악

#### 상관관계 시각화 (추세선 포함)
```python
fig_corr = px.scatter(
    data,
    x='Fuel Consumption Comb (mpg)',
    y='CO2 Emissions(g/km)',
    trendline='ols',  # 회귀선 자동 추가
    color='Vehicle Class'
)
```
**학습 포인트**: `trendline='ols'`로 통계적 관계를 시각적으로 표현

---

### 🔧 2. Graph Objects 고급 제어

#### 기준선 추가 기법
```python
# 수평선 (임계값 표시)
fig.add_hline(
    y=200, 
    line_dash="dash", 
    line_color="red",
    annotation_text="🚨 친환경 기준선 (200g/km)"
)

# 수직선 (기준값 표시)  
fig.add_vline(
    x=2.0,
    line_dash="dot",
    line_color="green", 
    annotation_text="💚 효율적 엔진 크기"
)
```
**학습 포인트**: 데이터에 의미 있는 기준선을 추가하여 해석력 향상

#### 영역 강조 표시
```python
# 사각형 영역 강조
fig.add_vrect(x0=35, x1=50, fillcolor="green", opacity=0.1)
fig.add_hrect(y0=120, y1=180, fillcolor="lightgreen", opacity=0.1)
```
**학습 포인트**: 특정 구간을 시각적으로 강조하여 중요 정보 전달

---

### 📐 3. 서브플롯 구성 및 다중 차트

#### 2x2 서브플롯 레이아웃
```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('차트1', '차트2', '차트3', '차트4'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"type": "pie"}]]  # 파이차트 지정
)

# 각 위치에 차트 추가
fig.add_trace(go.Bar(...), row=1, col=1)
fig.add_trace(go.Bar(...), row=1, col=2)  
fig.add_trace(go.Pie(...), row=2, col=2)
```
**학습 포인트**: 여러 관점의 분석을 하나의 대시보드로 통합

---

### 🎨 4. 고급 스타일링 및 레이아웃

#### 제목 및 축 레이블 고급 설정
```python
fig.update_layout(
    title={
        'text': '🌍 제목<br><sub>부제목</sub>',
        'x': 0.5,           # 중앙 정렬
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='🔧 X축 제목',
    yaxis_title='🌱 Y축 제목'
)
```

#### 배경 및 색상 테마
```python
fig.update_layout(
    plot_bgcolor='rgba(240,248,255,0.8)',  # 연한 하늘색
    paper_bgcolor='white',
    font=dict(size=12)
)
```

#### 범례 위치 조정
```python
fig.update_layout(
    legend=dict(
        orientation="v",     # 세로 배치
        yanchor="top", y=1,
        xanchor="left", x=1.01  # 차트 오른쪽 외부
    )
)
```

#### 축 그리드 스타일링
```python
fig.update_xaxes(
    gridcolor='lightgray',
    gridwidth=1,
    showgrid=True,
    tickangle=45  # 레이블 회전
)
```

---

### 💡 5. 호버 정보 커스터마이징

```python
# 상세한 호버 템플릿 구성
hovertemplate=
'<b>%{y}</b><br>' +
'🌱 평균 CO2: %{x:.1f} g/km<br>' +
'⛽ 평균 연비: %{customdata[0]:.1f} mpg<br>' +
'🚗 차량 수: %{customdata[1]:.0f}대<br>' +
'<extra></extra>',  # 박스 테두리 제거
customdata=np.column_stack((연비데이터, 차량수데이터))
```
**학습 포인트**: 사용자가 차트와 상호작용할 때 풍부한 정보 제공

---

### 🔍 6. 데이터 전처리 및 분석 기법

#### 상위 데이터 필터링
```python
# 가독성을 위한 상위 N개 선택
top_makes = data['Make'].value_counts().head(15).index
filtered_data = data[data['Make'].isin(top_makes)]
```

#### 통계값 계산 및 그룹화
```python
# 제조사별 통계 (최소 N대 이상)
stats = data.groupby('Make').agg({
    'CO2 Emissions(g/km)': ['mean', 'count'],
    'Fuel Consumption Comb (mpg)': 'mean'
}).round(2)
stats = stats[stats[('CO2 Emissions(g/km)', 'count')] >= 5]
```

#### 환경 점수 계산
```python
# 복합 지표 생성
stats['환경점수'] = (
    (300 - stats['평균_CO2']) * 0.6 +    # CO2 비중 60%
    (stats['평균_연비'] * 3) * 0.4       # 연비 비중 40%  
).round(1)
```

---

### ⚡ 7. 성능 최적화 팁

1. **대용량 데이터**: 상위 N개 필터링으로 렌더링 속도 개선
2. **색상 최적화**: `px.colors.qualitative.Set3` 등 미리 정의된 팔레트 사용
3. **메모리 관리**: 불필요한 컬럼 제거 및 데이터 타입 최적화
4. **차트 크기**: `width`, `height` 명시적 설정으로 레이아웃 안정화

---

### 🎓 핵심 학습 성과

1. **Plotly Express**: 빠른 프로토타이핑과 기본 인터랙티브 차트
2. **Graph Objects**: 세밀한 제어와 고급 커스터마이징
3. **서브플롯**: 다각도 분석을 위한 통합 대시보드 구성
4. **스타일링**: 전문적이고 사용자 친화적인 시각화 디자인
5. **데이터 스토리텔링**: 기준선, 영역 강조 등으로 인사이트 강화

**다음 학습 목표**: Streamlit과 연동하여 웹 애플리케이션으로 배포하기

---

## 🚀 Streamlit 핵심 정리

### 필수 구성 요소
- **텍스트**: `st.title()`, `st.header()`, `st.markdown()`
- **데이터 표시**: `st.dataframe()`, `st.metric()`, `st.code()`  
- **사용자 입력**: `st.button()`, `st.selectbox()`, `st.slider()`
- **상태 관리**: `st.session_state` - 페이지 간 데이터 유지
- **캐싱**: `@st.cache_data` - 성능 최적화

### 실습 데이터셋
- **ABNB 주식**: 캔들스틱 차트, 거래량 분석
- **EV 충전**: 시간대별 패턴 분석  
- **의료비**: 상관관계 시각화

---

## 프로젝트 개요

이 프로젝트는 클라우드 환경에서 다양한 데이터 시각화 도구를 학습하고 활용하는 것을 목표로 합니다. Python의 주요 시각화 라이브러리인 Matplotlib, Seaborn, Plotly와 지도 시각화 도구인 Folium, 그리고 웹 애플리케이션 개발을 위한 Streamlit 사용법을 다룹니다.

## 학습 목표

- 데이터 시각화의 중요성과 다양한 도구의 특성 이해
- 탐색적 데이터 분석(EDA)을 위한 시각화 기법 습득
- 정적 시각화부터 인터랙티브 시각화까지 단계별 학습
- 지도 기반 데이터 시각화 구현
- 웹 애플리케이션을 통한 데이터 시각화 배포

---

## 각 라이브러리 상세 정리

### 1. 데이터 시각화 기초 (Data Visualization I)

#### 데이터 시각화의 정의와 중요성
- **정의**: 복잡한 데이터를 시각적 요소를 활용하여 직관적으로 표현하는 과정
- **목적**: 데이터에 담긴 의미와 패턴을 효과적으로 전달

#### 데이터 시각화의 3가지 핵심 역할
1. **탐색적 데이터 분석(EDA)의 출발점**
   - 전체 데이터를 시각적으로 파악하여 분석 방향 설정
   - 변수 간 분포, 상관관계, 이상값 확인

2. **분석 결과의 의사결정 반영**
   - 분석 내용을 명확하게 표현하고 전달하는 도구
   - 단순한 숫자 이상으로 의미와 인사이트 제공

3. **시각화 전 데이터 전처리의 중요성**
   - 구조 파악: 데이터프레임 형태, 변수 개수 등
   - 변수 유형: 수치형/범주형 여부
   - 결측값, 이상치, 오류값 확인 및 처리

#### 앤스컴 콰르텟 (Anscombe's Quartet)
- 동일한 통계량(평균, 분산, 상관관계, 회귀선)을 가진 4개의 다른 데이터셋
- 시각화의 필요성을 보여주는 대표적인 사례

### 2. Matplotlib

#### 개요
- Python의 2D 플로팅 라이브러리로, 데이터 시각화를 위한 핵심 도구
- 시계열 데이터 시각화에 최적화
- MATLAB과 유사한 인터페이스 제공

#### 주요 특징
- **높은 유연성과 커스터마이징**: 세밀한 그래프 조정 가능
- **다양한 플롯 유형**: 선, 막대, 산점도, 히스토그램, 등고선 등
- **Figure와 Axes 구조**: 체계적인 그래프 구성

#### 핵심 구성 요소
1. **Figure**: 그래프의 전체 틀
2. **Axes**: 실제 그래프가 그려지는 공간
3. **Axis**: X축, Y축 설정 및 관리

#### 차트 유형별 분류
- **기본 플롯**: 선 그래프, 산점도, 막대 그래프, stem, step, fill_between
- **통계 플롯**: 히스토그램, 파이 차트
- **배열 플롯**: 이미지, 등고선 플롯
- **필드 플롯**: 벡터 필드, 스트림 플롯

### 3. Seaborn

#### 개요
- Matplotlib 기반의 통계적 데이터 시각화 라이브러리
- 복잡한 데이터셋의 시각화를 쉽게 만들어주는 고급 API 제공
- Pandas 데이터프레임과의 뛰어난 통합성

#### 주요 특징
- **사용자 친화적**: 기본 설정과 컬러 테마가 미리 구성
- **통계적 연산 제공**: 자동 통계 계산 및 시각화
- **다변량 데이터 시각화**: 여러 변수 간의 관계를 동시에 표현
- **hue 매개변수**: 범주형 데이터에 따른 색상 구분

#### 주요 플롯 함수
- **기본 플롯**: `lineplot()`, `scatterplot()`, `barplot()`
- **분포 플롯**: `histplot()`, `boxplot()`, `violinplot()`
- **관계 플롯**: `regplot()`, `pairplot()`, `heatmap()`
- **다중 플롯**: `FacetGrid()`, `catplot()`

#### 내장 데이터셋
tips, iris, titanic, flights 등 다양한 예제 데이터셋 제공

### 4. Plotly

#### 개요
- 파이썬의 인터랙티브 데이터 시각화 라이브러리
- 웹 기반으로 작동하며 대화형 그래프 생성에 특화
- 비즈니스 인텔리전스(BI) 도구로도 활용

#### 주요 특징
- **인터랙티브 시각화**: 사용자가 그래프와 상호작용 가능
- **고급 그래프 유형**: 3D 그래프, 지도 시각화, 애니메이션
- **웹 브라우저 지원**: 직접 브라우저에서 시각화 가능
- **Dash 연동**: 복잡한 대시보드 구축 가능

#### 서브모듈
- **plotly.express**: 고수준 인터페이스로 간단한 시각화
- **plotly.graph_objects**: 저수준 인터페이스로 세밀한 조정

#### 특화 시각화 기법
- **Treemap**: 계층적 데이터의 부분-전체 관계 표현
- **Sunburst**: 원형 계층 구조 시각화
- **Choropleth**: 지리 영역별 데이터를 지도 위에 색상으로 표현

### 5. Folium

#### 개요
- Python 기반의 지도 시각화 라이브러리
- 내부적으로 Leaflet.js(JavaScript 라이브러리) 사용
- 인터랙티브한 지도를 웹 브라우저에서 렌더링

#### 주요 특징
- **간단한 사용법**: 위도, 경도 좌표만으로 빠른 지도 생성
- **다양한 지도 타일**: OpenStreetMap, Stamen, Carto 등
- **마커와 팝업**: 위치 표시 및 정보 제공
- **GeoJSON, Shapefile 연동**: 공간 데이터와 통합 가능

#### 활용 기능
1. **CircleMarker**: 데이터 값의 크기를 원형 마커로 표현
2. **HeatMap**: 밀집도 시각화
3. **Choropleth Map**: 지역 단위 통계 데이터 시각화
4. **Layer Control**: 여러 레이어 관리

#### 응용 사례
- 교통사고 발생지점 시각화
- 공공데이터 위치정보 분석
- 기상 데이터 시각화
- 관광지 추천 지도 제작

### 6. Streamlit

#### 개요
- 데이터 사이언티스트와 머신러닝 엔지니어를 위한 웹 애플리케이션 프레임워크
- 복잡한 웹 개발 지식 없이 Python 코드만으로 웹 앱 구축
- Streamlit Community Cloud를 통한 무료 배포 지원

#### 핵심 장점
- **간단하고 Python 친화적**: 아름답고 읽기 쉬운 코드
- **빠른 프로토타이핑**: 실시간 피드백 가능
- **실시간 편집**: 스크립트 편집 시 앱 즉시 업데이트
- **오픈소스**: 활발한 커뮤니티 지원

#### 환경 설정

**Python 3.9를 사용하는 이유:**
- **패키지 호환성**: 일부 라이브러리나 프레임워크는 최신 버전의 Python에서 호환성 문제를 일으킬 수 있습니다. Python 3.9은 안정성과 호환성 면에서 널리 사용되며, 많은 주요 라이브러리가 이를 지원합니다.
- **스트림릿과의 호환성**: 스트림릿을 비롯한 많은 데이터 분석 및 웹 개발 라이브러리들이 Python 3.9에서 안정적으로 동작합니다. 최신 Python 버전에서는 일부 라이브러리가 아직 최적화되지 않거나 버전 충돌이 발생할 수 있습니다.

```bash
# Python 가상환경 생성
python -m venv streamlit_env
streamlit_env\Scripts\activate

# 또는 conda 환경 생성 (권장)
conda create -n streamlit_env python=3.9
conda activate streamlit_env

# Streamlit 설치
pip install streamlit
```

#### 기본 사용법
```python
import streamlit as st
st.write("Hello, Streamlit!")
```

```bash
streamlit run app.py
```

---

## 시각화 도구 비교표

| 도구 | 장점 | 단점 | 주요 용도 |
|------|------|------|-----------|
| **Matplotlib** | 높은 유연성, 커스터마이징 가능, 다양한 플롯 지원 | 기본 시각화가 복잡함 | 연구 논문, 정밀한 커스터마이징 |
| **Seaborn** | 통계적 시각화 최적화, 아름다운 기본 테마 | Matplotlib 의존성, 대화형 기능 부족 | 데이터 분석, 통계적 시각화 |
| **Plotly** | 인터랙티브 시각화, 웹 브라우저 지원, 간단한 API | 파일 크기 큼, 대규모 데이터 성능 문제 | 대화형 대시보드, 웹 기반 시각화 |
| **Folium** | 지도 시각화 특화, 인터랙티브 지도 | 지도 시각화로 제한됨 | 위치 기반 데이터 분석 |
| **Streamlit** | 웹 앱 쉬운 구축, 실시간 편집 | 웹 앱 기능으로 제한됨 | 데이터 앱 프로토타이핑, 배포 |

---

## 파일 구조

```
15week_cloud-data-viz/
├── 250818_cloud_data_viz.ipynb          # 메인 실습 노트북
├── 250818_cloud_data_viz_v2.ipynb       # 통합 실습 노트북 (오늘 학습 내용)
├── 72_dash_test.py                      # Dash 대시보드 예제
├── dataset/                             # 데이터셋 폴더
│   ├── global_internet_users.csv        # 글로벌 인터넷 사용자 데이터
│   └── EV_charge.csv                    # 전기차 충전 데이터
├── streamlit_env/                       # Streamlit 가상환경
├── requirements.txt                     # 패키지 의존성
├── .gitignore                          # Git 무시 파일
└── README.md                           # 프로젝트 설명서
```

---

## 📚 Plotly 고급 시각화 학습 정리 (CO2 분석 프로젝트)

### 🎯 학습 목표
- **Plotly Express vs Graph Objects** 차이점 이해 및 활용
- **인터랙티브 차트** 구현 기법 습득
- **다중 서브플롯** 구성 및 레이아웃 설계
- **고급 스타일링** 및 사용자 경험 최적화

---

### 📊 1. Plotly Express 기본 활용

#### 버블 차트 (Scatter Plot)
```python
# 3차원 데이터를 2D로 효과적 표현
fig_bubble = px.scatter(
    data, 
    x='Engine Size(L)', 
    y='CO2 Emissions(g/km)',
    size='Fuel Consumption Comb (mpg)',  # 버블 크기
    color='Make',                        # 색상 구분
    hover_data=['Model', 'Vehicle Class'], # 호버 정보
    size_max=20                          # 최대 버블 크기
)
```
**학습 포인트**: 3개 이상의 변수를 동시에 시각화하는 효과적인 방법

#### 박스플롯 분포 분석
```python
fig_box = px.box(
    data, 
    x='Vehicle Class', 
    y='CO2 Emissions(g/km)',
    color='Vehicle Class'  # 카테고리별 색상
)
```
**학습 포인트**: 범주형 데이터의 분포와 이상치를 한 번에 파악

#### 상관관계 시각화 (추세선 포함)
```python
fig_corr = px.scatter(
    data,
    x='Fuel Consumption Comb (mpg)',
    y='CO2 Emissions(g/km)',
    trendline='ols',  # 회귀선 자동 추가
    color='Vehicle Class'
)
```
**학습 포인트**: `trendline='ols'`로 통계적 관계를 시각적으로 표현

---

### 🔧 2. Graph Objects 고급 제어

#### 기준선 추가 기법
```python
# 수평선 (임계값 표시)
fig.add_hline(
    y=200, 
    line_dash="dash", 
    line_color="red",
    annotation_text="🚨 친환경 기준선 (200g/km)"
)

# 수직선 (기준값 표시)  
fig.add_vline(
    x=2.0,
    line_dash="dot",
    line_color="green", 
    annotation_text="💚 효율적 엔진 크기"
)
```
**학습 포인트**: 데이터에 의미 있는 기준선을 추가하여 해석력 향상

#### 영역 강조 표시
```python
# 사각형 영역 강조
fig.add_vrect(x0=35, x1=50, fillcolor="green", opacity=0.1)
fig.add_hrect(y0=120, y1=180, fillcolor="lightgreen", opacity=0.1)
```
**학습 포인트**: 특정 구간을 시각적으로 강조하여 중요 정보 전달

---

### 📐 3. 서브플롯 구성 및 다중 차트

#### 2x2 서브플롯 레이아웃
```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('차트1', '차트2', '차트3', '차트4'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"type": "pie"}]]  # 파이차트 지정
)

# 각 위치에 차트 추가
fig.add_trace(go.Bar(...), row=1, col=1)
fig.add_trace(go.Bar(...), row=1, col=2)  
fig.add_trace(go.Pie(...), row=2, col=2)
```
**학습 포인트**: 여러 관점의 분석을 하나의 대시보드로 통합

---

### 🎨 4. 고급 스타일링 및 레이아웃

#### 제목 및 축 레이블 고급 설정
```python
fig.update_layout(
    title={
        'text': '🌍 제목<br><sub>부제목</sub>',
        'x': 0.5,           # 중앙 정렬
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title='🔧 X축 제목',
    yaxis_title='🌱 Y축 제목'
)
```

#### 배경 및 색상 테마
```python
fig.update_layout(
    plot_bgcolor='rgba(240,248,255,0.8)',  # 연한 하늘색
    paper_bgcolor='white',
    font=dict(size=12)
)
```

#### 범례 위치 조정
```python
fig.update_layout(
    legend=dict(
        orientation="v",     # 세로 배치
        yanchor="top", y=1,
        xanchor="left", x=1.01  # 차트 오른쪽 외부
    )
)
```

#### 축 그리드 스타일링
```python
fig.update_xaxes(
    gridcolor='lightgray',
    gridwidth=1,
    showgrid=True,
    tickangle=45  # 레이블 회전
)
```

---

### 💡 5. 호버 정보 커스터마이징

```python
# 상세한 호버 템플릿 구성
hovertemplate=
'<b>%{y}</b><br>' +
'🌱 평균 CO2: %{x:.1f} g/km<br>' +
'⛽ 평균 연비: %{customdata[0]:.1f} mpg<br>' +
'🚗 차량 수: %{customdata[1]:.0f}대<br>' +
'<extra></extra>',  # 박스 테두리 제거
customdata=np.column_stack((연비데이터, 차량수데이터))
```
**학습 포인트**: 사용자가 차트와 상호작용할 때 풍부한 정보 제공

---

### 🔍 6. 데이터 전처리 및 분석 기법

#### 상위 데이터 필터링
```python
# 가독성을 위한 상위 N개 선택
top_makes = data['Make'].value_counts().head(15).index
filtered_data = data[data['Make'].isin(top_makes)]
```

#### 통계값 계산 및 그룹화
```python
# 제조사별 통계 (최소 N대 이상)
stats = data.groupby('Make').agg({
    'CO2 Emissions(g/km)': ['mean', 'count'],
    'Fuel Consumption Comb (mpg)': 'mean'
}).round(2)
stats = stats[stats[('CO2 Emissions(g/km)', 'count')] >= 5]
```

#### 환경 점수 계산
```python
# 복합 지표 생성
stats['환경점수'] = (
    (300 - stats['평균_CO2']) * 0.6 +    # CO2 비중 60%
    (stats['평균_연비'] * 3) * 0.4       # 연비 비중 40%  
).round(1)
```

---

### ⚡ 7. 성능 최적화 팁

1. **대용량 데이터**: 상위 N개 필터링으로 렌더링 속도 개선
2. **색상 최적화**: `px.colors.qualitative.Set3` 등 미리 정의된 팔레트 사용
3. **메모리 관리**: 불필요한 컬럼 제거 및 데이터 타입 최적화
4. **차트 크기**: `width`, `height` 명시적 설정으로 레이아웃 안정화

---

### 🎓 핵심 학습 성과

1. **Plotly Express**: 빠른 프로토타이핑과 기본 인터랙티브 차트
2. **Graph Objects**: 세밀한 제어와 고급 커스터마이징
3. **서브플롯**: 다각도 분석을 위한 통합 대시보드 구성
4. **스타일링**: 전문적이고 사용자 친화적인 시각화 디자인
5. **데이터 스토리텔링**: 기준선, 영역 강조 등으로 인사이트 강화

**다음 학습 목표**: Streamlit과 연동하여 웹 애플리케이션으로 배포하기

---

## 실습 내용

### 주요 실습 파일
- **250818_cloud_data_viz.ipynb**: 메인 실습 노트북
- **250818_cloud_data_viz_v2.ipynb**: 통합 실습 노트북 (Seaborn + Plotly + Folium)
- **CO2_Plotly_Visualization.ipynb**: CO2 배출량 데이터 종합 분석 (인터랙티브 시각화)
- **CO2_Visualization_V2.ipynb**: CO2 데이터 간단 버전 분석
- **streamlit_dashboard.py**: Streamlit 기반 대시보드 애플리케이션
- **72_dash_test.py**: Dash 인터랙티브 대시보드 예제

### 주요 실습 데이터
- **Tips 데이터셋**: 팁 데이터를 활용한 기본 시각화 실습
- **Global Internet Users**: 전 세계 인터넷 사용자 데이터 시각화
- **CO2 Emissions**: 7,385대 차량의 CO2 배출량 환경 분석 데이터
- **ABNB Stock**: 에어비앤비 주식 데이터 (캔들스틱 차트, 거래량 분석)
- **EV Charge**: 전기차 충전 패턴 및 사용량 분석 데이터
- **Medical Cost**: 의료비 영향 요인 분석 데이터
- **Seaborn 내장 데이터셋**: 다양한 통계 차트 실습
- **스타벅스 매장 데이터**: API 연동을 통한 실시간 지도 시각화

### 학습 순서
1. 데이터 시각화 기초 개념 이해
2. Matplotlib을 통한 기본 차트 작성
3. Seaborn을 활용한 통계적 시각화
4. Plotly로 인터랙티브 차트 구현
5. Folium으로 지도 기반 시각화
6. Dash를 활용한 웹 대시보드 구축
7. Streamlit으로 웹 애플리케이션 배포

### 오늘 배운 핵심 내용 요약

#### **Seaborn 통계 시각화**
- **scatter plot**: 상관관계 및 분포 탐색, hue/size/style 매개변수 활용
- **regplot**: 회귀선과 신뢰구간 시각화로 관계 분석
- **lineplot**: 시계열 데이터의 추세 확인
- **boxplot/violinplot**: 분포와 이상치 탐지, 통계량 비교
- **barplot**: 범주별 평균값 비교, 에러바를 통한 변동성 확인
- **histplot**: 수치형 데이터의 분포 패턴 분석
- **heatmap**: 피벗테이블 기반 데이터 요약 시각화
- **FacetGrid**: 다차원 데이터의 범주별 분할 시각화

#### **Plotly 인터랙티브 시각화**
- **Express vs Graph Objects**: 고수준/저수준 인터페이스 차이점
- **hover_data**: 마우스 오버 시 추가 정보 표시
- **애니메이션**: animation_frame을 통한 동적 시각화
- **3D 시각화**: scatter_3d로 다차원 관계 표현
- **색상 팔레트**: qualitative, sequential, diverging 색상 체계
- **템플릿**: plotly_white, plotly_dark 등 테마 적용

#### **Plotly Dash 웹 대시보드**
- **컴포넌트 구조**: html.Div, dcc.Graph, dcc.Dropdown 등
- **콜백 함수**: @callback 데코레이터를 통한 상호작용 구현
- **Input/Output**: 사용자 입력과 차트 업데이트 연결
- **레이아웃 설계**: CSS 스타일과 반응형 디자인

#### **Folium 지도 시각화**
- **기본 지도**: 위도/경도 기반 지도 생성
- **마커 시스템**: Marker, CircleMarker, 아이콘 커스터마이징
- **팝업/툴팁**: 사용자 상호작용을 위한 정보 표시
- **클러스터링**: MarkerCluster를 통한 밀집 지역 그룹화
- **히트맵**: HeatMap 플러그인으로 밀집도 시각화
- **타일 스타일**: OpenStreetMap, CartoDB, Stamen 등 다양한 스타일
- **실시간 데이터**: API 연동을 통한 동적 지도 생성

#### **실무 적용 포인트**
1. **데이터 탐색 단계**: Seaborn으로 빠른 EDA 수행
2. **프레젠테이션**: Plotly로 인터랙티브 시각화
3. **웹 배포**: Dash로 대시보드 구축
4. **지리 분석**: Folium으로 위치 기반 인사이트 도출
5. **성능 고려사항**: 대용량 데이터에서 렌더링 최적화

---

## 참고 자료

- [Matplotlib 공식 문서](https://matplotlib.org/)
- [Seaborn 공식 문서](https://seaborn.pydata.org/)
- [Plotly 공식 문서](https://plotly.com/python/)
- [Streamlit 공식 문서](https://streamlit.io/)

---

*생성일: 2025년 8월 18일*  
*15주차 클라우드 기반 데이터 시각화 과정*
