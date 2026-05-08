import { api } from '../api.js';

// ── 탭 공통 유틸 ─────────────────────────────────────────────────────────────
function tabShell(tabs) {
  return `
    <div style="margin-bottom:24px;">
      <h1 style="font-size:1.25rem; font-weight:700; color:#fff; margin-bottom:6px;">🏭 산업 경쟁력 분석</h1>
      <p style="font-size:0.875rem; color:#94a3b8; line-height:1.6;">
        Porter 5 Forces · 섹터 ETF 비교 · 산업 생애주기 · SWOT Matrix 4가지 프레임워크로 산업 경쟁력을 분석합니다.
      </p>
    </div>
    <div style="display:flex; gap:4px; margin-bottom:20px; border-bottom:1px solid #334155; padding-bottom:0;">
      ${tabs.map((t, i) => `
        <button class="ia-tab" data-tab="${i}"
          style="padding:9px 18px; border:none; border-radius:8px 8px 0 0; cursor:pointer;
                 font-size:0.825rem; font-weight:600; transition:all 0.15s;
                 background:${i===0?'#2563eb':'#1e293b'};
                 color:${i===0?'#fff':'#94a3b8'};">
          ${t}
        </button>`).join('')}
    </div>
    <div id="ia-content"></div>`;
}

function activateTab(container, idx, renders) {
  container.querySelectorAll('.ia-tab').forEach((btn, i) => {
    btn.style.background = i === idx ? '#2563eb' : '#1e293b';
    btn.style.color      = i === idx ? '#fff'    : '#94a3b8';
  });
  renders[idx](container.querySelector('#ia-content'));
}

// ── 메인 진입점 ──────────────────────────────────────────────────────────────
export function industryAnalysisView(container) {
  const TABS = ['① Porter 5 Forces', '② 섹터 주가 비교', '③ 산업 생애주기', '④ SWOT Matrix'];
  container.innerHTML = tabShell(TABS);

  const renders = [renderPorter, renderSector, renderLifecycle, renderSwot];

  container.querySelectorAll('.ia-tab').forEach((btn, i) => {
    btn.addEventListener('click', () => activateTab(container, i, renders));
  });

  // 기본: 첫 탭
  renders[0](container.querySelector('#ia-content'));
}


// ── Tab 1: Porter 5 Forces ───────────────────────────────────────────────────
const FORCES = ['경쟁강도', '신규진입 위협', '대체재 위협', '구매자 교섭력', '공급자 교섭력'];

function renderPorter(el) {
  el.innerHTML = `
    <div style="background:#1e293b; border-radius:12px; padding:24px; border:1px solid #334155;">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px;">
        <div>
          <label class="param-label">분석 산업명</label>
          <input id="porter-ind" type="text" value="반도체" class="param-input"/>
        </div>
      </div>
      <div style="margin-bottom:20px;">
        <div style="font-size:0.75rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">위협 강도 조절 (0 = 낮음 / 10 = 높음)</div>
        <div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:12px;" id="porter-sliders">
          ${FORCES.map((f, i) => `
            <div style="background:#0f172a; border-radius:8px; padding:12px 16px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="font-size:0.825rem; color:#e2e8f0;">${f}</span>
                <span id="porter-val-${i}" style="font-size:0.875rem; font-weight:700; color:#3b82f6;">
                  ${[8,6,4,5,7][i]}.0
                </span>
              </div>
              <input type="range" id="porter-sl-${i}" min="0" max="10" step="0.5"
                     value="${[8,6,4,5,7][i]}"
                     style="width:100%; accent-color:#3b82f6;"
                     oninput="document.getElementById('porter-val-${i}').textContent=parseFloat(this.value).toFixed(1)"/>
            </div>`).join('')}
        </div>
      </div>
      <button class="run-btn" id="porter-run">▶ 분석 실행</button>
      <div id="porter-result" style="margin-top:20px;"></div>
    </div>`;

  el.querySelector('#porter-run').addEventListener('click', async () => {
    const btn    = el.querySelector('#porter-run');
    const result = el.querySelector('#porter-result');
    const industry = el.querySelector('#porter-ind').value.trim() || '반도체';
    const scores = {};
    FORCES.forEach((f, i) => {
      scores[f] = parseFloat(el.querySelector(`#porter-sl-${i}`).value);
    });

    btn.disabled = true; btn.textContent = '분석 중...';
    result.innerHTML = '<p style="color:#94a3b8;">Porter 5 Forces 분석 중...</p>';
    try {
      const data = await api.industryPorter({ industry, scores });
      let html = '';
      if (data.image) html += `<img src="${data.image}" style="width:100%; border-radius:8px; margin-bottom:16px;"/>`;
      if (data.forces) {
        const gradeColor = { '강함': '#ef4444', '보통': '#f59e0b', '약함': '#22c55e' };
        html += `<div style="display:flex; flex-wrap:wrap; gap:10px;">
          ${Object.entries(data.forces).map(([f, v]) => `
            <div class="metric-box" style="min-width:130px;">
              <div style="font-size:0.7rem; color:#64748b; margin-bottom:4px;">${f}</div>
              <div style="font-size:1rem; font-weight:700; color:${gradeColor[v.level]};">
                ${v.score.toFixed(1)} — ${v.level}
              </div>
            </div>`).join('')}
          <div class="metric-box" style="min-width:130px; border:1px solid #3b82f6;">
            <div style="font-size:0.7rem; color:#64748b; margin-bottom:4px;">종합 위협지수</div>
            <div style="font-size:1.1rem; font-weight:700; color:#3b82f6;">
              ${data.avg_score} — ${data.grade}
            </div>
          </div>
        </div>`;
      }
      result.innerHTML = html;
    } catch(e) {
      result.innerHTML = `<p style="color:#ef4444;">오류: ${e.message}</p>`;
    } finally {
      btn.disabled = false; btn.textContent = '▶ 분석 실행';
    }
  });
}


