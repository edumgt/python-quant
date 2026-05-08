import { api } from '../api.js';

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function dartCompanySearchView(container) {
  container.innerHTML = `
    <div style="margin-bottom:28px;">
      <h1 style="font-size:1.45rem; font-weight:760; color:#131722; margin-bottom:8px;">
        <i class="fa-solid fa-magnifying-glass-chart"></i> DART 상장기업 검색
      </h1>
      <p style="font-size:0.88rem; color:#6b7280; line-height:1.65;">
        전자공시시스템의 회사코드 목록에서 상장기업명을 검색해 DART 고유번호, 종목코드, 표시용 티커를 확인합니다.
      </p>
    </div>

    <section class="dart-search-panel">
      <div class="dart-search-row">
        <div>
          <label class="param-label">상장기업명</label>
          <input id="dart-company-name" type="text" value="삼성전자" class="param-input" placeholder="예: 삼성전자, 카카오, 현대차" />
        </div>
        <button class="run-btn" id="dart-search-run">
          <i class="fa-solid fa-magnifying-glass"></i> 검색
        </button>
      </div>
      <div class="dart-help">
        서버 환경변수 <code>DART_API_KEY</code> 또는 <code>OPENDART_API_KEY</code>가 설정되지 않으면 검색이 제한될 수 있습니다.
      </div>
      <div id="dart-search-result" style="margin-top:18px;"></div>
    </section>
  `;

  const input = container.querySelector('#dart-company-name');
  const run = container.querySelector('#dart-search-run');
  const result = container.querySelector('#dart-search-result');

  const search = async () => {
    const companyName = input.value.trim();
    if (!companyName) {
      result.innerHTML = '<p style="color:#f23645;">회사명을 입력하세요.</p>';
      return;
    }

    run.disabled = true;
    run.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 검색 중';
    result.innerHTML = '<p style="color:#6b7280;">DART 회사코드 목록을 확인하는 중입니다...</p>';
    try {
      const data = await api.dartCompanySearch({ company_name: companyName, limit: 12 });
      if (!data.results.length) {
        result.innerHTML = `<p style="color:#6b7280;">'${escapeHtml(companyName)}'에 해당하는 상장기업을 찾지 못했습니다.</p>`;
        return;
      }

      result.innerHTML = `
        <div class="dart-result-summary">
          <strong>${escapeHtml(data.query)}</strong> 검색 결과 ${data.count}건
          <span>${escapeHtml(data.source)}</span>
        </div>
        <div class="dart-result-grid">
          ${data.results.map(item => `
            <article class="dart-result-card">
              <div class="dart-result-title">${escapeHtml(item.corp_name)}</div>
              <div class="dart-ticker">${escapeHtml(item.display)}</div>
              <dl>
                <div><dt>DART 고유번호</dt><dd>${escapeHtml(item.corp_code)}</dd></div>
                <div><dt>종목코드</dt><dd>${escapeHtml(item.stock_code)}</dd></div>
                <div><dt>Yahoo 티커</dt><dd>${escapeHtml(item.ticker)}</dd></div>
                <div><dt>수정일</dt><dd>${escapeHtml(item.modify_date)}</dd></div>
              </dl>
              <div class="dart-copy-row">
                <button type="button" data-copy="${escapeHtml(item.ticker)}" class="copy-btn">
                  <i class="fa-regular fa-copy"></i> 티커 복사
                </button>
                <button type="button" data-copy="${escapeHtml(item.corp_code)}" class="copy-btn">
                  <i class="fa-regular fa-copy"></i> DART 번호 복사
                </button>
              </div>
            </article>
          `).join('')}
        </div>
        <div class="dart-notes">
          ${data.notes.map(note => `<p>${escapeHtml(note)}</p>`).join('')}
        </div>
      `;

      result.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', async () => {
          await navigator.clipboard.writeText(button.dataset.copy || '');
          const original = button.innerHTML;
          button.innerHTML = '<i class="fa-solid fa-check"></i> 복사됨';
          setTimeout(() => { button.innerHTML = original; }, 900);
        });
      });
    } catch (error) {
      result.innerHTML = `
        <div class="dart-error">
          <strong>검색 실패</strong>
          <p>${escapeHtml(error.message)}</p>
          <p>OpenDART 인증키를 발급받아 서버 실행 환경에 <code>DART_API_KEY</code>로 설정한 뒤 다시 실행하세요.</p>
        </div>`;
    } finally {
      run.disabled = false;
      run.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> 검색';
    }
  };

  run.addEventListener('click', search);
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') search();
  });
}
