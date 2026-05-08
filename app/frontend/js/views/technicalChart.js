// ── 유틸 ─────────────────────────────────────────────────────────────────────
function tabShell(title, desc, tabs) {
  return `
    <div style="margin-bottom:20px;">
      <h1 style="font-size:1.2rem;font-weight:700;color:#0f172a;margin-bottom:6px;">
        <i class="fa-solid fa-chart-line"></i> ${title}
      </h1>
      <p style="font-size:0.85rem;color:#64748b;line-height:1.6;margin:0;">${desc}</p>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:20px;border-bottom:1px solid #d9e1ec;">
      ${tabs.map((t,i)=>`
        <button class="tc-tab" data-tab="${i}"
          style="padding:8px 14px;border:none;border-radius:8px 8px 0 0;cursor:pointer;
                 font-size:0.8rem;font-weight:600;transition:all 0.15s;
                 background:${i===0?'#2563eb':'#f1f5f9'};color:${i===0?'#fff':'#475569'};">
          ${t}
        </button>`).join('')}
    </div>
    <div id="tc-content"></div>`;
}
function activateTab(container, idx, renders) {
  container.querySelectorAll('.tc-tab').forEach((b,i)=>{
    b.style.background = i===idx?'#2563eb':'#f1f5f9';
    b.style.color      = i===idx?'#fff':'#475569';
  });
  renders[idx](container.querySelector('#tc-content'));
}

function card(title, icon, body, accent='#2563eb') {
  return `<div style="background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;
                      border:1px solid #e2e8f0;border-left:3px solid ${accent};box-shadow:0 1px 4px #0001;">
    <h3 style="font-size:0.92rem;font-weight:700;color:#0f172a;margin:0 0 14px;">
      <i class="${icon}" style="color:${accent};margin-right:6px;"></i>${title}
    </h3>${body}</div>`;
}
function info(html, color='#3b82f6') {
  return `<div style="background:${color}10;border:1px solid ${color}40;border-radius:8px;
                      padding:11px 14px;font-size:0.82rem;color:#334155;line-height:1.65;margin-bottom:14px;">${html}</div>`;
}
function pill(label, color) {
  return `<span style="display:inline-block;background:${color}18;color:${color};border:1px solid ${color}44;
                       border-radius:20px;padding:2px 10px;font-size:0.73rem;font-weight:600;margin:2px;">${label}</span>`;
}

// ── Canvas 차트 엔진 ─────────────────────────────────────────────────────────
class CandleChart {
  constructor(canvas, prices, options={}) {
    this.cv  = canvas;
    this.ctx = canvas.getContext('2d');
    this.prices = prices;   // [{o,h,l,c,v}]
    this.opt = { padL:52, padR:20, padT:24, padB:36, ...options };
    this.overlays = [];     // {type, data, color, label}
    this.annotations = [];  // {type, params}
    this.resize();
  }
  resize() {
    const dpr = window.devicePixelRatio||1;
    const w   = this.cv.offsetWidth;
    const h   = this.cv.offsetHeight;
    this.cv.width  = w*dpr;
    this.cv.height = h*dpr;
    this.ctx.scale(dpr,dpr);
    this.W = w; this.H = h;
  }
  addLine(data, color='#2563eb', label='') { this.overlays.push({type:'line',data,color,label}); }
  addBand(upper, lower, color='#3b82f6') { this.overlays.push({type:'band',upper,lower,color}); }
  addTrendLine(x1,y1,x2,y2,color='#f59e0b',dash=[]) { this.annotations.push({type:'trendline',x1,y1,x2,y2,color,dash}); }
  addHLine(y, color='#94a3b8', dash=[4,3], label='') { this.annotations.push({type:'hline',y,color,dash,label}); }
  addArrow(xi, label, color='#22c55e', dir=1) { this.annotations.push({type:'arrow',xi,label,color,dir}); }
  addWaveLabel(xi, label, color='#a855f7') { this.annotations.push({type:'wave',xi,label,color}); }

