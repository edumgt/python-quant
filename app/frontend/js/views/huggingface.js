import { apiPost } from '../api.js';

export function huggingfaceView(container) {
  container.innerHTML = `
    <section class="card">
      <h2>HuggingFace Diffusion (GPU)</h2>
      <label>Prompt<textarea id="hfPrompt" rows="4">A futuristic city skyline at sunset</textarea></label>
      <button class="run" id="hfRun">이미지 생성</button>
      <div id="hfArea"></div>
    </section>
  `;

  container.querySelector('#hfRun').addEventListener('click', async () => {
    const payload = { prompt: container.querySelector('#hfPrompt').value };
    try {
      const result = await apiPost('/api/genai/text-to-image', payload);
      container.querySelector('#hfArea').innerHTML = `<img class="preview" src="${result.image_url}" alt="diffusion result" />`;
    } catch (error) {
      container.querySelector('#hfArea').innerHTML = `<pre>${error.message}</pre>`;
    }
  });
}
