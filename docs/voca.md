# 투자분석 핵심 용어집 — Python Quant Lab

이 문서는 **Python Quant Lab**의 4대 분석 축(매크로·산업적·기본적·기술적)과 통합 리포트, 퀀트 전략, ML/DL 금융 예측, 웹앱 개발에서 반복 등장하는 핵심 용어를  
초등학생도 이해할 수 있는 수준의 쉬운 뜻 + 실전 예시로 정리한 사전입니다.

> 📖 관련 문서:
> - [docs/27.md](27.md) ~ [docs/36.md](36.md) — 모듈 7 전체 강의자료
> - [readme.md](../readme.md) — 전체 커리큘럼 및 API 구성

---

## 목차

1. [매크로 분석 용어](#1-매크로-분석-macro-analysis-용어)
2. [산업적 분석 용어](#2-산업적-분석-industry-analysis-용어)
3. [기본적 분석 용어](#3-기본적-분석-fundamental-analysis-용어)
4. [기술적 분석 용어](#4-기술적-분석-technical-analysis-용어)
5. [통합 리포트 & 투자의견 용어](#5-통합-리포트--투자의견-용어)
6. [퀀트 전략 & 포트폴리오 용어](#6-퀀트-전략--포트폴리오-용어)
7. [ML/DL 금융 예측 용어](#7-mldl-금융-예측-용어)
8. [웹앱 & API 개발 용어](#8-웹앱--api-개발-용어)
9. [통계·수학 기초](#9-통계수학-기초-statistics--math-basics)
10. [파이썬 실습 — 기초 통계 + 금융 데이터 확인](#10-파이썬-실습--기초-통계--금융-데이터-확인)
11. [자주 혼동하는 용어 비교](#11-자주-혼동하는-용어-비교)

---

## 1. 매크로 분석 (Macro Analysis) 용어

> 금리, 물가, 환율, 유가 같은 경제 전체의 큰 흐름을 읽는 데 필요한 용어

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 거시경제 | 巨視經濟 | Macroeconomics | 나라 전체 경제를 큰 그림으로 보는 것 | "금리가 오르면 집값·주가가 어떻게 될까?" |
| 기준금리 | 基準金利 | Base Rate | 중앙은행이 정하는 기본 이자율 | 한국은행이 3.5%로 올리면 은행 대출금리도 따라 오름 |
| 물가상승률(CPI) | 物價上昇率 | Inflation Rate | 물건 가격이 평균적으로 오른 비율 | 작년보다 라면 가격이 10% 오르면 인플레이션 |
| PPI | - | Producer Price Index | 생산자 물가지수 — 공장 출고 단계의 물가 | PPI 먼저 오르면 나중에 CPI도 오르는 경향 |
| PCE | - | Personal Consumption Expenditure | 개인소비지출 물가지수 — 미국 연준이 선호하는 인플레이션 지표 | 미국 금리 결정의 핵심 참고 지표 |
| 실업률 | 失業率 | Unemployment Rate | 일하고 싶은데 일자리 없는 사람 비율 | 실업률 높으면 경기 나쁜 신호 |
| 환율 | 換率 | Exchange Rate | 돈을 다른 나라 돈으로 바꿀 때의 비율 | USD/KRW 1,360 = 달러 1개에 원 1,360원 |
| 유가 | 油價 | Oil Price (WTI) | 원유(기름) 가격 | WTI 80달러 = 미국 기준 원유 배럴당 가격 |
| GDP | - | Gross Domestic Product | 한 나라가 1년에 만들어낸 가치 총합 | 우리나라 GDP 성장률 3% = 경제 규모가 3% 커진 것 |
| 경기사이클 | 景氣循環 | Business Cycle | 경기가 상승·과열·둔화·침체를 반복하는 패턴 | 상승기→과열기→침체기→회복기 4단계 |
| 장단기 금리차 | 長短期金利差 | Yield Spread | 장기 국채금리 - 단기 국채금리 | 역전(단기>장기)되면 경기 침체 선행 신호 |
| 수익률 곡선 | - | Yield Curve | 만기별 채권 수익률을 이은 곡선 | 정상: 우상향 / 역전: 우하향 |
| GBM | - | Geometric Brownian Motion | 가격이 랜덤하게 움직이는 수학 모델 | 주가·금리 시뮬레이션에 사용하는 공식 |
| 상관관계 | 相關關係 | Correlation | 두 지표가 같이 움직이는 정도 | 금리↑ → 채권가격↓ 처럼 반대로 움직이면 음의 상관 |
| 섹터 로테이션 | - | Sector Rotation | 경기 국면에 따라 유망 업종이 바뀌는 현상 | 경기 회복기 → 소재·산업재 선호 |

---

## 2. 산업적 분석 (Industry Analysis) 용어

> 특정 산업의 경쟁력과 매력도를 평가하는 데 필요한 용어

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 포터 5가지 힘 | - | Porter's 5 Forces | 산업의 경쟁 강도를 5개 축으로 분석하는 도구 | 신규 진입 장벽이 높으면 기존 기업이 유리 |
| PEST 분석 | - | PEST Analysis | 정치·경제·사회·기술 환경을 분석하는 틀 | 전기차 법 개정(P)이 배터리 업종에 미치는 영향 |
| SWOT 분석 | - | SWOT Analysis | 강점·약점·기회·위협을 정리하는 도구 | 삼성전자: 강점=기술력, 위협=중국 경쟁사 |
| 산업 수명주기 | 産業壽命週期 | Industry Life Cycle | 산업이 도입→성장→성숙→쇠퇴 단계를 거치는 과정 | 반도체: 성장기 / 석탄: 쇠퇴기 |
| TAM | - | Total Addressable Market | 해당 제품·서비스가 공략 가능한 전체 시장 규모 | AI 소프트웨어 TAM 2030년 1조 달러 전망 |
| SAM | - | Serviceable Addressable Market | 현실적으로 접근 가능한 시장 규모 | TAM 중 자사 제품이 실제 판매될 수 있는 범위 |
| 업종 KPI | - | Key Performance Indicator | 그 업종에서 가장 중요한 성과 지표 | 반도체: 영업이익률, 은행: NIM(순이자마진) |
| Peer Comparison | - | Peer Comparison | 같은 업종 경쟁사와 수치를 비교 분석하기 | 삼성전자 PER vs SK하이닉스 PER 비교 |
| 시장점유율 | 市場占有率 | Market Share | 전체 시장에서 내 기업이 차지하는 비율 | 카카오페이 결제 시장 점유율 20% |
| 진입장벽 | 進入障壁 | Entry Barrier | 새 경쟁자가 시장에 들어오기 어려운 조건 | 반도체 공장 수조 원 투자 필요 → 높은 장벽 |
| 경제적 해자 | - | Economic Moat | 경쟁사가 쉽게 넘어오지 못하는 지속 경쟁우위 | 브랜드·특허·네트워크효과·원가우위·전환비용 |
| 공급망 | 供給網 | Supply Chain | 원료에서 완제품까지 이어지는 생산·유통 흐름 | 배터리: 리튬광산→셀→팩→완성차 |
| 수직계열화 | 垂直系列化 | Vertical Integration | 공급망의 여러 단계를 한 기업이 통합 운영 | 애플이 자체 칩(M시리즈)을 직접 설계·생산 |

---

## 3. 기본적 분석 (Fundamental Analysis) 용어

### 3-1. 재무제표 (Financial Statements)

| 용어 | 한자 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 재무제표 | 財務諸表 | Financial Statements | 회사의 성적표 3종 세트 | 손익계산서·재무상태표·현금흐름표 |
| 손익계산서 | 損益計算書 | Income Statement | 일정 기간 벌고 쓴 결과표 | 매출→원가→판관비→영업이익→순이익 흐름 |
| 재무상태표 | 財務狀態表 | Balance Sheet | 특정 시점의 자산·부채·자본 표 | 자산 = 부채 + 자본 |
| 현금흐름표 | 現金흐름表 | Cash Flow Statement | 현금이 왜 늘고 줄었는지 표 | 영업/투자/재무 현금흐름 3개로 구분 |
| 매출액 | 賣出額 | Revenue | 물건·서비스 팔아 번 총액 | 삼성전자 연 매출 300조 원 |
| 영업이익 | 營業利益 | Operating Profit | 본업으로 번 이익 | 매출 - 원가 - 판관비 |
| 순이익 | 純利益 | Net Income | 세금까지 다 뺀 최종 이익 | 영업이익 - 이자비용 - 법인세 |
| CFO | - | Operating Cash Flow | 본업에서 들어온 실제 현금 | 순이익 흑자여도 CFO 마이너스면 이익의 질 낮음 |
| FCF | - | Free Cash Flow | 설비투자 후 남은 현금 | CFO - Capex(설비투자) |
| 감가상각 | 減價償却 | Depreciation | 자산 가치가 시간이 지나며 줄어드는 것 | 컴퓨터를 5년에 걸쳐 비용으로 인식 |

### 3-2. 가치평가 (Valuation)

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 밸류에이션 | 價値評價 | Valuation | 기업의 적정 가치를 계산하는 일 | "삼성전자가 얼마짜리 회사인가?" |
| DCF | - | Discounted Cash Flow | 미래 현금흐름을 현재 가치로 할인해 기업 가치 계산 | 5년치 FCF를 WACC로 할인해 합산 |
| EVA | - | Economic Value Added | 투자된 자본 비용을 넘어서 실제로 번 경제적 이익 | NOPAT - (투자자본 × WACC) |
| WACC | - | Weighted Average Cost of Capital | 자기자본비용과 부채비용의 가중평균 | 주식 조달 비용 + 대출 이자 비용을 합친 것 |
| 터미널 밸류 | - | Terminal Value | 예측 기간 이후 영구 현금흐름의 현재 가치 | FCFn × (1+g) ÷ (r - g) |
| PER | 株價收益比率 | Price Earnings Ratio | 주가가 1주당 이익의 몇 배인지 | PER 15 = 지금 주가가 연이익의 15배 |
| PBR | 株價純資産比率 | Price Book Ratio | 주가가 순자산의 몇 배인지 | PBR 1 이하 = 청산가치보다 싸게 거래 |
| PSR | 株價賣出比率 | Price Sales Ratio | 주가가 매출의 몇 배인지 | 적자 기업 밸류에이션에 활용 |
| EV/EBITDA | - | Enterprise Value / EBITDA | 기업 전체 가치가 세전이익의 몇 배인지 | 10배 이하면 저평가 가능성 |
| EPS | - | Earnings Per Share | 주식 1주당 이익 | 순이익 ÷ 총 발행주식 수 |
| 내재가치 | 內在價値 | Intrinsic Value | 계산으로 구한 기업의 진짜 적정 가격 | DCF로 구한 주당 가치 vs 현재 주가 비교 |
| 안전마진 | 安全餘白 | Margin of Safety | 내재가치 대비 주가가 얼마나 싼지 여유 | 내재가치 10만원, 주가 7만원 → 30% 안전마진 |
| 목표주가 | 目標株價 | Price Target | 애널리스트가 산출한 6~12개월 적정 주가 | "삼성전자 목표주가 90,000원, 매수" |
| PER 밴드 | - | PER Band Chart | 과거 PER 범위를 주가와 함께 표시한 차트 | 현재 PER이 역사적 하단 → 저평가 신호 |
| 업사이드 | - | Upside Potential | 현재 주가 대비 목표주가까지 상승 여력 | 현재 7만원, 목표 8만4천원 → 업사이드 +20% |

### 3-3. 포트폴리오·리스크

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 포트폴리오 | - | Portfolio | 내 투자 바구니 전체 구성 | 주식 50% + 채권 30% + 현금 20% |
| 분산투자 | 分散投資 | Diversification | 여러 곳에 나눠 투자해 위험 줄이기 | 계란을 한 바구니에 담지 않기 |
| 샤프 비율 | - | Sharpe Ratio | 위험 1단위당 초과수익 | 샤프 1.0 이상이면 준수한 전략 |
| VaR | - | Value at Risk | 일정 신뢰수준에서 최대 예상 손실 | 95% VaR 5% = 100일 중 5일 이상 -5% 손실 가능 |
| CVaR | - | Conditional VaR | VaR를 초과한 경우의 평균 손실 | VaR 이상 손실 날 때 평균 손실 크기 |
| MDD | 最大落幅 | Maximum Drawdown | 최고점 대비 가장 크게 빠진 낙폭 | 100에서 70까지 떨어지면 MDD -30% |
| 리밸런싱 | 再均衡 | Rebalancing | 비율이 어긋나면 원래대로 되돌리기 | 주식 비중이 60%→70%로 커지면 채권으로 이동 |
| 상관계수 | 相關係數 | Correlation Coefficient | -1~+1 사이로 두 자산의 동조화 정도 | -1에 가까울수록 서로 반대로 움직임 |

---

## 4. 기술적 분석 (Technical Analysis) 용어

### 4-1. 추세·이동평균

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 추세 | 趨勢 | Trend | 가격이 꾸준히 움직이는 방향 | 상승추세: 저점이 계속 높아짐 |
| 이동평균선(MA) | 移動平均線 | Moving Average | 최근 N일 종가의 평균선 | 5일선, 20일선, 60일선 |
| 골든크로스 | - | Golden Cross | 단기 MA가 장기 MA를 위로 돌파 | 5일선이 20일선을 위로 넘으면 매수 신호 |
| 데드크로스 | - | Dead Cross | 단기 MA가 장기 MA를 아래로 돌파 | 5일선이 20일선 아래로 내리면 매도 신호 |
| 정배열 | 正配列 | Bullish MA Alignment | 단기선이 장기선보다 위에 있는 배열 | 5일 > 20일 > 60일 → 강한 상승 신호 |
| 역배열 | 逆配列 | Bearish MA Alignment | 단기선이 장기선보다 아래 배열 | 5일 < 20일 < 60일 → 강한 하락 신호 |
| 지지선 | 支持線 | Support Line | 가격이 내려올 때 멈추는 바닥 수준 | 코스피 2,400이 반복적으로 지지 역할 |
| 저항선 | 抵抗線 | Resistance Line | 가격이 올라갈 때 막히는 천장 수준 | 삼성전자 80,000원에서 반복 하락 |
| 추세채널 | 趨勢채널 | Trend Channel | 추세선 + 평행선으로 만든 통로 | 상승채널 상단에서 매도, 하단에서 매수 |
| ADX | - | Average Directional Index | 추세 강도를 0~100으로 나타낸 지표 | ADX 25 이상이면 추세가 뚜렷함 |

### 4-2. 보조지표

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| RSI | - | Relative Strength Index | 최근 N일간 상승/하락 힘의 비율 | RSI < 30 과매도, RSI > 70 과매수 |
| MACD | - | Moving Average Convergence Divergence | 단기·장기 MA 차이와 그 신호선 | MACD가 시그널을 위로 돌파 → 매수 |
| 볼린저밴드 | - | Bollinger Bands | 이동평균 ± 2σ로 만든 밴드 | 주가가 상단 돌파 시 과열, 하단 이탈 시 침체 |
| 갭 | - | Gap | 전날 종가와 오늘 시가 사이의 빈 공간 | 상승갭 + 거래량 급증 = 강한 매수 신호 |
| 피보나치 되돌림 | - | Fibonacci Retracement | 상승폭의 38.2%, 50%, 61.8% 지점 | 상승 후 61.8% 되돌림에서 다시 반등 기대 |

### 4-3. 캔들차트·패턴

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 캔들차트 | - | Candlestick Chart | 시가·고가·저가·종가를 막대로 표현한 차트 | 빨간 캔들=종가>시가, 파란 캔들=종가<시가 |
| 해머 | - | Hammer | 긴 아래꼬리 + 짧은 몸통 = 매수세 강화 신호 | 하락 끝에 나오면 반등 가능성 |
| 장악형 | 長握型 | Engulfing Pattern | 전날 몸통을 다음날 큰 몸통이 완전히 덮는 패턴 | 하락 장악형 = 상승 끝에 나오면 매도 신호 |
| 헤드앤숄더 | - | Head and Shoulders | 산 3개 모양 = 상승 추세 종료 패턴 | 목선 하향 이탈 시 매도, 목표가 = 고점-목선 |
| 이중바닥 | - | Double Bottom | W자 모양 = 하락 추세 반전 패턴 | 두 번째 저점이 첫 번째보다 높으면 신뢰도 증가 |
| 엘리어트파동 | - | Elliott Wave | 충격 5파 + 조정 3파의 반복 패턴 | 2파 저점에서 진입, 5파 완성 시 청산 |

### 4-4. 백테스트·퀀트 파이프라인

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 백테스트 | 過去檢證 | Backtest | 과거 데이터로 전략의 성과를 시뮬레이션 | "2020~2024 동안 내 전략의 수익률은?" |
| 시그널 | 信號 | Signal | 매수·매도를 발생시키는 조건 | RSI<30이 되는 순간 매수 시그널 |
| 슬리피지 | - | Slippage | 예상 체결가와 실제 체결가의 차이 | 큰 거래에서 주가가 밀려 손실이 추가됨 |
| 팩터 | 要因 | Factor | 수익률을 설명하는 특성 변수 | 저PER, 모멘텀, 저변동성 팩터 |
| 알파 | α | Alpha | 시장 대비 초과수익 | KOSPI +5%, 내 전략 +12% → 알파 +7% |
| 베타 | β | Beta | 시장 수익률 대비 민감도 | 베타 1.5 = 시장이 10% 오를 때 15% 상승 |
| 오버피팅 | - | Overfitting | 과거 데이터에만 너무 맞춰 실전에서 안 통하는 현상 | 학습 성적 100점인데 실전 시험 낙제 |
| 퀀트 파이프라인 | - | Quant Pipeline | 데이터 수집 → 지표 계산 → 시그널 생성 → 백테스트 자동화 흐름 | QuantPipeline.py로 전 과정 자동 실행 |

---

## 5. 통합 리포트 & 투자의견 용어

> 기본적 분석 + 기술적 분석을 합친 통합 리포트에서 사용하는 용어

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 통합 리포트 | 統合報告書 | Integrated Report | 기본적·기술적 분석을 하나의 문서로 합친 투자 의견서 | 증권사 애널리스트가 발행하는 주식 리서치 리포트 |
| 투자의견 | 投資意見 | Investment Rating | 주식에 대한 매수·보유·매도 등 권고 의견 | Goldman Sachs 삼성전자 "Buy" 등급 유지 |
| 강력매수 | 强力買收 | Strong Buy | 목표주가 대비 큰 업사이드 + 강한 기술적 신호 | 총점 75점 이상 → Strong Buy |
| 비중확대 | 比重擴大 | Overweight | 해당 섹터 비중을 벤치마크보다 늘리라는 권고 | "IT 섹터 Overweight 유지" |
| 목표주가 | 目標株價 | Price Target | DCF·멀티플 복합 산출한 12개월 목표 가격 | PER 12배 × EPS 7,500원 = 목표 90,000원 |
| 업사이드 | - | Upside / Upside Potential | 현재가 대비 목표주가까지 상승 여지 | 현재 75,000원, 목표 90,000원 → 업사이드 +20% |
| 시나리오 분석 | - | Scenario Analysis | Bull/Base/Bear 세 가지 시나리오별 목표주가 산출 | Bull: 10만원, Base: 9만원, Bear: 7만5천원 |
| 리스크 요인 | - | Risk Factor | 주가 하락 또는 목표주가 미달 가능성이 있는 요소 | 규제 리스크, 경쟁 심화, 금리 상승 |
| 스코어링 | - | Scoring | 여러 지표에 점수를 부여해 합산·비교하는 방식 | FA 40점 + TA 40점 + 거시 20점 = 100점 만점 |
| 종합점수 | 綜合點數 | Composite Score | 기본적·기술적·거시 점수를 가중합산한 최종 점수 | 78점 → 매수 의견 |
| 손절가 | 損切價 | Stop-Loss Price | 손실 제한을 위해 미리 정해두는 매도 가격 | MA60 이탈 시 손절 실행 |
| 목표가 밴드 | - | Price Target Band | 상단(Bull)·중앙(Base)·하단(Bear) 세 목표주가 범위 | 밴드 상단 = 낙관, 하단 = 비관 시나리오 |
| Equity Research | - | Equity Research | 증권사·투자은행이 발행하는 주식 분석 보고서 | 매수/목표주가/실적추정 포함 10~30페이지 문서 |
| Buy-Side | - | Buy-Side | 자산운용사·연기금처럼 투자 집행 주체 | 국민연금, 미래에셋자산운용 |
| Sell-Side | - | Sell-Side | 증권사처럼 분석 리포트를 발행하는 주체 | 삼성증권, Goldman Sachs 리서치 센터 |

---

## 6. 퀀트 전략 & 포트폴리오 용어

> 퀀트 전략 수립, 포트폴리오 최적화, 리스크 관리에서 자주 쓰이는 용어

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 포트폴리오 | - | Portfolio | 내 투자 바구니 전체 구성 | 주식 50% + 채권 30% + 현금 20% |
| 분산투자 | 分散投資 | Diversification | 여러 곳에 나눠 투자해 위험 줄이기 | 계란을 한 바구니에 담지 않기 |
| 샤프 비율 | - | Sharpe Ratio | 위험 1단위당 초과수익 | 샤프 1.0 이상이면 준수한 전략 |
| 칼마 비율 | - | Calmar Ratio | 연 수익률 ÷ 최대 낙폭(MDD) | 칼마 1.0 이상 = MDD 대비 수익률이 좋음 |
| VaR | - | Value at Risk | 일정 신뢰수준에서 최대 예상 손실 | 95% VaR 5% = 100일 중 5일 이상 -5% 손실 가능 |
| CVaR | - | Conditional VaR | VaR를 초과한 경우의 평균 손실 | VaR 이상 손실 날 때 평균 손실 크기 |
| MDD | 最大落幅 | Maximum Drawdown | 최고점 대비 가장 크게 빠진 낙폭 | 100에서 70까지 떨어지면 MDD -30% |
| 리밸런싱 | 再均衡 | Rebalancing | 비율이 어긋나면 원래대로 되돌리기 | 주식 비중이 60%→70%로 커지면 채권으로 이동 |
| 상관계수 | 相關係數 | Correlation Coefficient | -1~+1 사이로 두 자산의 동조화 정도 | -1에 가까울수록 서로 반대로 움직임 |
| MPT | - | Modern Portfolio Theory | 수익-위험 최적화로 효율적 포트폴리오를 구성하는 이론 | 주어진 위험 수준에서 최대 수익률 조합 찾기 |
| 효율적 프론티어 | - | Efficient Frontier | 동일 위험에서 최고 수익을 내는 포트폴리오 집합 | 위험-수익 평면에서 곡선 위쪽에 위치한 포트폴리오 |
| 모멘텀 팩터 | - | Momentum Factor | 최근 성과가 좋은 주식이 계속 좋을 가능성 활용 | 최근 6개월 수익률 상위 20% 종목 매수 |
| 저변동성 팩터 | - | Low Volatility Factor | 변동성이 낮은 주식이 장기적으로 좋은 성과 내는 현상 | 표준편차 하위 20% 종목 매수 |
| 퀀텀 스코어링 | - | Multi-Factor Scoring | 여러 팩터 점수를 합산해 종목 순위를 매기는 방식 | 저PER+고ROE+모멘텀 점수 합산 상위 30 매수 |
| 승률 | 勝率 | Win Rate | 전체 거래 중 수익 거래의 비율 | 60% 승률 = 10번 중 6번 이익 |
| 페이오프 비율 | - | Payoff Ratio | 평균 이익 ÷ 평균 손실 | 2.0 = 이익이 손실의 2배 → 승률 33%여도 수익 가능 |

---

## 7. ML/DL 금융 예측 용어

> 머신러닝·딥러닝을 금융 시계열 예측에 적용할 때 필요한 용어

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 지도학습 | 指導學習 | Supervised Learning | 정답(레이블)이 있는 데이터로 학습 | 어제 지표로 내일 주가 방향(상/하) 예측 |
| 비지도학습 | 非指導學習 | Unsupervised Learning | 정답 없이 데이터 패턴을 스스로 찾기 | K-Means로 비슷한 주가 패턴끼리 묶기 |
| 훈련·검증·테스트 분리 | - | Train/Val/Test Split | 학습·검증·최종평가를 위해 데이터를 나누기 | 80% 훈련, 10% 검증, 10% 최종 테스트 |
| 오버피팅 | - | Overfitting | 훈련 데이터에 너무 맞춰 새 데이터에는 못 쓰는 현상 | 훈련 정확도 99% → 실전 정확도 52% |
| 교차검증 | 交叉檢證 | Cross Validation | 데이터를 K개로 나눠 K번 훈련·검증을 반복하는 방법 | K=5 폴드 교차검증으로 안정적인 성능 평가 |
| 특성공학 | 特性工學 | Feature Engineering | 원시 데이터에서 모델에 유용한 변수를 만드는 작업 | 주가로 RSI·MACD·5일 수익률 변수 추가 |
| 랜덤 포레스트 | - | Random Forest | 수많은 결정 트리를 앙상블해 예측하는 모델 | 100개 트리의 평균으로 주가 방향 예측 |
| SVM | - | Support Vector Machine | 데이터를 두 그룹으로 최대한 잘 나누는 경계선을 찾는 모델 | 주가 상승/하락 분류 |
| LSTM | - | Long Short-Term Memory | 과거 정보를 선택적으로 기억하는 RNN의 발전 모델 | 60일 주가 시퀀스 → 다음 날 주가 예측 |
| CNN | - | Convolutional Neural Network | 패턴 인식에 강한 합성곱 신경망 | 주가 차트 이미지로 패턴 인식, 시계열 특성 추출 |
| Transformer | - | Transformer | 어텐션 메커니즘으로 장거리 의존성을 잡는 모델 | GPT·BERT 기반, 주가 시계열의 복잡한 패턴 학습 |
| 어텐션 | - | Attention Mechanism | 중요한 시점에 더 집중하게 만드는 신경망 메커니즘 | 실적 발표일·금리 결정일 주가에 더 높은 가중치 |
| 감성분석 | 感性分析 | Sentiment Analysis | 텍스트가 긍정·중립·부정인지 자동 판단 | 뉴스·공시 제목을 분석해 주가 방향 예측 보조 |
| RMSE | - | Root Mean Squared Error | 예측값과 실제값 차이를 제곱해 평균 후 루트 | 주가 예측 오차 측정, 낮을수록 정확 |
| 정확도 | 正確度 | Accuracy | 전체 예측 중 맞춘 비율 | 60% 정확도 = 상승/하락 방향을 10번 중 6번 맞힘 |
| 파이프라인 | - | Pipeline | 데이터 전처리 → 모델 학습 → 예측을 자동화한 흐름 | sklearn Pipeline으로 스케일링+학습 한 번에 |

---

## 8. 웹앱 & API 개발 용어

> FastAPI 백엔드와 Vanilla JS 프론트엔드로 구성된 웹앱 개발에서 쓰이는 용어

| 용어 | 한자/약어 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| REST API | - | REST API | 요청(Request)을 보내면 데이터(Response)를 돌려주는 웹 통신 규칙 | `GET /api/stock/005930.KS` → 삼성전자 데이터 반환 |
| FastAPI | - | FastAPI | Python으로 API를 빠르게 만드는 웹 프레임워크 | `@app.post("/api/quant/backtest")` 한 줄로 엔드포인트 생성 |
| 엔드포인트 | - | Endpoint | API에서 데이터를 요청할 수 있는 URL 주소 | `/api/macro/realtime`, `/api/quant/backtest` |
| Pydantic | - | Pydantic | 데이터 유효성 검사·직렬화를 자동으로 해주는 Python 라이브러리 | `class BacktestRequest(BaseModel): fast_ma: int = 20` |
| uvicorn | - | uvicorn | FastAPI를 실행하는 비동기 ASGI 웹 서버 | `uvicorn main:app --port 8000` |
| SPA | - | Single Page Application | 페이지를 새로 불러오지 않고 화면만 교체하는 방식 | 버튼 클릭 시 URL은 변경되지만 전체 페이지 리로드 없음 |
| Fetch API | - | Fetch API | 브라우저 내장 HTTP 요청 함수 | `fetch('/api/quant/backtest', {method:'POST', body:...})` |
| Canvas API | - | Canvas API | 브라우저에서 픽셀 단위로 그림을 그리는 HTML5 API | 캔들 차트·레이더차트를 Canvas에 직접 렌더링 |
| Chart.js | - | Chart.js | 웹 브라우저에서 차트를 쉽게 그려주는 JavaScript 라이브러리 | 레이더차트·막대·선 차트 구현에 활용 |
| base64 | - | Base64 | 바이너리 데이터(이미지 등)를 텍스트로 변환하는 인코딩 방식 | matplotlib 차트 PNG를 base64로 변환해 JSON으로 전송 |
| CORS | - | Cross-Origin Resource Sharing | 다른 도메인의 요청을 허용하는 보안 설정 | 프론트(포트 3000)가 백엔드(포트 8000)에 요청할 때 필요 |
| 환경변수 | 環境變數 | Environment Variable | 소스코드 밖에서 설정값을 주입하는 방식 | `.env` 파일에 `DART_API_KEY=abc123` 저장 |
| Gzip 압축 | - | Gzip Compression | 서버 응답 데이터를 압축해 전송 속도 향상 | FastAPI `GZipMiddleware`로 대용량 차트 PNG 전송 가속 |
| 정적 파일 | 靜的 - | Static Files | HTML·CSS·JS처럼 서버에서 변경 없이 그대로 제공되는 파일 | FastAPI `StaticFiles`로 `frontend/` 폴더를 웹에 제공 |
| WebSocket | - | WebSocket | 서버-클라이언트 간 실시간 양방향 통신 방식 | 주가 실시간 스트리밍, 알림 푸시 |

---

## 9. 통계·수학 기초 (Statistics & Math Basics)

> 퀀트 분석에서 자주 쓰이는 통계 개념

| 용어 | 한자 | 영어 | 아주 쉬운 뜻 | 실전 예시 |
|---|---|---|---|---|
| 평균 | 平均 | Mean | 값을 모두 더해 개수로 나눈 대표값 | 5일 수익률 합계 ÷ 5 |
| 표준편차 | 標準偏差 | Standard Deviation | 평균에서 얼마나 흩어져 있는지 정도 | 변동성(volatility)의 계산 기초 |
| 정규분포 | 正規分布 | Normal Distribution | 평균 중심으로 종 모양으로 퍼진 분포 | 주가 수익률이 정규분포를 따른다는 가정 |
| 분위수 | 分位數 | Quantile | 데이터를 순서대로 정렬했을 때 특정 위치 값 | VaR 5% = 하위 5% 손실 구간 |
| 상관계수 | 相關係數 | Correlation Coefficient | -1~+1 사이 두 변수 관계의 방향·강도 | r=0.9 → 강한 양의 상관 |
| 회귀분석 | 回歸分析 | Regression Analysis | 변수 간 선형 관계를 찾는 분석 | 금리 변화가 주가에 미치는 영향 측정 |
| p값 | - | p-value | 결과가 우연일 가능성 | p<0.05이면 통계적으로 유의미 |
| 신뢰구간 | 信賴區間 | Confidence Interval | 진짜 값이 포함될 가능성이 높은 범위 | 95% CI: 수익률이 -2%~+8% 사이일 가능성 95% |
| t-검정 | t-檢定 | t-test | 두 그룹 평균 차이가 실제 차이인지 검증 | 전략 A vs B 수익률 차이가 유의미한지 확인 |
| ANOVA | 分散分析 | Analysis of Variance | 3개 이상 그룹 평균 차이 검증 | 섹터별 수익률 차이가 통계적으로 유의미한지 |

---

## 10. 파이썬 실습 — 기초 통계 + 금융 데이터 확인

```python
import numpy as np
import pandas as pd
from scipy import stats

# 수익률 시뮬레이션 (GBM 기반)
rng = np.random.default_rng(42)
returns = rng.normal(0.0004, 0.012, 252)  # 일간 수익률 1년치

# 기초 통계량
print("평균(연환산):", np.mean(returns) * 252)
print("변동성(연환산):", np.std(returns, ddof=1) * np.sqrt(252))

# VaR / CVaR (95%)
var_95 = np.percentile(returns, 5)
cvar_95 = returns[returns <= var_95].mean()
print(f"VaR 95%: {var_95*100:.2f}%")
print(f"CVaR 95%: {cvar_95*100:.2f}%")

# Sharpe Ratio (무위험 수익률 연 3% 가정)
rf_daily = 0.03 / 252
excess = returns - rf_daily
sharpe = np.mean(excess) / np.std(excess, ddof=1) * np.sqrt(252)
print(f"Sharpe Ratio: {sharpe:.2f}")

# MDD 계산
cum = np.cumprod(1 + returns)
peak = np.maximum.accumulate(cum)
mdd = np.min((cum - peak) / peak)
print(f"MDD: {mdd*100:.2f}%")

# 두 자산 상관관계
asset_a = rng.normal(0.0003, 0.010, 252)
asset_b = 0.6 * asset_a + 0.4 * rng.normal(0, 0.010, 252)
corr, p_val = stats.pearsonr(asset_a, asset_b)
print(f"두 자산 상관계수: {corr:.3f}  (p={p_val:.4f})")
```

---

## 11. 자주 혼동하는 용어 비교

| 비교 쌍 | A | B | 핵심 차이 |
|---|---|---|---|
| 매출 vs 이익 | 번 총액 | 쓰고 남은 액 | 매출이 커도 비용이 더 크면 적자 |
| 영업이익 vs 순이익 | 본업 이익 | 최종 이익 | 이자·세금·일회성 반영 여부 |
| CFO vs FCF | 영업현금흐름 | 영업현금 - 설비투자 | FCF가 진짜 여유 현금 |
| PER vs PBR | 이익 대비 주가 | 순자산 대비 주가 | 성장주는 PER, 가치주는 PBR 우선 |
| VaR vs CVaR | 최대 손실 기준 | VaR 초과 시 평균 손실 | CVaR가 꼬리 위험을 더 잘 반영 |
| 알파 vs 베타 | 시장 초과수익 | 시장 민감도 | 알파↑·베타↓가 이상적 |
| 백테스트 vs 실전 | 과거 기반 시뮬 | 실시간 매매 | 오버피팅 주의, 슬리피지 감안 |
| 지지선 vs 저항선 | 하락 멈추는 바닥 | 상승 막히는 천장 | 돌파 시 역할 교체(저항→지지) |
| 골든크로스 vs 데드크로스 | 단기MA 상향 돌파 | 단기MA 하향 돌파 | 후행성 있어 확인 후 진입 필요 |
| DCF vs EVA | 미래 현금 할인 | 자본비용 차감 이익 | DCF는 절대가치, EVA는 부가가치 |
| PER vs EV/EBITDA | 주가 ÷ 주당이익 | 기업가치 ÷ EBITDA | EV/EBITDA는 부채 포함 기업 전체 비교에 유리 |
| Buy-Side vs Sell-Side | 투자 집행(운용사·연기금) | 분석 리포트 발행(증권사) | Sell-Side 리포트를 Buy-Side가 참고해 투자 결정 |
| 기본적 분석 vs 기술적 분석 | 내재가치·재무 중심 | 차트·지표·타이밍 중심 | 좋은 기업(FA) + 좋은 타이밍(TA) = 통합 리포트 |
| RSI vs MACD | 과매수·과매도 강도 | 추세 전환 시그널 | RSI는 현재 상태, MACD는 방향 전환 포착에 강함 |
| LSTM vs Transformer | 시퀀셜 순서 기억 RNN계열 | 어텐션 기반 병렬 처리 | Transformer가 장거리 의존성·속도 면에서 유리 |
| 훈련 vs 백테스트 | ML 모델 학습용 과거 데이터 | 전략 검증용 과거 데이터 | 오버피팅 방지 위해 훈련/백테스트 기간 분리 필수 |
| REST API vs WebSocket | 요청-응답 단방향 | 서버-클라이언트 실시간 양방향 | 주가 조회는 REST, 실시간 스트리밍은 WebSocket |