// ── Tab 2: 섹터 주가 비교 ────────────────────────────────────────────────────
const SECTOR_OPTS = [
  { v:'SOXX', l:'반도체 (SOXX)' }, { v:'XLE', l:'에너지 (XLE)' },
  { v:'XLF', l:'금융 (XLF)' },    { v:'XLV', l:'헬스케어 (XLV)' },
  { v:'XLK', l:'기술 (XLK)' },    { v:'XLI', l:'산업재 (XLI)' },
  { v:'XLY', l:'소비재경기 (XLY)'},{ v:'XLP', l:'소비재필수 (XLP)'},
  { v:'XLB', l:'소재 (XLB)' },    { v:'XLRE',l:'부동산 (XLRE)'},
  { v:'XLU', l:'유틸리티 (XLU)' },{ v:'IBB', l:'바이오 (IBB)' },
];
const DEFAULT_SECTORS = ['SOXX','XLE','XLF','XLV','XLK','XLI'];
const PERIODS_SEC = [
  {v:'1mo',l:'1개월'},{v:'3mo',l:'3개월'},{v:'6mo',l:'6개월'},
  {v:'1y',l:'1년'},{v:'2y',l:'2년'},{v:'5y',l:'5년'},
];

function renderSector(el) {
  el.innerHTML = `
    <div style="background:#1e293b; border-radius:12px; padding:24px; border:1px solid #334155;">
      <div style="margin-bottom:16px;">
        <label class="param-label" style="margin-bottom:8px; display:block;">섹터 ETF 선택</label>
        <div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:8px;" id="sec-grid">
          ${SECTOR_OPTS.map(t => `
            <label style="display:flex; align-items:center; gap:8px; padding:8px 12px;
                   background:#0f172a; border-radius:8px; cursor:pointer;
                   border:1px solid #334155; font-size:0.8rem; color:#94a3b8;">
              <input type="checkbox" value="${t.v}" ${DEFAULT_SECTORS.includes(t.v)?'checked':''}
                     style="accent-color:#3b82f6;"/>
              ${t.l}
            </label>`).join('')}
        </div>
      </div>
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px; flex-wrap:wrap;">
        <label class="param-label" style="margin:0;">기간:</label>
        <div style="display:flex; gap:6px; flex-wrap:wrap;" id="sec-period">
          ${PERIODS_SEC.map(p => `
            <button data-p="${p.v}" class="sec-pbtn"
              style="padding:5px 12px; border-radius:6px; border:1px solid #334155; cursor:pointer;
                     font-size:0.8rem; background:${p.v==='1y'?'#2563eb':'#0f172a'};
                     color:${p.v==='1y'?'#fff':'#94a3b8'};">${p.l}</button>`).join('')}
        </div>
      </div>
      <button class="run-btn" id="sec-run">▶ 비교 분석</button>
      <div id="sec-result" style="margin-top:20px;"></div>
    </div>`;

  let selPeriod = '1y';
  el.querySelectorAll('.sec-pbtn').forEach(b => {
    b.addEventListener('click', () => {
      selPeriod = b.dataset.p;
      el.querySelectorAll('.sec-pbtn').forEach(x => {
        x.style.background = x===b?'#2563eb':'#0f172a';
        x.style.color      = x===b?'#fff':'#94a3b8';
      });
    });
  });

  el.querySelector('#sec-run').addEventListener('click', async () => {
    const btn    = el.querySelector('#sec-run');
    const result = el.querySelector('#sec-result');
    const tickers = [...el.querySelectorAll('#sec-grid input:checked')].map(x => x.value);
    if (!tickers.length) { result.innerHTML='<p style="color:#ef4444;">최소 1개 선택하세요.</p>'; return; }
    btn.disabled=true; btn.textContent='수신 중...';
    result.innerHTML='<p style="color:#94a3b8;">Yahoo Finance 데이터 수신 중... (10~20초)</p>';
    try {
      const data = await api.industrySector({ tickers, period: selPeriod });
      let html = '';
      if (data.image) html += `<img src="${data.image}" style="width:100%; border-radius:8px; margin-bottom:16px;"/>`;
      if (data.summary) {
        const sorted = Object.entries(data.summary).sort((a,b)=>b[1].return_pct-a[1].return_pct);
        html += `<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.825rem;">
          <thead><tr style="background:#0f172a;">
            <th style="padding:8px 12px;text-align:left;color:#64748b;font-size:0.7rem;">섹터</th>
            <th style="padding:8px 12px;text-align:right;color:#64748b;font-size:0.7rem;">수익률</th>
            <th style="padding:8px 12px;text-align:right;color:#64748b;font-size:0.7rem;">연환산 변동성</th>
          </tr></thead><tbody>
          ${sorted.map(([n,s])=>`<tr style="border-bottom:1px solid #334155;">
            <td style="padding:8px 12px;color:#e2e8f0;">${n}</td>
            <td style="padding:8px 12px;text-align:right;font-weight:700;
                color:${s.return_pct>=0?'#22c55e':'#ef4444'};">${s.return_pct>=0?'▲':'▼'}${Math.abs(s.return_pct).toFixed(2)}%</td>
            <td style="padding:8px 12px;text-align:right;color:#94a3b8;">${s.annual_vol.toFixed(1)}%</td>
          </tr>`).join('')}
          </tbody></table></div>`;
      }
      result.innerHTML = html;
    } catch(e) {
      result.innerHTML=`<p style="color:#ef4444;">오류: ${e.message}</p>`;
    } finally {
      btn.disabled=false; btn.textContent='▶ 비교 분석';
    }
  });
}


// ── Tab 3: 산업 생애주기 ─────────────────────────────────────────────────────
const STAGES = ['도입기','성장기','성숙기','쇠퇴기'];
const STAGE_COLORS = {'도입기':'#3b82f6','성장기':'#22c55e','성숙기':'#f59e0b','쇠퇴기':'#ef4444'};
const STAGE_EXAMPLES = {
  '도입기': '양자컴퓨터, 핵융합, 뇌-컴퓨터 인터페이스',
  '성장기': 'AI 반도체, 전기차, 클라우드, 우주산업',
  '성숙기': '스마트폰, 자동차, 은행, 석유화학',
  '쇠퇴기': '인쇄매체, 유선전화, DVD 렌탈',
};

function renderLifecycle(el) {
  el.innerHTML = `
    <div style="background:#1e293b; border-radius:12px; padding:24px; border:1px solid #334155;">
      <!-- 단계 선택 카드 -->
      <div style="margin-bottom:20px;">
        <label class="param-label" style="margin-bottom:10px; display:block;">현재 생애주기 단계 선택</label>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px;" id="stage-cards">
          ${STAGES.map((s,i) => `
            <div data-stage="${s}" class="stage-card"
                 style="text-align:center; padding:16px 8px; background:#0f172a; border-radius:10px;
                        cursor:pointer; border:2px solid ${i===1?STAGE_COLORS[s]:'#334155'};
                        transition:all 0.15s;"
                 onclick="this.closest('#ia-content, div').querySelectorAll && (() => {})()">
              <div style="font-size:1.25rem; margin-bottom:6px;">${['🚀','📈','⚖️','📉'][i]}</div>
              <div style="font-size:0.875rem; font-weight:700; color:${STAGE_COLORS[s]};">${s}</div>
              <div style="font-size:0.68rem; color:#64748b; margin-top:4px; line-height:1.4;">${STAGE_EXAMPLES[s]}</div>
            </div>`).join('')}
        </div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px;">
        <div>
          <label class="param-label">분석 산업명</label>
          <input id="lc-ind" type="text" value="전기차" class="param-input"/>
        </div>
      </div>
      <button class="run-btn" id="lc-run">▶ 생애주기 분석</button>
      <div id="lc-result" style="margin-top:20px;"></div>
    </div>`;

  let selStage = '성장기';

  el.querySelectorAll('.stage-card').forEach(card => {
    card.addEventListener('click', () => {
      selStage = card.dataset.stage;
      el.querySelectorAll('.stage-card').forEach(c => {
        const col = STAGE_COLORS[c.dataset.stage];
        c.style.borderColor = c === card ? col : '#334155';
        c.style.background  = c === card ? col + '22' : '#0f172a';
      });
    });
  });

  el.querySelector('#lc-run').addEventListener('click', async () => {
    const btn    = el.querySelector('#lc-run');
    const result = el.querySelector('#lc-result');
    const industry = el.querySelector('#lc-ind').value.trim() || '전기차';
    btn.disabled=true; btn.textContent='분석 중...';
    result.innerHTML='<p style="color:#94a3b8;">생애주기 차트 생성 중...</p>';
    try {
      const data = await api.industryLifecycle({ stage: selStage, industry });
      let html = '';
      if (data.image) html += `<img src="${data.image}" style="width:100%; border-radius:8px; margin-bottom:16px;"/>`;
      if (data.strategies) {
        const col = STAGE_COLORS[selStage] || '#3b82f6';
        html += `
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div style="background:#0f172a; border-radius:10px; padding:16px; border-left:3px solid ${col};">
              <div style="font-size:0.75rem; font-weight:600; color:#64748b; margin-bottom:8px; text-transform:uppercase;">단계 특징</div>
              ${data.characteristics.map(c=>`<div style="font-size:0.825rem; color:#e2e8f0; margin-bottom:5px;">• ${c}</div>`).join('')}
            </div>
            <div style="background:#0f172a; border-radius:10px; padding:16px; border-left:3px solid #3b82f6;">
              <div style="font-size:0.75rem; font-weight:600; color:#64748b; margin-bottom:8px; text-transform:uppercase;">투자 전략</div>
              ${data.strategies.map(s=>`<div style="font-size:0.825rem; color:#3b82f6; margin-bottom:5px;">• ${s}</div>`).join('')}
            </div>
          </div>`;
      }
      result.innerHTML = html;
    } catch(e) {
      result.innerHTML=`<p style="color:#ef4444;">오류: ${e.message}</p>`;
    } finally {
      btn.disabled=false; btn.textContent='▶ 생애주기 분석';
    }
  });
}


// ── Tab 4: SWOT Matrix (순수 프론트엔드) ─────────────────────────────────────
const SWOT_DEFAULTS = {
  S: '높은 기술 진입장벽\n강력한 브랜드 파워\n원가 경쟁력',
  W: '높은 설비투자 비용\n특정 고객사 의존도\n인력 부족',
  O: 'AI 수요 급증\n신흥국 시장 확대\n정부 보조금 정책',
  T: '중국 경쟁사 부상\n경기침체 수요 감소\n공급망 불안정',
};
const SWOT_COLORS = { S:'#22c55e', W:'#ef4444', O:'#3b82f6', T:'#f59e0b' };
const SWOT_LABELS = { S:'강점 (Strengths)', W:'약점 (Weaknesses)', O:'기회 (Opportunities)', T:'위협 (Threats)' };

function renderSwot(el) {
  el.innerHTML = `
    <div style="background:#1e293b; border-radius:12px; padding:24px; border:1px solid #334155;">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:20px;">
        ${['S','W','O','T'].map(k => `
          <div>
            <label style="display:block; font-size:0.75rem; font-weight:600;
                   color:${SWOT_COLORS[k]}; margin-bottom:6px; text-transform:uppercase;">
              ${SWOT_LABELS[k]}
            </label>
            <textarea id="swot-${k}" rows="4" class="param-input" style="resize:vertical;">${SWOT_DEFAULTS[k]}</textarea>
          </div>`).join('')}
      </div>
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
        <div style="flex:1;">
          <label class="param-label">기업 / 산업명</label>
          <input id="swot-title" type="text" value="삼성전자 반도체" class="param-input"/>
        </div>
        <button class="run-btn" id="swot-run" style="margin-top:18px;">▶ SWOT 매트릭스 생성</button>
      </div>
      <div id="swot-result"></div>
    </div>`;

  el.querySelector('#swot-run').addEventListener('click', () => {
    const title = el.querySelector('#swot-title').value || 'SWOT 분석';
    const items = {};
    ['S','W','O','T'].forEach(k => {
      items[k] = el.querySelector(`#swot-${k}`).value
        .split('\n').map(l => l.trim()).filter(Boolean);
    });
    renderSwotMatrix(el.querySelector('#swot-result'), title, items);
  });

  // 기본 렌더
  setTimeout(() => el.querySelector('#swot-run').click(), 50);
}