  draw() {
    const {ctx,W,H,opt,prices} = this;
    const {padL,padR,padT,padB} = opt;
    const cW = W - padL - padR;
    const cH = H - padT - padB;
    const n  = prices.length;

    const allH = prices.map(p=>p.h), allL = prices.map(p=>p.l);
    const allVals = [...allH, ...allL,
      ...this.overlays.flatMap(o=>o.type==='line'?o.data:o.type==='band'?[...o.upper,...o.lower]:[]).filter(v=>v!=null)];
    const maxP = Math.max(...allVals)*1.01;
    const minP = Math.min(...allVals)*0.99;
    const rng  = maxP - minP || 1;

    const xOf = i => padL + (i+0.5)/n*cW;
    const yOf = v => padT + (1-(v-minP)/rng)*cH;
    const bW  = Math.max(2, cW/n*0.6);

    ctx.clearRect(0,0,W,H);

    // grid
    ctx.strokeStyle='#f1f5f9'; ctx.lineWidth=1;
    for (let i=0;i<=4;i++) {
      const y = padT + i/4*cH;
      ctx.beginPath(); ctx.moveTo(padL,y); ctx.lineTo(W-padR,y); ctx.stroke();
      const v = maxP - i/4*rng;
      ctx.fillStyle='#94a3b8'; ctx.font='10px sans-serif'; ctx.textAlign='right';
      ctx.fillText(v>=1000?Math.round(v).toLocaleString():v.toFixed(1), padL-4, y+4);
    }

    // bands
    this.overlays.filter(o=>o.type==='band').forEach(o=>{
      ctx.beginPath();
      o.upper.forEach((v,i)=>{ if(v==null) return; i===0?ctx.moveTo(xOf(i),yOf(v)):ctx.lineTo(xOf(i),yOf(v)); });
      [...o.lower].reverse().forEach((v,i)=>{ if(v==null) return; ctx.lineTo(xOf(n-1-i),yOf(v)); });
      ctx.closePath();
      ctx.fillStyle=o.color+'22'; ctx.fill();
    });

    // candles
    prices.forEach((p,i)=>{
      const x  = xOf(i);
      const yO = yOf(p.o), yC = yOf(p.c), yHi = yOf(p.h), yLo = yOf(p.l);
      const bull = p.c >= p.o;
      ctx.strokeStyle = bull?'#2563eb':'#ef4444';
      ctx.fillStyle   = bull?'#dbeafe':'#fee2e2';
      ctx.lineWidth   = 1;
      ctx.beginPath(); ctx.moveTo(x,yHi); ctx.lineTo(x,yLo); ctx.stroke();
      const top = Math.min(yO,yC), ht = Math.max(2, Math.abs(yC-yO));
      ctx.fillRect(x-bW/2, top, bW, ht);
      ctx.strokeRect(x-bW/2, top, bW, ht);
    });

    // line overlays
    this.overlays.filter(o=>o.type==='line').forEach(o=>{
      ctx.beginPath(); ctx.strokeStyle=o.color; ctx.lineWidth=1.5;
      let started=false;
      o.data.forEach((v,i)=>{ if(v==null) return; started?ctx.lineTo(xOf(i),yOf(v)):ctx.moveTo(xOf(i),yOf(v)); started=true; });
      ctx.stroke();
    });

    // hlines
    this.annotations.filter(a=>a.type==='hline').forEach(a=>{
      ctx.save(); ctx.setLineDash(a.dash); ctx.strokeStyle=a.color; ctx.lineWidth=1.2;
      ctx.beginPath(); ctx.moveTo(padL,yOf(a.y)); ctx.lineTo(W-padR,yOf(a.y)); ctx.stroke();
      ctx.restore();
      if(a.label){ ctx.fillStyle=a.color; ctx.font='10px sans-serif'; ctx.textAlign='left'; ctx.fillText(a.label,W-padR+2,yOf(a.y)+4); }
    });

    // trendlines
    this.annotations.filter(a=>a.type==='trendline').forEach(a=>{
      ctx.save(); ctx.setLineDash(a.dash); ctx.strokeStyle=a.color; ctx.lineWidth=1.8;
      ctx.beginPath(); ctx.moveTo(xOf(a.x1),yOf(a.y1)); ctx.lineTo(xOf(a.x2),yOf(a.y2)); ctx.stroke();
      ctx.restore();
    });

    // arrows
    this.annotations.filter(a=>a.type==='arrow').forEach(a=>{
      const x=xOf(a.xi), y=padT+cH+8;
      ctx.fillStyle=a.color; ctx.font='bold 10px sans-serif'; ctx.textAlign='center';
      ctx.fillText(a.dir>0?'▲':'▼', x, y-2);
      ctx.fillText(a.label, x, y+10);
    });

    // wave labels
    this.annotations.filter(a=>a.type==='wave').forEach(a=>{
      const p = prices[a.xi];
      const x = xOf(a.xi), y = yOf(p.h)-10;
      ctx.fillStyle=a.color; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
      ctx.fillText(a.label, x, y);
    });

    // x-axis date labels
    ctx.fillStyle='#94a3b8'; ctx.font='10px sans-serif'; ctx.textAlign='center';
    const step = Math.max(1, Math.floor(n/8));
    prices.forEach((p,i)=>{ if(i%step===0&&p.date){ ctx.fillText(p.date, xOf(i), H-padB+14); } });
  }
}

// ── 가격 데이터 생성기 ────────────────────────────────────────────────────────
function genPrices(n=80, start=50000, seed=42, scenario='trend_up') {
  let rng = seed;
  const rand = () => { rng=(rng*1664525+1013904223)%2**32; return rng/2**32; };
  const randn = () => { const u=rand(),v=rand(); return Math.sqrt(-2*Math.log(u+1e-10))*Math.cos(2*Math.PI*v); };
  const prices=[];
  let price=start, vol=start*0.02;
  const months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  for(let i=0;i<n;i++){
    let drift=0;
    if(scenario==='trend_up')   drift=price*0.004;
    if(scenario==='trend_down') drift=-price*0.004;
    if(scenario==='sideways')   drift=(i%20<10?1:-1)*price*0.001;
    if(scenario==='wave') {
      const phase=i/n*Math.PI*2;
      drift=Math.sin(phase)*price*0.006+(i<n*0.6?price*0.003:-price*0.002);
    }
    const chg=drift+randn()*vol;
    const o=price, c=Math.max(o*0.85,o+chg);
    const hi=Math.max(o,c)*(1+rand()*0.015);
    const lo=Math.min(o,c)*(1-rand()*0.015);
    const m=months[Math.floor(i/7)%12], d=(i%28)+1;
    prices.push({o,h:hi,l:lo,c,v:Math.floor(rand()*1e6+2e5),date:`${m}${d}`});
    price=c; vol=vol*0.95+Math.abs(chg)*0.05;
  }
  return prices;
}

