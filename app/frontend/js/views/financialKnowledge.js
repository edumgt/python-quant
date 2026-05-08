import { api } from '../api.js';

const pct = (v, digits = 1) => `${(Number(v) * 100).toFixed(digits)}%`;

export function financialKnowledgeView(container) {
  container.innerHTML = `
    <div style="margin-bottom:22px;">
      <h1 style="font-size:1.25rem; font-weight:760; color:#131722; margin:0 0 6px;">
        <i class="fa-solid fa-layer-group"></i> 퀀트를 위한 금융 필수 지식
      </h1>
      <p style="font-size:0.86rem; color:#64748b; line-height:1.65; margin:0;">
        37~40.md의 5일 커리큘럼이 웹앱에 반영되어 있는지 점검하고, 금융상품 이해와 자산배분방법론을 한 화면에서 실습합니다.
      </p>
    </div>

    <section style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin-bottom:18px;">
      ${[
        ['Day 052', '주식/ETF', '개요 · 운용 전략 · 성과 비교', 'fa-chart-line'],
        ['Day 053', '채권', '개요 · 듀레이션 · 수익률 곡선', 'fa-building-columns'],
        ['Day 054', '파생상품', '선물 · 옵션 · 스왑 · 헤징', 'fa-code-branch'],
        ['Day 055', '포트폴리오 이론', '성과분석 · MDD · Sharpe', 'fa-briefcase'],
        ['Day 056', '자산배분 모델', '평균분산 · 블랙리터만 · Risk-Parity', 'fa-diagram-project'],
      ].map(([day, title, desc, icon]) => `
        <div style="border:1px solid #d9e1ec; border-radius:8px; padding:14px; background:#fff; min-height:112px;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <div style="width:34px; height:34px; display:grid; place-items:center; border-radius:8px; background:#eef4ff; color:#2962ff;">
              <i class="fa-solid ${icon}"></i>
            </div>
            <div>
              <div style="font-size:0.72rem; color:#64748b; font-weight:700;">${day}</div>
              <div style="font-size:0.92rem; color:#131722; font-weight:760;">${title}</div>
            </div>
          </div>
          <div style="font-size:0.77rem; color:#64748b; line-height:1.45;">${desc}</div>
        </div>
      `).join('')}
    </section>

    <div style="border:1px solid #d9e1ec; border-radius:8px; padding:18px; background:#fff;">
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin-bottom:16px;">
        <div>
          <label class="param-label">점검 초점</label>
          <select id="fk-focus" class="param-input">
            <option value="balanced">전체 균형</option>
            <option value="products">금융상품 이해</option>
            <option value="allocation">자산배분방법론</option>
          </select>
        </div>
        <div>
          <label class="param-label">시뮬레이션 수</label>
          <input id="fk-sims" type="number" value="3000" min="500" max="10000" class="param-input"/>
        </div>
        <div>
          <label class="param-label">무위험 수익률</label>
          <input id="fk-rf" type="number" value="0.03" min="0" max="0.1" step="0.005" class="param-input"/>
        </div>
      </div>

      <button class="run-btn" id="fk-run">
        <i class="fa-solid fa-play"></i> 반영 상태 점검
      </button>
      <div id="fk-result" style="margin-top:18px;"></div>
    </div>
  `;

  container.querySelector('#fk-run').addEventListener('click', async () => {
    const btn = container.querySelector('#fk-run');
    const result = container.querySelector('#fk-result');
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 점검 중...';
    result.innerHTML = '<p style="color:#64748b; font-size:0.86rem;">커리큘럼-웹앱 매핑과 자산배분 예시를 계산하고 있습니다.</p>';

    try {
      const data = await api.financialKnowledge({
        focus: container.querySelector('#fk-focus').value,
        n_simulations: +container.querySelector('#fk-sims').value,
        risk_free: +container.querySelector('#fk-rf').value,
      });

      result.innerHTML = `
        ${renderDiagnostics(data.diagnostics)}
        ${data.image ? `<img src="${data.image}" style="width:100%; border-radius:8px; border:1px solid #d9e1ec; margin:14px 0 10px; background:#0f172a;"/>` : ''}
        ${renderChartExplanation()}
        ${renderCoverage(data.coverage)}
        ${renderStrategies(data.strategies)}
        ${renderCurriculum(data.curriculum)}
      `;
    } catch (e) {
      result.innerHTML = `<p style="color:#ef4444;">오류: ${e.message}</p>`;
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-play"></i> 반영 상태 점검';
    }
  });
}

