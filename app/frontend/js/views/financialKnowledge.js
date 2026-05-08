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
        ${data.image ? `<img src="${data.image}" style="width:100%; border-radius:8px; border:1px solid #d9e1ec; margin:14px 0 18px; background:#0f172a;"/>` : ''}
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
  return `
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; margin-bottom:14px;">
      ${rows.map((row) => `
        <div style="border:1px solid #d9e1ec; border-radius:8px; padding:14px; background:#f8fafc;">
          <div style="font-size:0.75rem; color:#64748b; font-weight:700; margin-bottom:4px;">${row.area}</div>
          <div style="font-size:1rem; color:${row.status === '부분 반영' ? '#d97706' : '#089981'}; font-weight:800; margin-bottom:6px;">${row.status}</div>
          <div style="font-size:0.78rem; color:#475569; line-height:1.5;">${row.note}</div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderCoverage(rows = []) {
  return `
    <section style="margin-bottom:18px;">
      <h2 style="font-size:1rem; color:#131722; margin:0 0 10px;">문서-웹앱 반영 점검</h2>
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
