export async function apiGet(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export async function apiPost(url, payload = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

/**
 * Run an API call while showing a loading state on the given button.
 * @param {HTMLButtonElement} btn
 * @param {() => Promise<any>} fn
 */
export async function withLoading(btn, fn) {
  const original = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> 실행 중…';
  try {
    return await fn();
  } finally {
    btn.disabled = false;
    btn.innerHTML = original;
  }
}

/** Render metric badges */
export function renderMetrics(items) {
  return `<div class="metrics">${items.map(([k, v]) => `<span class="metric-badge">${k}: <strong>${v}</strong></span>`).join('')}</div>`;
}

/** Render base64 image */
export function renderImage(b64) {
  return `<img class="preview" src="data:image/png;base64,${b64}" alt="result" />`;
}

/** Render error alert */
export function renderError(msg) {
  return `<div class="alert alert-error">⚠️ ${msg}</div>`;
}

