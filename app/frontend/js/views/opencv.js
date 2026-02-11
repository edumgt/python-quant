import { apiPost } from '../api.js';

export function opencvView(container) {
  container.innerHTML = `
    <section class="card">
      <h2>OpenCV Circle Animation</h2>
      <label>너비<input id="cvWidth" type="number" value="512" /></label>
      <label>높이<input id="cvHeight" type="number" value="512" /></label>
      <button class="run" id="ocvRun">영상 생성</button>
      <div id="ocvArea"></div>
    </section>
  `;

  container.querySelector('#ocvRun').addEventListener('click', async () => {
    const payload = {
      width: Number(container.querySelector('#cvWidth').value),
      height: Number(container.querySelector('#cvHeight').value),
    };
    const result = await apiPost('/api/cv/circle-animation', payload);
    container.querySelector('#ocvArea').innerHTML = `<video class="preview" controls src="${result.video_url}"></video>`;
  });
}