function calcMA(prices, n) {
  return prices.map((_,i)=>{
    if(i<n-1) return null;
    return prices.slice(i-n+1,i+1).reduce((s,p)=>s+p.c,0)/n;
  });
}
function calcRSI(prices, n=14) {
  const d=prices.map((_,i)=>i===0?0:prices[i].c-prices[i-1].c);
  return prices.map((_,i)=>{
    if(i<n) return null;
    const slice=d.slice(i-n+1,i+1);
    const g=slice.filter(v=>v>0).reduce((s,v)=>s+v,0)/n;
    const l=-slice.filter(v=>v<0).reduce((s,v)=>s+v,0)/n;
    return l===0?100:100-100/(1+g/l);
  });
}
function calcBB(prices, n=20) {
  const mid=calcMA(prices,n);
  const upper=prices.map((_,i)=>{
    if(i<n-1) return null;
    const slice=prices.slice(i-n+1,i+1).map(p=>p.c);
    const m=slice.reduce((s,v)=>s+v,0)/n;
    const sd=Math.sqrt(slice.reduce((s,v)=>s+(v-m)**2,0)/n);
    return m+2*sd;
  });
  const lower=prices.map((_,i)=>{
    if(i<n-1) return null;
    const slice=prices.slice(i-n+1,i+1).map(p=>p.c);
    const m=slice.reduce((s,v)=>s+v,0)/n;
    const sd=Math.sqrt(slice.reduce((s,v)=>s+(v-m)**2,0)/n);
    return m-2*sd;
  });
  return {mid,upper,lower};
}
function calcMACD(prices,f=12,s=26,sig=9) {
  const ema=(data,span)=>{
    const k=2/(span+1); const out=[];
    data.forEach((v,i)=>out.push(i===0?v:out[i-1]*(1-k)+v*k));
    return out;
  };
  const closes=prices.map(p=>p.c);
  const e12=ema(closes,f), e26=ema(closes,s);
  const macd=e12.map((v,i)=>i<s-1?null:v-e26[i]);
  const validMacd=macd.map(v=>v??0);
  const sigLine=ema(validMacd,sig).map((v,i)=>macd[i]==null?null:v);
  const hist=macd.map((v,i)=>v==null?null:v-sigLine[i]);
  return {macd,signal:sigLine,hist};
}

// ── 미니 라인차트 (RSI / MACD용) ─────────────────────────────────────────────
function drawMiniChart(canvas, data, min, max, color='#8b5cf6', refLines=[]) {
  const ctx=canvas.getContext('2d');
  const dpr=window.devicePixelRatio||1;
  canvas.width=canvas.offsetWidth*dpr; canvas.height=canvas.offsetHeight*dpr;
  ctx.scale(dpr,dpr);
  const W=canvas.offsetWidth, H=canvas.offsetHeight;
  const pL=40,pR=8,pT=6,pB=20;
  const cW=W-pL-pR, cH=H-pT-pB;
  const rng=max-min||1;
  const xOf=i=>(i/(data.length-1))*cW+pL;
  const yOf=v=>pT+(1-(v-min)/rng)*cH;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
  refLines.forEach(({v,c,d})=>{
    ctx.save(); ctx.setLineDash(d||[4,3]); ctx.strokeStyle=c||'#94a3b8'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(pL,yOf(v)); ctx.lineTo(W-pR,yOf(v)); ctx.stroke();
    ctx.restore();
    ctx.fillStyle=c||'#94a3b8'; ctx.font='9px sans-serif'; ctx.textAlign='right';
    ctx.fillText(v,pL-2,yOf(v)+3);
  });
  ctx.beginPath(); ctx.strokeStyle=color; ctx.lineWidth=1.5;
  let started=false;
  data.forEach((v,i)=>{
    if(v==null) return;
    started?ctx.lineTo(xOf(i),yOf(v)):ctx.moveTo(xOf(i),yOf(v)); started=true;
  });
  ctx.stroke();
  // zero fill for MACD hist
  if(refLines.some(r=>r.v===0)) {
    data.forEach((v,i)=>{
      if(v==null) return;
      const x=xOf(i), y0=yOf(0), y1=yOf(v), h=y1-y0;
      ctx.fillStyle=v>=0?'#22c55e44':'#ef444444';
      ctx.fillRect(x-2, Math.min(y0,y1), 4, Math.abs(h));
    });
  }
  ctx.fillStyle='#94a3b8'; ctx.font='9px sans-serif'; ctx.textAlign='right';
  ctx.fillText(max.toFixed(0),pL-2,pT+8);
  ctx.fillText(min.toFixed(0),pL-2,H-pB+4);
}

// ── 탭 렌더러 ─────────────────────────────────────────────────────────────────