function renderDiagnostics(rows = []) {
  const statusColor = (s) => s === '부분 반영' ? '#d97706' : s === '충분' ? '#2962ff' : '#089981';
  const explanations = [
    ['📋 커리큘럼 충분', '37~40.md 4개 문서가 Day 052~056을 모두 다룹니다. 주식/ETF·채권·파생상품·포트폴리오·자산배분까지 5개 주제가 빠짐없이 문서화되어 있습니다.', '#2962ff'],
    ['⚠️ 부분 반영이란?', '문서 내용은 있지만 웹앱 화면이 없거나 일부만 구현된 상태입니다. 예: 금융상품별 통합 비교 화면 부재.', '#d97706'],
    ['✅ 반영 완료란?', '문서의 핵심 내용이 이 화면에 실습 형태로 구현된 상태입니다. 이론뿐 아니라 파라미터를 바꿔 직접 결과를 확인할 수 있습니다.', '#089981'],
  ];
  return `
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin-bottom:10px;">
      ${rows.map((row) => `
        <div style="border:1px solid #d9e1ec; border-radius:8px; padding:14px; background:#f8fafc;">
          <div style="font-size:0.75rem; color:#64748b; font-weight:700; margin-bottom:4px;">${row.area}</div>
          <div style="font-size:1rem; color:${statusColor(row.status)}; font-weight:800; margin-bottom:6px;">${row.status}</div>
          <div style="font-size:0.78rem; color:#475569; line-height:1.5;">${row.note}</div>
        </div>
      `).join('')}
    </div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; margin-bottom:18px;">
      ${explanations.map(([title, desc, col]) => `
        <div style="border-top:3px solid ${col}; border-radius:8px; padding:13px; background:#f8fafc; border:1px solid #e5edf5; border-top:3px solid ${col};">
          <div style="font-size:0.82rem; font-weight:700; color:#0f172a; margin-bottom:5px;">${title}</div>
          <div style="font-size:0.76rem; color:#64748b; line-height:1.55;">${desc}</div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderChartExplanation() {
  const charts = [
    ['📈 자산군별 누적 성과 (좌상)', '주식/ETF → 원자재 → 채권 → 현금 순으로 기대수익률이 높지만 변동성도 함께 큽니다. 선이 크게 흔들릴수록 리스크가 높은 자산입니다.', '#3b82f6'],
    ['🎯 효율적 투자선 (우상)', '산포도에서 <strong>왼쪽 위</strong>에 있을수록 같은 리스크에 수익이 높습니다. ★ = 평균분산 최적점(Sharpe 최대), ◆ = Risk-Parity 위치.', '#a855f7'],
    ['📊 모델별 비중 비교 (좌하)', '4가지 모델이 같은 자산군에 얼마나 다른 비중을 배분하는지 보여줍니다. 60/40은 주식 쏠림, Risk-Parity는 채권 비중이 높습니다.', '#22c55e'],
    ['💹 파생상품 + 채권 곡선 (우하)', '콜·풋·스트래들의 손익 구조와 현재 금리 환경(수익률 곡선)을 동시에 확인합니다. 우상향 곡선은 장기 프리미엄이 있는 정상 환경입니다.', '#f59e0b'],
  ];
  return `
    <div style="margin-bottom:18px;">
      <div style="font-size:0.78rem; color:#64748b; font-weight:700; margin-bottom:8px; letter-spacing:0.03em;">차트 읽는 법</div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px;">
        ${charts.map(([title, desc, col]) => `
          <div style="border-top:3px solid ${col}; background:#f8fafc; border-radius:8px; padding:13px; border:1px solid #e5edf5; border-top:3px solid ${col};">
            <div style="font-size:0.82rem; font-weight:700; color:#0f172a; margin-bottom:5px;">${title}</div>
            <div style="font-size:0.76rem; color:#64748b; line-height:1.55;">${desc}</div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function renderCoverage(rows = []) {
  const colGuide = [
    ['반영률', '문서 내용 중 웹앱에 구현된 비율. 80% 이상이면 핵심 내용이 대부분 반영된 것입니다.', '#089981'],
    ['웹앱 상태', '"보완됨" = 신규 추가, "기존+보완" = 기존 화면에 내용 추가, "구현 예정" = 미반영.', '#2962ff'],
    ['핵심 항목', '해당 Day에서 반드시 이해해야 할 개념 목록입니다. 모르는 항목은 문서를 먼저 읽으세요.', '#a855f7'],
  ];
  return `
    <section style="margin-bottom:18px;">
      <h2 style="font-size:1rem; color:#131722; margin:0 0 8px;">문서-웹앱 반영 점검</h2>
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:8px; margin-bottom:12px;">
        ${colGuide.map(([col, desc, color]) => `
          <div style="border-left:3px solid ${color}; background:#f8fafc; border-radius:6px; padding:10px 12px;">
            <div style="font-size:0.75rem; font-weight:700; color:${color}; margin-bottom:3px;">${col}</div>
            <div style="font-size:0.74rem; color:#64748b; line-height:1.5;">${desc}</div>
          </div>
        `).join('')}
      </div>
      <div style="overflow:auto; border:1px solid #d9e1ec; border-radius:8px;">
        <table style="width:100%; border-collapse:collapse; font-size:0.82rem; min-width:760px;">
          <thead>
            <tr style="background:#f1f5f9;">
              <th style="padding:10px; text-align:left; color:#475569;">일차</th>
              <th style="padding:10px; text-align:left; color:#475569;">주제</th>
              <th style="padding:10px; text-align:left; color:#475569;">문서</th>
              <th style="padding:10px; text-align:left; color:#475569;">반영률</th>
              <th style="padding:10px; text-align:left; color:#475569;">웹앱 상태</th>
              <th style="padding:10px; text-align:left; color:#475569;">핵심 항목</th>
            </tr>
          </thead>
          <tbody>
            ${rows.map(row => `
              <tr style="border-top:1px solid #e5edf5;">
                <td style="padding:10px; color:#131722; font-weight:700;">${row.day}</td>
                <td style="padding:10px; color:#131722;">${row.topic}</td>
                <td style="padding:10px; color:#64748b;">${row.document}</td>
                <td style="padding:10px; color:#089981; font-weight:800;">${pct(row.coverage, 0)}</td>
                <td style="padding:10px; color:#2962ff; font-weight:700;">${row.web_status}</td>
                <td style="padding:10px; color:#475569;">${row.items.join(' · ')}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </section>
  `;
}

function renderStrategies(strategies = {}) {
  return `
    <section style="margin-bottom:18px;">
      <h2 style="font-size:1rem; color:#131722; margin:0 0 10px;">자산배분 모델 비교</h2>
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px;">
        ${Object.entries(strategies).map(([name, info]) => `
          <div style="border:1px solid #d9e1ec; border-radius:8px; padding:14px; background:#fff;">
            <div style="font-size:0.92rem; color:#131722; font-weight:800; margin-bottom:10px;">${name}</div>
            <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-bottom:12px;">
              ${Object.entries(info.metrics || {}).map(([k, v]) => `
                <div style="background:#f8fafc; border:1px solid #e5edf5; border-radius:6px; padding:8px;">
                  <div style="font-size:0.68rem; color:#64748b; text-transform:uppercase;">${k}</div>
                  <div style="font-size:0.88rem; color:#131722; font-weight:800;">${formatMetric(k, v)}</div>
                </div>
              `).join('')}
            </div>
            <div style="display:grid; gap:6px;">
              ${Object.entries(info.weights || {}).map(([asset, weight]) => `
                <div>
                  <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#475569; margin-bottom:3px;">
                    <span>${asset}</span><strong>${pct(weight, 1)}</strong>
                  </div>
                  <div style="height:6px; border-radius:99px; background:#e5edf5; overflow:hidden;">
                    <div style="height:100%; width:${Math.max(2, Number(weight) * 100)}%; background:#2962ff;"></div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    </section>
  `;
}

function renderCurriculum(rows = []) {
  return `
    <section>
      <h2 style="font-size:1rem; color:#131722; margin:0 0 10px;">5일 커리큘럼 운영안</h2>
      <div style="display:grid; gap:8px;">
        ${rows.map(row => `
          <div style="display:grid; grid-template-columns:90px 1fr 1.2fr; gap:12px; align-items:center; border:1px solid #d9e1ec; border-radius:8px; padding:10px; background:#fff;">
            <strong style="color:#2962ff; font-size:0.82rem;">${row.day}</strong>
            <span style="color:#131722; font-size:0.86rem; font-weight:760;">${row.title}</span>
            <span style="color:#64748b; font-size:0.78rem;">${row.practice}</span>
          </div>
        `).join('')}
      </div>
    </section>
  `;
}

function formatMetric(key, value) {
  if (['cagr', 'volatility', 'mdd'].includes(key)) return pct(value, 1);
  return Number(value).toFixed(2);
}
