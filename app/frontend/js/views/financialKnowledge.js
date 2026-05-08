const BASE_MONEY = 1000000;
const MIN_GROWTH_MULTIPLIER = 0.7;
const MIN_BAR_WIDTH_PERCENT = 2;

const STYLE_PRESETS = {
  safe: {
    name: '안정형',
    description: '손실을 줄이는 것을 가장 중요하게 생각해요.',
    weights: { '주식/ETF': 0.2, '채권': 0.55, '원자재': 0.1, '현금': 0.15 },
    checks: ['원금 손실이 걱정돼요', '수익이 조금 낮아도 괜찮아요', '큰 변동은 피하고 싶어요'],
  },
  balanced: {
    name: '균형형',
    description: '안정성과 수익을 함께 챙기고 싶어요.',
    weights: { '주식/ETF': 0.4, '채권': 0.35, '원자재': 0.15, '현금': 0.1 },
    checks: ['적당한 변동은 감수할 수 있어요', '예금보다 높은 수익을 원해요', '장기적으로 키우고 싶어요'],
  },
  growth: {
    name: '성장형',
    description: '변동이 있더라도 더 큰 수익을 기대해요.',
    weights: { '주식/ETF': 0.6, '채권': 0.2, '원자재': 0.15, '현금': 0.05 },
    checks: ['단기 하락을 버틸 수 있어요', '장기 수익을 더 중요하게 봐요', '공격적으로 투자해도 괜찮아요'],
  },
};

const ASSET_RETURN = { '주식/ETF': 0.09, '채권': 0.035, '원자재': 0.055, '현금': 0.02 };
const ASSET_RISK = { '주식/ETF': 0.2, '채권': 0.07, '원자재': 0.17, '현금': 0.01 };
const SCENARIO_ADJUST = { slow: -0.03, normal: 0, fast: 0.03 };

export function financialKnowledgeView(container) {
  container.innerHTML = `
    <div style="margin-bottom:18px;">
      <h1 style="font-size:1.18rem; font-weight:760; color:#131722; margin:0 0 6px;">
        <i class="fa-solid fa-layer-group"></i> 쉬운 자산배분 체험
      </h1>
      <p style="font-size:0.9rem; color:#475569; line-height:1.6; margin:0;">
        금융 지식이 적어도 괜찮아요. <strong>100만원</strong>을 투자 성향에 맞게 나누고, 결과를 간단히 확인해요.
      </p>
    </div>

    <section style="border:1px solid #d9e1ec; border-radius:8px; padding:16px; background:#fff;">
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin-bottom:12px;">
        <div>
          <label class="param-label">투자 금액 (원)</label>
          <input id="fk-money" type="number" class="param-input" min="100000" step="10000" value="${BASE_MONEY}" />
        </div>
        <div>
          <label class="param-label">투자 방식 체크</label>
          <select id="fk-style" class="param-input">
            <option value="safe">안정형</option>
            <option value="balanced" selected>균형형</option>
            <option value="growth">성장형</option>
          </select>
        </div>
        <div>
          <label class="param-label">시뮬레이션 기간</label>
          <select id="fk-years" class="param-input">
            <option value="1">1년</option>
            <option value="3" selected>3년</option>
            <option value="5">5년</option>
          </select>
        </div>
        <div>
          <label class="param-label">시장 분위기</label>
          <select id="fk-scenario" class="param-input">
            <option value="slow">보수적</option>
            <option value="normal" selected>보통</option>
            <option value="fast">긍정적</option>
          </select>
        </div>
      </div>

      <button class="run-btn" id="fk-run">
        <i class="fa-solid fa-play"></i> 시뮬레이션 보기
      </button>

      <div id="fk-result" style="margin-top:16px;"></div>
    </section>
  `;

  const render = () => {
    const money = Math.max(100000, Number(container.querySelector('#fk-money').value) || BASE_MONEY);
    const years = Math.max(1, Number(container.querySelector('#fk-years').value) || 1);
    const style = container.querySelector('#fk-style').value;
    const scenario = container.querySelector('#fk-scenario').value;
    const preset = STYLE_PRESETS[style] || STYLE_PRESETS.balanced;
    const expected = calcExpectedReturn(preset.weights) + (SCENARIO_ADJUST[scenario] || 0);
    const risk = calcRisk(preset.weights);
    const growthMultiplier = getGrowthMultiplier(expected);
    const futureMoney = money * (growthMultiplier ** years);

    container.querySelector('#fk-result').innerHTML = `
      ${renderSummary(preset, money, years, expected, risk, futureMoney)}
      ${renderAllocations(preset.weights, money, growthMultiplier, years)}
    `;
  };

  container.querySelector('#fk-run').addEventListener('click', render);
  render();
}