// ① 기업 선정
function renderStockSelect(content, state) {
  const companies = [
    {name:'삼성전자', ticker:'005930.KS', sector:'반도체·IT', tags:['대형주','배당','수출'], scenario:'trend_up', start:71000},
    {name:'SK하이닉스', ticker:'000660.KS', sector:'반도체', tags:['사이클','HBM'], scenario:'wave', start:168000},
    {name:'NAVER', ticker:'035420.KS', sector:'플랫폼', tags:['광고','커머스'], scenario:'sideways', start:165000},
    {name:'현대차', ticker:'005380.KS', sector:'자동차·EV', tags:['EV전환','배당'], scenario:'trend_up', start:230000},
    {name:'LG에너지솔루션', ticker:'373220.KS', sector:'2차전지', tags:['EV배터리'], scenario:'wave', start:380000},
    {name:'카카오', ticker:'035720.KS', sector:'플랫폼·핀테크', tags:['구독','핀테크'], scenario:'trend_down', start:40000},
    {name:'셀트리온', ticker:'068270.KS', sector:'바이오', tags:['바이오시밀러'], scenario:'sideways', start:165000},
    {name:'삼성바이오로직스', ticker:'207940.KS', sector:'바이오', tags:['CMO'], scenario:'trend_up', start:850000},
  ];

  content.innerHTML = `
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-bottom:20px;">
      ${companies.map((c,i)=>`
        <div class="stock-card" data-idx="${i}" style="background:#fff;border-radius:10px;padding:16px;
             border:2px solid ${state.selected===i?'#2563eb':'#e2e8f0'};cursor:pointer;transition:all 0.15s;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
            <div>
              <div style="font-size:0.95rem;font-weight:700;color:#0f172a;">${c.name}</div>
              <div style="font-size:0.75rem;color:#64748b;">${c.ticker}</div>
            </div>
            <span style="background:#eff6ff;color:#2563eb;border-radius:6px;padding:2px 8px;font-size:0.72rem;font-weight:600;">${c.sector}</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px;">
            ${c.tags.map(t=>pill(t,'#64748b')).join('')}
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:0.78rem;color:#94a3b8;">시뮬레이션 추세</span>
            <span style="font-size:0.78rem;font-weight:600;color:${
              c.scenario==='trend_up'?'#16a34a':c.scenario==='trend_down'?'#dc2626':
              c.scenario==='wave'?'#a855f7':'#f59e0b'};">
              ${c.scenario==='trend_up'?'↑ 상승추세':c.scenario==='trend_down'?'↓ 하락추세':
                c.scenario==='wave'?'〜 파동형':'─ 횡보'}
            </span>
          </div>
          ${state.selected===i?`<div style="margin-top:8px;padding:4px 8px;background:#eff6ff;border-radius:6px;font-size:0.75rem;color:#2563eb;font-weight:600;">✓ 선택됨 — 나머지 탭에서 분석 가능</div>`:''}
        </div>`).join('')}
    </div>
    <div id="stock-preview" style="${state.selected==null?'display:none':''}">
      ${state.selected!=null?renderStockPreview(companies[state.selected]):''}
    </div>`;

  content.querySelectorAll('.stock-card').forEach(el=>{
    el.addEventListener('click',()=>{
      state.selected = +el.dataset.idx;
      state.company  = companies[state.selected];
      renderStockSelect(content, state);
    });
  });
}

function renderStockPreview(c) {
  return card(`${c.name} — 분석 미리보기`, 'fa-solid fa-magnifying-glass-chart', `
    ${info(`<strong>${c.name} (${c.ticker})</strong>를 선택했습니다. 위 탭에서 추세, 이동평균, 캔들패턴, 지표, 파동 분석을 순서대로 실습하세요.`,'#2563eb')}
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;">
      ${[['섹터',c.sector,'#3b82f6'],['추세 유형',c.scenario,'#a855f7'],['기준가격',c.start.toLocaleString()+'원','#22c55e']].map(([l,v,col])=>`
        <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;">
          <div style="font-size:0.72rem;color:#64748b;margin-bottom:4px;">${l}</div>
          <div style="font-size:0.9rem;font-weight:700;color:${col};">${v}</div>
        </div>`).join('')}
    </div>`, '#2563eb');
}

// ② 추세분석
function renderTrend(content, state) {
  const c = state.company;
  const prices = genPrices(80, c.start, 7, c.scenario);

  content.innerHTML = card('추세분석 — 추세선 · 채널 · 강도', 'fa-solid fa-arrow-trend-up', `
    ${info(`<strong>분석 기업: ${c.name}</strong> | 추세선 = 연속 저점/고점 연결 | 채널 = 추세선 + 평행선 | ADX > 25 = 강한 추세`,'#22c55e')}
    <canvas id="cv-trend" style="width:100%;height:340px;display:block;border-radius:8px;border:1px solid #e2e8f0;"></canvas>
    <div id="trend-signal" style="margin-top:14px;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;"></div>
    <div style="margin-top:16px;">
      <div style="font-size:0.82rem;font-weight:600;color:#0f172a;margin-bottom:10px;">추세 판단 기준</div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:0.8rem;">
          <tr style="background:#f8fafc;">
            <th style="padding:7px 10px;text-align:left;color:#475569;border-bottom:1px solid #e2e8f0;">구분</th>
            <th style="padding:7px 10px;text-align:left;color:#475569;border-bottom:1px solid #e2e8f0;">조건</th>
            <th style="padding:7px 10px;text-align:left;color:#475569;border-bottom:1px solid #e2e8f0;">매매 관점</th>
          </tr>
          ${[['상승추세','HH·HL 연속, MA 정배열, ADX>25','추세선 저점 매수 / 채널 상단 이익실현'],
             ['하락추세','LH·LL 연속, MA 역배열, ADX>25','추세선 고점 매도 / 반등 시 공매도'],
             ['횡보','가격이 박스권 내 등락, ADX<20','박스권 하단 매수, 상단 이익실현'],
             ['추세 전환','추세선 종가 이탈 + 거래량 폭증','포지션 축소 후 신추세 확인 대기']].map(([g,c,m])=>`
            <tr style="border-bottom:1px solid #f1f5f9;">
              <td style="padding:7px 10px;color:#0f172a;font-weight:600;">${g}</td>
              <td style="padding:7px 10px;color:#475569;">${c}</td>
              <td style="padding:7px 10px;color:#2563eb;font-size:0.78rem;">${m}</td>
            </tr>`).join('')}
        </table>
      </div>
    </div>`, '#22c55e');

  requestAnimationFrame(()=>{
    const cv = content.querySelector('#cv-trend');
    if(!cv) return;
    cv.style.height='340px';
    const chart = new CandleChart(cv, prices);
    const ma20  = calcMA(prices,20);
    const ma60  = calcMA(prices,60);
    chart.addLine(ma20,'#2563eb','MA20');
    chart.addLine(ma60,'#ef4444','MA60');

    // 추세선 자동 감지
    const lows  = prices.map(p=>p.l);
    const highs = prices.map(p=>p.h);
    const li1=10, li2=40, hi1=5, hi2=35;
    chart.addTrendLine(li1,lows[li1],li2,lows[li2],'#22c55e');
    chart.addTrendLine(li1,highs[hi1],li2,highs[hi2],'#22c55e',[4,3]);
    chart.draw();

    // 신호 판단
    const last   = prices[prices.length-1].c;
    const m20    = ma20[ma20.length-1];
    const m60    = ma60[ma60.length-1];
    const trend  = last>m20&&m20>m60?'상승추세':last<m20&&m20<m60?'하락추세':'횡보/전환';
    const tColor = trend==='상승추세'?'#16a34a':trend==='하락추세'?'#dc2626':'#f59e0b';
    const hh = prices.slice(-20).every((_,i,a)=>i===0||a[i].h>=a[i-1].h*0.97);
    content.querySelector('#trend-signal').innerHTML = [
      ['현재 추세',trend,tColor],['MA 배열',m20>m60?'정배열(강세)':'역배열(약세)',m20>m60?'#16a34a':'#dc2626'],
      ['고저점 구조',hh?'HH·HL (상승)':'LH·LL (하락)',hh?'#16a34a':'#dc2626'],['현재가 vs MA20',last>m20?'MA20 위':'MA20 아래',last>m20?'#16a34a':'#dc2626'],
    ].map(([l,v,c])=>`
      <div style="background:#f8fafc;border-radius:8px;padding:12px;text-align:center;border:1px solid #e2e8f0;">
        <div style="font-size:0.73rem;color:#64748b;margin-bottom:4px;">${l}</div>
        <div style="font-size:0.88rem;font-weight:700;color:${c};">${v}</div>
      </div>`).join('');
  });
}

