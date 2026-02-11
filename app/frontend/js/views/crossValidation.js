import { apiPost } from '../api.js';

export function crossValidationView(container) {
  container.innerHTML = `
    <section class="card">
      <h2>Cross Validation</h2>
      <label>샘플 수<input id="cvSamples" type="number" value="1000" /></label>
      <label>특성 수<input id="cvFeatures" type="number" value="10" /></label>
      <label>Fold 수<input id="cvFold" type="number" value="5" /></label>
      <button class="run" id="cvRun">실행</button>
      <pre id="cvResult">결과를 기다리는 중...</pre>
    </section>
  `;

  container.querySelector('#cvRun').addEventListener('click', async () => {
    const payload = {
      n_samples: Number(container.querySelector('#cvSamples').value),
      n_features: Number(container.querySelector('#cvFeatures').value),
      cv: Number(container.querySelector('#cvFold').value),
    };
    const result = await apiPost('/api/ml/cross-validation', payload);
    container.querySelector('#cvResult').textContent = JSON.stringify(result, null, 2);
  });
}
