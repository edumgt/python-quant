import { apiPost } from '../api.js';

export function randomForestView(container) {
  container.innerHTML = `
    <section class="card">
      <h2>Random Forest</h2>
      <label>테스트 비율<input id="rfTest" type="number" step="0.1" value="0.3" /></label>
      <button class="run" id="rfRun">평가 실행</button>
      <pre id="rfResult"></pre>
    </section>
  `;

  container.querySelector('#rfRun').addEventListener('click', async () => {
    const payload = { test_size: Number(container.querySelector('#rfTest').value) };
    const result = await apiPost('/api/ml/random-forest', payload);
    container.querySelector('#rfResult').textContent = JSON.stringify(result, null, 2);
  });
}
