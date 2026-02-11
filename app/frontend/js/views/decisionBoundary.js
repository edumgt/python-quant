import { apiGet } from '../api.js';

export function decisionBoundaryView(container) {
  container.innerHTML = `
    <section class="card">
      <h2>Decision Boundary</h2>
      <button class="run" id="dbRun">이미지 생성</button>
      <div id="dbArea"></div>
    </section>
  `;

  container.querySelector('#dbRun').addEventListener('click', async () => {
    const result = await apiGet('/api/ml/decision-boundary');
    container.querySelector('#dbArea').innerHTML = `<img class="preview" src="data:image/png;base64,${result.image_base64}" alt="decision boundary" />`;
  });
}
