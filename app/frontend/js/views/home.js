export function homeView(container, navigate) {
  const modules = [
    { icon: '📊', name: 'Cross Validation',      tag: 'ML · Scikit-learn',    view: 'cross-validation' },
    { icon: '🗺️', name: 'Decision Boundary',    tag: 'ML · Visualization',   view: 'decision-boundary' },
    { icon: '🌳', name: 'Random Forest',          tag: 'ML · Ensemble',        view: 'random-forest' },
    { icon: '🔵', name: 'KMeans 클러스터링',      tag: 'ML · Clustering',      view: 'kmeans' },
    { icon: '⚔️', name: 'SVM 분류기',            tag: 'ML · Classification',  view: 'svm' },
    { icon: '🧠', name: 'MLP 신경망',             tag: 'ML · Neural Network',  view: 'mlp' },
    { icon: '📈', name: '선형 회귀',              tag: 'ML · Regression',      view: 'linear-regression' },
    { icon: '💬', name: '텍스트 분류 (TF-IDF)',   tag: 'NLP · Text',           view: 'text-classify' },
    { icon: '🎥', name: 'OpenCV 애니메이션',      tag: 'CV · Video',           view: 'opencv' },
    { icon: '📡', name: '1D CNN 시계열',          tag: 'DL · CNN',             view: 'cnn-timeseries' },
    { icon: '🔁', name: 'LSTM 예측기',            tag: 'DL · RNN',             view: 'lstm' },
    { icon: '🤖', name: 'Transformer',            tag: 'DL · Attention',       view: 'transformer' },
    { icon: '📉', name: '백테스트 엔진',          tag: 'Quant · Strategy',     view: 'backtest' },
    { icon: '💼', name: '포트폴리오 최적화',      tag: 'Quant · Portfolio',    view: 'portfolio' },
    { icon: '🔬', name: '퀀트 파이프라인',        tag: 'Quant · Pipeline',     view: 'pipeline' },
    { icon: '⚠️', name: '리스크 분석 (VaR)',     tag: 'Quant · Risk',         view: 'risk' },
    { icon: '🎨', name: 'HuggingFace 이미지 생성', tag: 'GenAI · Diffusion',  view: 'huggingface' },
    { icon: '🌐', name: '거시경제현황 1 (실시간)',   tag: '거시경제 · yfinance', view: 'macro-realtime' },
    { icon: '📊', name: '거시경제현황 2 (시뮬레이션)', tag: '거시경제 · GBM',   view: 'macro-simulation' },
    { icon: '🏭', name: '산업 경쟁력 분석',          tag: 'Porter·섹터·SWOT', view: 'industry-analysis' },
  ];

  container.innerHTML = `
    <div style="margin-bottom:32px;">
      <h1 style="font-size:1.5rem; font-weight:700; color:#fff; margin-bottom:8px;">Python Quant Lab</h1>
      <p style="font-size:0.875rem; color:#94a3b8; line-height:1.6;">
        FastAPI 백엔드 + Vanilla JS 프론트엔드로 구성한 ML/DL/Quant 교육 실습 대시보드입니다.
        사이드바 또는 아래 카드에서 실습 모듈을 선택하세요.
      </p>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:16px; margin-bottom:32px;" id="home-grid">
      ${modules.map(m => `
        <div data-view="${m.view}" style="background:#1e293b; border-radius:12px; padding:20px 16px;
             cursor:pointer; border:1px solid #334155; transition:border-color 0.15s, transform 0.15s;"
             onmouseover="this.style.borderColor='#3b82f6';this.style.transform='translateY(-2px)'"
             onmouseout="this.style.borderColor='#334155';this.style.transform='translateY(0)'">
          <div style="font-size:1.75rem; margin-bottom:10px;">${m.icon}</div>
          <div style="font-size:0.825rem; font-weight:600; color:#e2e8f0; margin-bottom:4px;">${m.name}</div>
          <div style="font-size:0.7rem; color:#64748b;">${m.tag}</div>
        </div>`).join('')}
    </div>

    <div style="background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155;">
      <div style="font-size:0.75rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">API Endpoints</div>
      <pre style="font-size:0.75rem; color:#94a3b8; line-height:1.8; overflow-x:auto;">POST /api/ml/cross-validation
GET  /api/ml/decision-boundary
POST /api/ml/random-forest      POST /api/ml/kmeans
POST /api/ml/svm                POST /api/ml/mlp
POST /api/ml/linear-regression  POST /api/nlp/text-classify
POST /api/cv/circle-animation   POST /api/dl/cnn-timeseries
POST /api/dl/lstm-predictor     POST /api/dl/transformer-timeseries
POST /api/quant/backtest        POST /api/quant/portfolio
POST /api/quant/risk            POST /api/quant/pipeline
POST /api/genai/text-to-image</pre>
    </div>
  `;

  document.querySelectorAll('#home-grid [data-view]').forEach(card => {
    card.addEventListener('click', () => navigate(card.dataset.view));
  });
}
