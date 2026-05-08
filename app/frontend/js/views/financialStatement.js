const statementCards = [
  {
    title: '손익계산서',
    icon: 'fa-solid fa-chart-column',
    sourceLabel: '손익계산서 예시 이미지 보기',
    sourceUrl: 'https://bb-investment.tistory.com/16',
    summary: '일정 기간 동안 매출이 비용을 거쳐 영업이익과 순이익으로 바뀌는 과정을 보여줍니다.',
    checks: [
      ['매출액', '전년 또는 전분기 대비 성장률을 먼저 확인합니다.'],
      ['매출원가율', '매출이 늘어도 원가율이 같이 뛰면 수익성 개선이 제한됩니다.'],
      ['판관비', '고정비 성격이 강해 매출 증가 시 영업 레버리지 효과를 만듭니다.'],
      ['영업이익', '본업의 경쟁력과 비용 통제력을 보는 핵심 항목입니다.'],
      ['당기순이익', '금융손익, 법인세, 일회성 손익까지 반영된 최종 성과입니다.'],
    ],
    analysis: [
      '예시 이미지는 매출액, 매출원가, 판관비, 영업이익, 당기순이익의 흐름을 따라 읽기 좋습니다.',
      '매출 증가와 동시에 원가·판관비가 안정적이면 영업이익률 개선 가능성이 큽니다.',
      '영업이익은 흑자인데 순이익이 약하면 금융비용, 법인세, 일회성 손실을 추가 확인해야 합니다.',
    ],
  },
  {
    title: '대차대조표 / 재무상태표',
    icon: 'fa-solid fa-scale-balanced',
    sourceLabel: '재무상태표 예시 이미지 보기',
    sourceUrl: 'https://yackong.tistory.com/4',
    summary: '특정 시점의 자산, 부채, 자본 구조를 보여주며 회사의 재무 안정성을 판단합니다.',
    checks: [
      ['자산', '유동자산과 비유동자산 구성을 나눠 현금화 가능성을 봅니다.'],
      ['부채', '유동부채 비중이 높으면 단기 상환 압박이 커질 수 있습니다.'],
      ['자본', '자본총계가 두껍고 이익잉여금이 누적되면 완충력이 큽니다.'],
      ['유동비율', '유동자산 / 유동부채로 단기 지급능력을 봅니다.'],
      ['부채비율', '부채총계 / 자본총계로 레버리지 부담을 봅니다.'],
    ],
    analysis: [
      '예시 이미지는 자산 = 부채 + 자본 구조를 한눈에 확인하는 데 적합합니다.',
      '유동자산이 유동부채보다 충분히 크면 단기 유동성 위험이 낮아집니다.',
      '부채가 빠르게 늘면서 자본 증가가 따라오지 못하면 이자비용과 증자 가능성을 점검해야 합니다.',
    ],
  },
  {
    title: '현금흐름표',
    icon: 'fa-solid fa-money-bill-transfer',
    sourceLabel: '현금흐름표 예시 이미지 보기',
    sourceUrl: 'https://buyandpray.tistory.com/42',
    summary: '회계상 이익이 실제 현금으로 전환되는지 영업·투자·재무 현금흐름으로 확인합니다.',
    checks: [
      ['영업활동 현금흐름', '본업에서 현금이 들어오는지 보는 가장 중요한 항목입니다.'],
      ['투자활동 현금흐름', '설비투자, 금융상품, 자산 매각 여부를 확인합니다.'],
      ['재무활동 현금흐름', '차입, 상환, 배당, 증자 등 자금조달 흐름을 봅니다.'],
      ['순이익 대비 CFO', '순이익보다 영업현금흐름이 계속 약하면 이익의 질을 의심합니다.'],
      ['FCF', '영업현금흐름에서 설비투자를 뺀 잉여현금 창출력을 봅니다.'],
    ],
    analysis: [
      '예시 이미지는 영업·투자·재무 현금흐름을 나눠 읽는 연습에 좋습니다.',
      '좋은 기업은 대체로 영업현금흐름이 플러스이고, 성장기에는 투자현금흐름이 마이너스일 수 있습니다.',
      '순이익은 흑자인데 영업현금흐름이 반복적으로 마이너스라면 매출채권, 재고, 회계상 이익의 질을 확인해야 합니다.',
    ],
  },
];

export function financialStatementView(container) {
  container.innerHTML = `
    <div style="margin-bottom:28px;">
      <h1 style="font-size:1.45rem; font-weight:760; color:#131722; margin-bottom:8px;">
        <i class="fa-solid fa-file-invoice-dollar"></i> 재무제표분석
      </h1>
      <p style="font-size:0.88rem; color:#6b7280; line-height:1.65;">
        손익계산서, 대차대조표(재무상태표), 현금흐름표를 각각 따로 보지 않고 서로 연결해서 읽는 기본적 분석 화면입니다.
      </p>
    </div>

    <div class="statement-grid">
      ${statementCards.map(card => `
        <article class="statement-card">
          <div class="statement-head">
            <div class="statement-icon"><i class="${card.icon}"></i></div>
            <div>
              <h2>${card.title}</h2>
              <p>${card.summary}</p>
            </div>
          </div>
          <a class="statement-link" href="${card.sourceUrl}" target="_blank" rel="noopener noreferrer">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> ${card.sourceLabel}
          </a>
          <div class="statement-table">
            ${card.checks.map(([label, desc]) => `
              <div class="statement-row">
                <strong>${label}</strong>
                <span>${desc}</span>
              </div>`).join('')}
          </div>
          <div class="statement-analysis">
            <div class="statement-analysis-title">예시 이미지 분석</div>
            ${card.analysis.map(text => `<p>${text}</p>`).join('')}
          </div>
        </article>
      `).join('')}
    </div>

    <section class="statement-flow">
      <h2>세 표를 연결해서 읽는 순서</h2>
      <div class="statement-flow-grid">
        <div><b>1. 손익계산서</b><span>매출 성장과 영업이익률로 본업의 힘을 확인합니다.</span></div>
        <div><b>2. 재무상태표</b><span>그 성장이 부채 부담을 키우며 만들어진 것인지 확인합니다.</span></div>
        <div><b>3. 현금흐름표</b><span>이익이 실제 현금으로 들어오고 있는지 최종 검증합니다.</span></div>
      </div>
    </section>
  `;
}
