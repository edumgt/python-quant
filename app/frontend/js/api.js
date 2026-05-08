const BASE = '';

// Backward-compat helpers used by legacy views
export async function apiGet(path) { return apiFetch(path); }
export async function apiPost(path, body) { return apiFetch(path, { method: 'POST', body: JSON.stringify(body) }); }
export async function withLoading(btn, fn) {
  btn.disabled = true;
  const orig = btn.textContent;
  btn.textContent = '실행 중...';
  try { return await fn(); } finally { btn.disabled = false; btn.textContent = orig; }
}
export function renderError(msg) { return `<p style="color:#ef4444; margin-top:12px;">오류: ${msg}</p>`; }
export function renderImage(src) { return src ? `<img src="${src}" style="width:100%; border-radius:8px; margin-top:16px;"/>` : ''; }
export function renderMetrics(m) {
  if (!m) return '';
  return `<div style="display:flex; flex-wrap:wrap; gap:12px; margin-top:16px;">
    ${Object.entries(m).map(([k, v]) => `
      <div class="metric-box">
        <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; margin-bottom:4px;">${k.replace(/_/g,' ')}</div>
        <div style="font-size:1rem; font-weight:700; color:#3b82f6;">${typeof v === 'number' ? v.toFixed(4) : v}</div>
      </div>`).join('')}
  </div>`;
}

export async function apiFetch(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

export const api = {
  health:           ()      => apiFetch('/api/health'),
  crossValidation:  (body)  => apiFetch('/api/ml/cross-validation',        { method: 'POST', body: JSON.stringify(body) }),
  decisionBoundary: ()      => apiFetch('/api/ml/decision-boundary'),
  randomForest:     (body)  => apiFetch('/api/ml/random-forest',           { method: 'POST', body: JSON.stringify(body) }),
  kmeans:           (body)  => apiFetch('/api/ml/kmeans',                  { method: 'POST', body: JSON.stringify(body) }),
  svm:              (body)  => apiFetch('/api/ml/svm',                     { method: 'POST', body: JSON.stringify(body) }),
  mlp:              (body)  => apiFetch('/api/ml/mlp',                     { method: 'POST', body: JSON.stringify(body) }),
  linearRegression: (body)  => apiFetch('/api/ml/linear-regression',       { method: 'POST', body: JSON.stringify(body) }),
  textClassify:     (body)  => apiFetch('/api/nlp/text-classify',          { method: 'POST', body: JSON.stringify(body) }),
  opencv:           (body)  => apiFetch('/api/cv/circle-animation',        { method: 'POST', body: JSON.stringify(body) }),
  huggingface:      (body)  => apiFetch('/api/genai/text-to-image',        { method: 'POST', body: JSON.stringify(body) }),
  cnnTimeseries:    (body)  => apiFetch('/api/dl/cnn-timeseries',          { method: 'POST', body: JSON.stringify(body) }),
  lstm:             (body)  => apiFetch('/api/dl/lstm-predictor',          { method: 'POST', body: JSON.stringify(body) }),
  transformer:      (body)  => apiFetch('/api/dl/transformer-timeseries',  { method: 'POST', body: JSON.stringify(body) }),
  backtest:         (body)  => apiFetch('/api/quant/backtest',             { method: 'POST', body: JSON.stringify(body) }),
  portfolio:        (body)  => apiFetch('/api/quant/portfolio',            { method: 'POST', body: JSON.stringify(body) }),
  risk:             (body)  => apiFetch('/api/quant/risk',                 { method: 'POST', body: JSON.stringify(body) }),
  pipeline:         (body)  => apiFetch('/api/quant/pipeline',             { method: 'POST', body: JSON.stringify(body) }),
  macroRealtime:    (body)  => apiFetch('/api/macro/realtime',              { method: 'POST', body: JSON.stringify(body) }),
  macroSimulation:  (body)  => apiFetch('/api/macro/simulation',            { method: 'POST', body: JSON.stringify(body) }),
  industryPorter:   (body)  => apiFetch('/api/industry/porter',             { method: 'POST', body: JSON.stringify(body) }),
  industrySector:   (body)  => apiFetch('/api/industry/sector',             { method: 'POST', body: JSON.stringify(body) }),
  industryLifecycle:(body)  => apiFetch('/api/industry/lifecycle',          { method: 'POST', body: JSON.stringify(body) }),
};