// ③ 이동평균선
function renderMA(content, state) {
  const c = state.company;
  const prices = genPrices(80, c.start, 13, c.scenario);
  const ma5=calcMA(prices,5), ma20=calcMA(prices,20), ma60=calcMA(prices,60);

  content.innerHTML = card('이동평균선 — 골든크로스 · 데드크로스 · 정배열', 'fa-solid fa-chart-line', `
    ${info(`MA5(단기)·MA20(중기)·MA60(장기)의 배열과 크로스 신호를 확인합니다. 골든크로스(단기↑장기)는 상승 전환 신호입니다.`,'#3b82f6')}
    <canvas id="cv-ma" style="width:100%;height:320px;display:block;border-radius:8px;border:1px solid #e2e8f0;"></canvas>
    <div id="ma-signals" style="margin-top:14px;"></div>`, '#3b82f6');

  requestAnimationFrame(()=>{
    const cv=content.querySelector('#cv-ma');
    if(!cv) return;
    const chart=new CandleChart(cv,prices);
    chart.addLine(ma5,'#22c55e','MA5');
    chart.addLine(ma20,'#2563eb','MA20');
    chart.addLine(ma60,'#ef4444','MA60');

    // 크로스 포인트 표시
    ma20.forEach((v,i)=>{
      if(i<1||v==null||ma60[i]==null) return;
      if(ma20[i-1]<ma60[i-1]&&ma20[i]>=ma60[i]) chart.addArrow(i,'골든',`#22c55e`,1);
      if(ma20[i-1]>ma60[i-1]&&ma20[i]<=ma60[i]) chart.addArrow(i,'데드','#ef4444',-1);
    });
    chart.draw();

    const m5=ma5[ma5.length-1], m20=ma20[ma20.length-1], m60=ma60[ma60.length-1];
    const last=prices[prices.length-1].c;
    const crossType = m20>m60?'골든크로스 상태':'데드크로스 상태';
    const arr = m20>m60?'정배열':'역배열';
    content.querySelector('#ma-signals').innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px;">
        ${[['MA5',m5,'#22c55e'],['MA20',m20,'#2563eb'],['MA60',m60,'#ef4444'],['배열상태',arr,m20>m60?'#16a34a':'#dc2626'],['크로스',crossType,m20>m60?'#16a34a':'#dc2626']].map(([l,v,col])=>`
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:11px;text-align:center;">
            <div style="font-size:0.72rem;color:#64748b;margin-bottom:4px;">${l}</div>
            <div style="font-size:0.85rem;font-weight:700;color:${col};">${typeof v==='number'?Math.round(v).toLocaleString()+'원':v}</div>
          </div>`).join('')}
      </div>
      ${info(`<strong>실전 전략:</strong> ${m20>m60?`정배열 — MA5가 MA20 위를 유지하는 한 눌림목(MA20 터치)마다 매수 기회. 목표는 채널 상단, 손절은 MA60 이탈.`:`역배열 — 반등 시 MA20이 저항. 데드크로스 확인 후 반등매도(Short) 또는 현금 보유 전략.`}`,'#3b82f6')}`;
  });
}

// ④ 캔들 패턴
function renderCandle(content, state) {
  const patterns = [
    {name:'망치봉 (Hammer)',   signal:'반등', color:'#22c55e',
     desc:'하락 추세 말단에서 아래 꼬리가 몸통의 2배 이상. 매도세가 매수세에 밀린 증거.',
     cond:'하락 추세 + 지지선 근처 + 거래량 증가', target:'직전 저항선', stop:'망치봉 저가 이하'},
    {name:'베어리쉬 엔걸핑',   signal:'하락', color:'#ef4444',
     desc:'큰 음봉이 전날 양봉 몸통 전체를 감싸며 매도 압력 폭증 신호.',
     cond:'상승 추세 + 저항선 근처 + 거래량 증가', target:'직전 지지선', stop:'음봉 고가 이상'},
    {name:'도지 (Doji)',       signal:'전환', color:'#f59e0b',
     desc:'시가=종가. 매수·매도 균형. 추세 방향에 따라 전환 또는 조정 신호.',
     cond:'추세 말단 + 지지·저항 근처', target:'다음봉 방향 확인 후 진입', stop:'도지 고·저가 이탈'},
    {name:'샛별 (Morning Star)',signal:'반등', color:'#22c55e',
     desc:'음봉→소형봉→양봉 3캔들. 바닥 반전의 강한 신호.',
     cond:'하락 추세 말단 + 과매도', target:'38.2%~61.8% 되돌림', stop:'첫 음봉 저가'},
    {name:'이브닝스타',         signal:'하락', color:'#ef4444',
     desc:'양봉→소형봉→음봉. 상단 반전의 강한 신호. 샛별의 반대.',
     cond:'상승 추세 말단 + 과매수', target:'38.2% 되돌림', stop:'첫 양봉 고가'},
    {name:'불리쉬 엔걸핑',     signal:'반등', color:'#22c55e',
     desc:'큰 양봉이 전날 음봉 전체를 감쌈. 강한 매수 전환.',
     cond:'하락 추세 + 지지선', target:'직전 고점', stop:'음봉 저가'},
  ];

  const selectedPat = state.pat ?? 0;
  const p = patterns[selectedPat];

  content.innerHTML = `
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
      ${patterns.map((pt,i)=>`
        <button class="pat-btn" data-idx="${i}"
          style="padding:7px 14px;border-radius:20px;border:1px solid ${state.pat===i?pt.color:'#e2e8f0'};
                 background:${state.pat===i?pt.color+'18':'#fff'};color:${state.pat===i?pt.color:'#475569'};
                 font-size:0.8rem;font-weight:600;cursor:pointer;">
          ${pt.name}
        </button>`).join('')}
    </div>
    ${card(p.name, 'fa-solid fa-chart-candlestick', `
      ${info(`<strong>신호:</strong> ${p.signal==='반등'?'📈 매수 신호':'📉 매도 신호'} &nbsp;|&nbsp; ${p.desc}`
        , p.signal==='반등'?'#22c55e':'#ef4444')}
      <canvas id="cv-candle" style="width:100%;height:280px;display:block;border-radius:8px;border:1px solid #e2e8f0;"></canvas>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px;">
        ${[['진입 조건',p.cond,'#2563eb'],['목표가',p.target,'#22c55e'],['손절',p.stop,'#ef4444']].map(([l,v,c])=>`
          <div style="background:#f8fafc;border-radius:8px;padding:12px;border-left:3px solid ${c};">
            <div style="font-size:0.72rem;color:#64748b;margin-bottom:4px;">${l}</div>
            <div style="font-size:0.8rem;color:#0f172a;line-height:1.5;">${v}</div>
          </div>`).join('')}
      </div>`, p.color)}`;

  content.querySelectorAll('.pat-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{ state.pat=+btn.dataset.idx; renderCandle(content,state); });
  });

  requestAnimationFrame(()=>{
    const cv=content.querySelector('#cv-candle');
    if(!cv) return;
    const c=state.company;
    const prices=genPrices(40, c.start, 19+selectedPat, selectedPat%2===0?'trend_up':'trend_down');
    const chart=new CandleChart(cv,prices,{padL:56,padR:16,padT:20,padB:30});
    const ma20=calcMA(prices,20);
    chart.addLine(ma20,'#2563eb');
    const mid=prices.length-3;
    chart.addArrow(mid, p.signal==='반등'?'↑패턴':'↓패턴', p.signal==='반등'?'#22c55e':'#ef4444', p.signal==='반등'?1:-1);
    chart.draw();
  });
}

// ⑤ 보조지표
function renderIndicators(content, state) {
  const c = state.company;
  const prices = genPrices(80, c.start, 31, c.scenario);
  const rsi = calcRSI(prices);
  const {macd, signal, hist} = calcMACD(prices);
  const {mid, upper, lower} = calcBB(prices);

  content.innerHTML = card('보조지표 — RSI · MACD · 볼린저밴드', 'fa-solid fa-gauge-high', `
    ${info(`RSI(과매수/과매도) · MACD(추세 전환) · 볼린저밴드(변동성·밴드 위치)를 함께 보면 신호 신뢰도가 높아집니다.`,'#a855f7')}
    <canvas id="cv-ind" style="width:100%;height:280px;display:block;border-radius:8px;border:1px solid #e2e8f0;"></canvas>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">
      <div>
        <div style="font-size:0.78rem;font-weight:600;color:#475569;margin-bottom:6px;">RSI (14)</div>
        <canvas id="cv-rsi" style="width:100%;height:100px;display:block;border-radius:6px;"></canvas>
      </div>
      <div>
        <div style="font-size:0.78rem;font-weight:600;color:#475569;margin-bottom:6px;">MACD (12,26,9)</div>
        <canvas id="cv-macd" style="width:100%;height:100px;display:block;border-radius:6px;"></canvas>
      </div>
    </div>
    <div id="ind-signal" style="margin-top:14px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;"></div>`, '#a855f7');

  requestAnimationFrame(()=>{
    const cvMain=content.querySelector('#cv-ind');
    if(!cvMain) return;
    const chart=new CandleChart(cvMain,prices);
    chart.addLine(mid,'#2563eb','MA20');
    chart.addBand(upper,lower,'#94a3b8');
    chart.draw();

    const cvRsi=content.querySelector('#cv-rsi');
    if(cvRsi) drawMiniChart(cvRsi,rsi,0,100,'#8b5cf6',[{v:70,c:'#ef4444'},{v:30,c:'#22c55e'}]);

    const cvMacd=content.querySelector('#cv-macd');
    if(cvMacd) {
      const mRange=Math.max(...macd.filter(v=>v!=null).map(Math.abs))*1.5||1;
      drawMiniChart(cvMacd,macd,-mRange,mRange,'#2563eb',[{v:0,c:'#94a3b8'}]);
    }

    const lastRsi=rsi.filter(v=>v!=null).slice(-1)[0];
    const lastMacd=macd.filter(v=>v!=null).slice(-1)[0];
    const lastSig=signal.filter(v=>v!=null).slice(-1)[0];
    const lastC=prices[prices.length-1].c;
    const lastUp=upper.filter(v=>v!=null).slice(-1)[0];
    const lastLo=lower.filter(v=>v!=null).slice(-1)[0];
    const bbPct=((lastC-lastLo)/(lastUp-lastLo)*100).toFixed(0);
    const rsiSig=lastRsi>70?'과매수 ⚠️':lastRsi<30?'과매도 ✅':'중립';
    const macdSig=lastMacd>lastSig?'골든크로스 ↑':'데드크로스 ↓';

    content.querySelector('#ind-signal').innerHTML=[
      ['RSI',lastRsi.toFixed(1),lastRsi>70?'#ef4444':lastRsi<30?'#22c55e':'#64748b'],
      ['RSI 신호',rsiSig,lastRsi>70?'#ef4444':lastRsi<30?'#22c55e':'#64748b'],
      ['MACD 신호',macdSig,lastMacd>lastSig?'#22c55e':'#ef4444'],
      ['BB 위치',`${bbPct}%`,+bbPct>70?'#ef4444':+bbPct<30?'#22c55e':'#64748b'],
    ].map(([l,v,c])=>`
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:11px;text-align:center;">
        <div style="font-size:0.72rem;color:#64748b;margin-bottom:4px;">${l}</div>
        <div style="font-size:0.88rem;font-weight:700;color:${c};">${v}</div>
      </div>`).join('');
  });
}

// ⑥ 엘리어트 파동
function renderElliott(content, state) {
  const c = state.company;
  const prices = genPrices(80, c.start, 37, 'wave');

  content.innerHTML = card('엘리어트 파동 — 충격5파 + 조정3파 분석', 'fa-solid fa-wave-square', `
    ${info(`주가가 추세 방향으로 5파(충격파) + 반대 방향으로 3파(조정파: a-b-c)로 움직인다는 이론입니다. 피보나치 비율로 각 파동의 목표·되돌림 구간을 계산합니다.`,'#a855f7')}
    <canvas id="cv-elliott" style="width:100%;height:340px;display:block;border-radius:8px;border:1px solid #e2e8f0;"></canvas>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:16px;">
      ${[
        ['1파','첫 상승, 인지 어려움','하락 추세 속 반등으로 보임','#60a5fa'],
        ['2파','1파 되돌림(최대 61.8%)','1파 시작점 이탈 시 파동 무효','#3b82f6'],
        ['3파','가장 강하고 긴 파동','거래량 폭발, 추격 매수','#1d4ed8'],
        ['4파','2차 조정(1파 고점 불침범)','3파 보유자 일부 차익실현','#7c3aed'],
        ['5파','마지막 상승, 다이버전스','거래량 줄고 RSI 다이버전스','#a855f7'],
        ['abc조정','상승분 38.2~61.8% 되돌림','c파에서 새 진입 기회 탐색','#64748b'],
      ].map(([wave,desc,tip,col])=>`
        <div style="background:#f8fafc;border-radius:8px;padding:12px;border-left:3px solid ${col};">
          <div style="font-size:0.88rem;font-weight:700;color:${col};margin-bottom:4px;">${wave}</div>
          <div style="font-size:0.78rem;color:#0f172a;margin-bottom:4px;">${desc}</div>
          <div style="font-size:0.75rem;color:#64748b;">${tip}</div>
        </div>`).join('')}
    </div>
    <div style="margin-top:16px;padding:14px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;font-size:0.82rem;color:#334155;line-height:1.7;">
      <strong style="color:#0f172a;">실전 진입 전략:</strong><br>
      2파 완성(1파 61.8% 되돌림) + RSI 과매도 + 지지선 확인 → <span style="color:#16a34a;font-weight:600;">3파 진입 최적 시점</span><br>
      5파 고점 + RSI 다이버전스 + 피보나치 161.8% 확장 → <span style="color:#dc2626;font-weight:600;">조정파 a 시작 경고</span>
    </div>`, '#a855f7');

  requestAnimationFrame(()=>{
    const cv=content.querySelector('#cv-elliott');
    if(!cv) return;
    const chart=new CandleChart(cv,prices);
    const ma20=calcMA(prices,20);
    chart.addLine(ma20,'#94a3b8');

    // 파동 포인트 시뮬레이션
    const waveIdx=[5,15,30,42,52,65,75];
    const labels=['1','2','3','4','5','a','b'];
    const colors=['#60a5fa','#3b82f6','#1d4ed8','#7c3aed','#a855f7','#ef4444','#f59e0b'];
    waveIdx.forEach((xi,i)=>{
      if(xi<prices.length) chart.addWaveLabel(xi, labels[i], colors[i]);
    });

    // 피보나치 레벨
    const lo=prices[0].l, hi=prices.slice(0,55).reduce((m,p)=>Math.max(m,p.h),0);
    [38.2,61.8].forEach(lvl=>{
      const y=hi-(hi-lo)*lvl/100;
      chart.addHLine(y,'#a855f7',[3,3],`Fib ${lvl}%`);
    });
    chart.draw();
  });
}

// ⑦ 종합 신호
function renderSummary(content, state) {
  const c = state.company;
  const prices = genPrices(80, c.start, 43, c.scenario);
  const ma20=calcMA(prices,20), ma60=calcMA(prices,60);
  const rsi=calcRSI(prices);
  const {macd,signal}=calcMACD(prices);
  const {upper,lower}=calcBB(prices);

  const lastC=prices[prices.length-1].c;
  const lm20=ma20[ma20.length-1], lm60=ma60[ma60.length-1];
  const lRsi=rsi.filter(v=>v!=null).slice(-1)[0];
  const lMacd=macd.filter(v=>v!=null).slice(-1)[0];
  const lSig=signal.filter(v=>v!=null).slice(-1)[0];
  const lUp=upper.filter(v=>v!=null).slice(-1)[0];
  const lLo=lower.filter(v=>v!=null).slice(-1)[0];
  const bbPct=(lastC-lLo)/(lUp-lLo);

  const signals=[
    {name:'추세(MA정배열)',  bull:lm20>lm60, score:lm20>lm60?1:-1},
    {name:'가격 vs MA20',   bull:lastC>lm20, score:lastC>lm20?1:-1},
    {name:'RSI',            bull:lRsi<50,    score:lRsi<30?2:lRsi>70?-2:lRsi<50?0.5:-0.5},
    {name:'MACD',           bull:lMacd>lSig, score:lMacd>lSig?1:-1},
    {name:'볼린저밴드 위치', bull:bbPct<0.5,  score:bbPct<0.2?2:bbPct>0.8?-2:0},
  ];
  const total=signals.reduce((s,sg)=>s+sg.score,0);
  const opinion=total>=2?'매수 우세':total<=-2?'매도 우세':'중립';
  const opColor=total>=2?'#16a34a':total<=-2?'#dc2626':'#f59e0b';

  content.innerHTML=card(`${c.name} 기술적 분석 종합 리포트`, 'fa-solid fa-file-chart-column', `
    ${info(`5개 기술적 지표를 종합해 현재 매수/매도/중립 신호를 판단합니다. 단일 지표가 아닌 복수 지표의 방향 일치도를 보는 것이 핵심입니다.`,'#0f172a')}
    <canvas id="cv-summary" style="width:100%;height:280px;display:block;border-radius:8px;border:1px solid #e2e8f0;margin-bottom:16px;"></canvas>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:16px;">
      ${signals.map(sg=>`
        <div style="background:#f8fafc;border-radius:8px;padding:12px;border-left:3px solid ${sg.score>0?'#22c55e':sg.score<0?'#ef4444':'#94a3b8'};">
          <div style="font-size:0.72rem;color:#64748b;margin-bottom:4px;">${sg.name}</div>
          <div style="font-size:0.88rem;font-weight:700;color:${sg.score>0?'#16a34a':sg.score<0?'#dc2626':'#f59e0b'};">
            ${sg.score>0?'↑ 강세':'↓ 약세'}
          </div>
        </div>`).join('')}
    </div>
    <div style="padding:18px;border-radius:10px;border:2px solid ${opColor};background:${opColor}10;text-align:center;">
      <div style="font-size:0.75rem;color:#64748b;margin-bottom:6px;">종합 기술적 의견</div>
      <div style="font-size:1.4rem;font-weight:800;color:${opColor};">${opinion}</div>
      <div style="font-size:0.78rem;color:#475569;margin-top:4px;">
        종합 스코어: ${total.toFixed(1)} | 기준: +2이상=매수우세, -2이하=매도우세
      </div>
    </div>
    <div style="margin-top:14px;padding:12px;background:#f8fafc;border-radius:8px;font-size:0.78rem;color:#475569;line-height:1.65;border:1px solid #e2e8f0;">
      ⚠️ 본 분석은 시뮬레이션 데이터 기반 교육용 리포트입니다. 실제 투자 결정은 추가적인 기본적 분석과 리스크 관리를 병행하세요.
    </div>`, '#0f172a');

  requestAnimationFrame(()=>{
    const cv=content.querySelector('#cv-summary');
    if(!cv) return;
    const chart=new CandleChart(cv,prices);
    chart.addLine(ma20,'#2563eb');
    chart.addLine(ma60,'#ef4444');
    chart.addBand(upper,lower,'#94a3b8');
    chart.draw();
  });
}

// ── 메인 진입점 ──────────────────────────────────────────────────────────────
export function technicalChartView(container) {
  const state = { selected:0, company:{name:'삼성전자',ticker:'005930.KS',sector:'반도체·IT',scenario:'trend_up',start:71000}, pat:0 };

  const TABS = ['① 기업 선정','② 추세분석','③ 이동평균','④ 캔들패턴','⑤ 보조지표','⑥ 엘리어트파동','⑦ 종합리포트'];

  const renders = [
    c=>renderStockSelect(c,state),
    c=>renderTrend(c,state),
    c=>renderMA(c,state),
    c=>renderCandle(c,state),
    c=>renderIndicators(c,state),
    c=>renderElliott(c,state),
    c=>renderSummary(c,state),
  ];

  container.innerHTML = tabShell(
    '기술적 분석 실습',
    '기업 선정부터 추세·이동평균·캔들패턴·보조지표·엘리어트파동·종합리포트까지 단계별로 실습합니다.',
    TABS
  );

  container.querySelectorAll('.tc-tab').forEach((btn,i)=>{
    btn.addEventListener('click',()=>activateTab(container,i,renders));
  });

  renders[0](container.querySelector('#tc-content'));
}