function renderSummary(preset, money, years, expected, risk, futureMoney) {
  return `
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:10px; margin-bottom:12px;">
      ${[
        ['선택 성향', `${preset.name}`, '#2962ff'],
        ['현재 금액', `${formatWon(money)}`, '#089981'],
        ['예상 연수익률', `${toPct(expected)}`, '#2962ff'],
        ['예상 변동성', `${toPct(risk)}`, '#d97706'],
        [`${years}년 후 예상`, `${formatWon(futureMoney)}`, '#7c3aed'],
      ].map(([label, value, color]) => `
        <div style="background:#f8fafc; border:1px solid #e5edf5; border-left:3px solid ${color}; border-radius:8px; padding:10px;">
          <div style="font-size:0.74rem; color:#64748b; margin-bottom:4px;">${label}</div>
          <div style="font-size:0.95rem; color:#131722; font-weight:800;">${value}</div>
        </div>
      `).join('')}
    </div>
    <div style="border:1px solid #d9e1ec; border-radius:8px; padding:10px 12px; background:#fff; margin-bottom:12px;">
      <div style="font-size:0.85rem; color:#131722; font-weight:700; margin-bottom:6px;">${preset.description}</div>
      <div style="display:grid; gap:4px;">
        ${preset.checks.map((text) => `
          <div style="font-size:0.8rem; color:#475569;">☑ ${text}</div>
        `).join('')}
      </div>
    </div>
  `;
}

function renderAllocations(weights, money, growthMultiplier, years) {
  return `
    <section style="border:1px solid #d9e1ec; border-radius:8px; padding:12px; background:#fff;">
      <h2 style="font-size:0.95rem; color:#131722; margin:0 0 8px;">${formatWon(money)} 자산배분 결과</h2>
      <div style="display:grid; gap:8px;">
        ${Object.entries(weights).map(([asset, weight]) => {
          const nowMoney = money * weight;
          const futureMoney = nowMoney * (growthMultiplier ** years);
          return `
            <div style="border:1px solid #e5edf5; border-radius:8px; padding:10px; background:#f8fafc;">
              <div style="display:flex; justify-content:space-between; gap:8px; font-size:0.8rem; margin-bottom:4px;">
                <strong style="color:#131722;">${asset}</strong>
                <span style="color:#475569;">${toPct(weight)} · ${formatWon(nowMoney)}</span>
              </div>
              <div style="height:6px; border-radius:99px; background:#e5edf5; overflow:hidden; margin-bottom:6px;">
                <div style="height:100%; width:${Math.max(MIN_BAR_WIDTH_PERCENT, weight * 100)}%; background:#2962ff;"></div>
              </div>
              <div style="font-size:0.76rem; color:#64748b;">${years}년 후 예상: ${formatWon(futureMoney)}</div>
            </div>
          `;
        }).join('')}
      </div>
      <p style="font-size:0.74rem; color:#64748b; margin:10px 0 0;">
        ※ 학습용 단순 시뮬레이션입니다. 실제 수익은 달라질 수 있어요.
      </p>
    </section>
  `;
}

function calcExpectedReturn(weights) {
  return Object.entries(weights).reduce((acc, [asset, weight]) => acc + (ASSET_RETURN[asset] || 0) * weight, 0);
}

function calcRisk(weights) {
  return Object.entries(weights).reduce((acc, [asset, weight]) => acc + (ASSET_RISK[asset] || 0) * weight, 0);
}

function getGrowthMultiplier(expected) {
  return Math.max(MIN_GROWTH_MULTIPLIER, 1 + expected);
}

function formatWon(value) {
  return `${Math.round(value).toLocaleString('ko-KR')}원`;
}

function toPct(value) {
  return `${(Number(value) * 100).toFixed(1)}%`;
}
