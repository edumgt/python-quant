export function homeView(container, navigate) {
  const groups = [
    {
      title: '매크로 분석',
      desc: '금리, 물가, 유가, 환율, 주가지수 같은 거시 지표의 흐름을 확인합니다.',
      icon: 'fa-solid fa-globe',
      items: [
        { icon: 'fa-solid fa-satellite-dish', name: '거시경제현황 1 (실시간)', tag: 'yfinance · 추세/상관관계', view: 'macro-realtime' },
        { icon: 'fa-solid fa-chart-area', name: '거시경제현황 2 (시뮬레이션)', tag: 'GBM · 경기국면', view: 'macro-simulation' },
      ],
    },
    {
      title: '산업적 분석',
      desc: '산업 경쟁력, KPI, Peer Comparison, PEST, SWOT으로 업종 매력도를 분석합니다.',
      icon: 'fa-solid fa-industry',
      items: [
        { icon: 'fa-solid fa-industry', name: '산업 경쟁력 분석', tag: 'Porter · KPI · PEST · SWOT', view: 'industry-analysis' },
      ],
    },
    {
      title: '기본적 분석',
      desc: '기업의 실적, 재무 체력, 가치평가 관점에서 투자 대상을 검토합니다.',
      icon: 'fa-solid fa-file-invoice-dollar',
      items: [
        { icon: 'fa-solid fa-magnifying-glass-chart', name: 'DART 상장기업 검색', tag: '회사명 → 종목코드 · DART 고유번호', view: 'dart-company-search' },
        { icon: 'fa-solid fa-scale-balanced', name: '재무제표분석', tag: '손익계산서 · 재무상태표 · 현금흐름표', view: 'financial-statement' },
        { icon: 'fa-solid fa-briefcase', name: '포트폴리오 최적화', tag: '자본 배분 · 샤프 비율', view: 'portfolio' },
        { icon: 'fa-solid fa-shield-halved', name: '리스크 분석 (VaR)', tag: '손실 위험 · 자본 보전', view: 'risk' },
        { icon: 'fa-solid fa-calculator', name: '밸류에이션 실습', tag: 'FCF · DCF · EVA · 기업선정', view: 'valuation' },
      ],
    },
    {
      title: '퀀트를 위한 금융 필수 지식',
      desc: '주식/ETF, 채권, 파생상품과 포트폴리오 이론, 자산배분 모델을 5일 과정으로 점검합니다.',
      icon: 'fa-solid fa-layer-group',
      items: [
        { icon: 'fa-solid fa-layer-group', name: '금융상품·자산배분', tag: '37~41.md · 5일 커리큘럼', view: 'financial-knowledge' },
        { icon: 'fa-solid fa-briefcase', name: '자산배분 최적화', tag: '평균분산 · Risk-Parity', view: 'portfolio' },
        { icon: 'fa-solid fa-shield-halved', name: '리스크 지표 실습', tag: 'VaR · CVaR · 손실위험', view: 'risk' },
      ],
    },
    {
      title: '기술적 분석',
      desc: '가격, 추세, 지표, 백테스트를 통해 매매 전략의 동작을 검증합니다.',
      icon: 'fa-solid fa-chart-line',
      items: [
        { icon: 'fa-solid fa-chart-candlestick', name: '기술적 분석 실습', tag: '추세·MA·캔들·지표·파동', view: 'technical-chart' },
        { icon: 'fa-solid fa-clock-rotate-left', name: '백테스트 엔진', tag: 'MA 크로스오버 · 성과 분석', view: 'backtest' },
        { icon: 'fa-solid fa-diagram-project', name: '퀀트 파이프라인', tag: 'MA · RSI · MACD · ML', view: 'pipeline' },
      ],
    },
  ];

  container.innerHTML = `
    <div style="margin-bottom:28px;">
      <h1 style="font-size:1.5rem; font-weight:700; color:#131722; margin-bottom:8px;">Python Quant Lab</h1>
      <p style="font-size:0.875rem; color:#6b7280; line-height:1.6;">
        투자분석 기초 방법론을 매크로 분석, 산업적 분석, 기본적 분석, 기술적 분석 4개 흐름으로 구성했습니다.
        우측 메뉴 또는 아래 분류 카드에서 실습을 선택하세요.
      </p>
    </div>

    <div class="analysis-group-grid" id="home-grid">
      ${groups.map(group => `
        <section class="analysis-group">
          <div class="analysis-group-head">
            <div class="analysis-group-icon"><i class="${group.icon}"></i></div>
            <div>
              <h2>${group.title}</h2>
              <p>${group.desc}</p>
            </div>
          </div>
          <div class="home-grid">
            ${group.items.map(item => `
              <div class="home-card ${item.disabled ? 'is-disabled' : ''}" ${item.view ? `data-view="${item.view}"` : ''}>
                <div class="home-icon"><i class="${item.icon}"></i></div>
                <div class="home-card-title">${item.name}</div>
                <div class="home-card-tag">${item.disabled ? `${item.tag} · 준비 중` : item.tag}</div>
              </div>`).join('')}
          </div>
        </section>
      `).join('')}
    </div>
  `;

  container.querySelectorAll('#home-grid [data-view]').forEach(card => {
    card.addEventListener('click', () => navigate(card.dataset.view));
  });
}