function renderSwotMatrix(el, title, items) {
  const bg = { S:'#052e16', W:'#450a0a', O:'#082f49', T:'#431407' };
  const border = { S:'#22c55e', W:'#ef4444', O:'#3b82f6', T:'#f59e0b' };

  el.innerHTML = `
    <div style="background:#0f172a; border-radius:12px; padding:20px;">
      <div style="text-align:center; font-size:1rem; font-weight:700; color:#fff; margin-bottom:16px;">
        SWOT Matrix — ${title}
      </div>
      <!-- 축 레이블 -->
      <div style="display:grid; grid-template-columns:80px 1fr 1fr; gap:4px; margin-bottom:4px;">
        <div></div>
        <div style="text-align:center; font-size:0.75rem; font-weight:700; color:#22c55e; padding:4px;
             background:#052e16; border-radius:6px;">내부 요인 (Internal)</div>
        <div style="text-align:center; font-size:0.75rem; font-weight:700; color:#3b82f6; padding:4px;
             background:#082f49; border-radius:6px;">외부 요인 (External)</div>
      </div>
      <div style="display:grid; grid-template-columns:80px 1fr 1fr; gap:4px;">
        <!-- 행 레이블 + 4분면 -->
        <div style="display:grid; grid-template-rows:1fr 1fr; gap:4px;">
          <div style="display:flex; align-items:center; justify-content:center; padding:8px 4px;
               background:#052e16; border-radius:6px; font-size:0.72rem; font-weight:700;
               color:#22c55e; text-align:center; line-height:1.4;">긍정적<br/>(Positive)</div>
          <div style="display:flex; align-items:center; justify-content:center; padding:8px 4px;
               background:#450a0a; border-radius:6px; font-size:0.72rem; font-weight:700;
               color:#ef4444; text-align:center; line-height:1.4;">부정적<br/>(Negative)</div>
        </div>
        ${[['S','O'],['W','T']].map(row => `
          <div style="display:grid; grid-template-rows:1fr 1fr; gap:4px;">
            ${row.map(k => `
              <div style="background:${bg[k]}; border:1px solid ${border[k]}; border-radius:8px;
                   padding:14px; min-height:120px;">
                <div style="font-size:0.75rem; font-weight:700; color:${border[k]};
                     margin-bottom:8px; text-transform:uppercase;">${SWOT_LABELS[k]}</div>
                ${items[k].map(line => `
                  <div style="display:flex; align-items:flex-start; gap:6px; margin-bottom:5px;">
                    <span style="color:${border[k]}; font-size:0.8rem; flex-shrink:0; margin-top:1px;">▸</span>
                    <span style="font-size:0.8rem; color:#e2e8f0; line-height:1.4;">${line}</span>
                  </div>`).join('')}
              </div>`).join('')}
          </div>`).join('')}
      </div>
      <!-- SO/ST/WO/WT 전략 힌트 -->
      <div style="margin-top:16px; display:grid; grid-template-columns:repeat(2,1fr); gap:10px;">
        ${[
          { label:'SO 전략', desc:'강점으로 기회 활용', color:'#22c55e', hint:'공격적 확장 전략' },
          { label:'ST 전략', desc:'강점으로 위협 대응', color:'#f59e0b', hint:'다각화·방어 전략' },
          { label:'WO 전략', desc:'기회로 약점 보완', color:'#3b82f6', hint:'내부 역량 강화 전략' },
          { label:'WT 전략', desc:'약점·위협 최소화', color:'#ef4444', hint:'축소·철수 전략' },
        ].map(s => `
          <div style="background:#1e293b; border-radius:8px; padding:10px 14px;
               border-left:3px solid ${s.color}; display:flex; align-items:center; gap:10px;">
            <div>
              <div style="font-size:0.8rem; font-weight:700; color:${s.color};">${s.label}</div>
              <div style="font-size:0.75rem; color:#94a3b8;">${s.desc} → ${s.hint}</div>
            </div>
          </div>`).join('')}
      </div>
    </div>`;
}
