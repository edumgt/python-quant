export function homeView() {
  const modules = [
    { icon: '📊', name: 'Cross Validation', tag: 'ML · Scikit-learn', route: 'Cross Validation' },
    { icon: '🗺️', name: 'Decision Boundary', tag: 'ML · Visualization', route: 'Decision Boundary' },
    { icon: '🌳', name: 'Random Forest', tag: 'ML · Ensemble', route: 'Random Forest' },
    { icon: '🔵', name: 'KMeans', tag: 'ML · Clustering', route: 'KMeans' },
    { icon: '⚔️', name: 'SVM', tag: 'ML · Classification', route: 'SVM' },
    { icon: '🧠', name: 'MLP Neural Net', tag: 'DL · Neural Network', route: 'MLP Neural Net' },
    { icon: '📈', name: 'Regression', tag: 'ML · Regression', route: 'Regression' },
    { icon: '💬', name: 'NLP Classify', tag: 'NLP · Text', route: 'NLP Classify' },
    { icon: '🎥', name: 'OpenCV', tag: 'CV · Video', route: 'OpenCV' },
    { icon: '🎨', name: 'HuggingFace', tag: 'GenAI · Diffusion', route: 'HuggingFace' },
  ];

  const cards = modules.map(m => `
    <div class="module-card" data-route="${m.route}">
      <div class="icon">${m.icon}</div>
      <div class="name">${m.name}</div>
      <div class="tag">${m.tag}</div>
    </div>
  `).join('');

  return `
    <section class="card">
      <h2>🧠 Python ML/DL Education Lab</h2>
      <p class="desc">
        Python FastAPI 백엔드와 Vanilla JS 프론트엔드로 구성한 교육용 ML/DL 실습 대시보드입니다.
        아래 모듈 카드 또는 상단 메뉴에서 실습을 선택하세요.
        <br/><br/>
        An educational ML/DL lab with a Python FastAPI backend and Vanilla JS frontend.
        Select a module below or from the top navigation.
      </p>
      <div class="module-grid">${cards}</div>
    </section>

    <section class="card">
      <h2>📚 학습 순서 권장 / Recommended Learning Path</h2>
      <p class="desc">기초 ML → 앙상블 → 클러스터링 → SVM → 신경망 → 회귀 → NLP → OpenCV → 생성형 AI</p>
      <ol style="padding-left:20px; line-height:2; font-size:0.88rem; color:var(--text-muted);">
        <li><strong>Cross Validation</strong> — 모델 평가 기초</li>
        <li><strong>Decision Boundary</strong> — 2D 분류 경계 시각화</li>
        <li><strong>Random Forest</strong> — 앙상블 트리 분류기</li>
        <li><strong>KMeans Clustering</strong> — 비지도 클러스터링</li>
        <li><strong>SVM</strong> — 서포트 벡터 머신 (RBF/Linear/Poly)</li>
        <li><strong>MLP Neural Net</strong> — 다층 퍼셉트론 신경망</li>
        <li><strong>Linear/Poly Regression</strong> — 회귀 분석</li>
        <li><strong>NLP Text Classify</strong> — TF-IDF + 로지스틱 회귀 텍스트 분류</li>
        <li><strong>OpenCV Animation</strong> — 영상 생성</li>
        <li><strong>HuggingFace Diffusion</strong> — Stable Diffusion (GPU 필요)</li>
      </ol>
    </section>

    <section class="card">
      <h2>⚡ API 엔드포인트 / API Endpoints</h2>
      <pre style="font-size:0.78rem;">POST /api/ml/cross-validation
GET  /api/ml/decision-boundary
POST /api/ml/random-forest
POST /api/ml/kmeans
POST /api/ml/svm
POST /api/ml/mlp
POST /api/ml/linear-regression
POST /api/nlp/text-classify
POST /api/cv/circle-animation
POST /api/genai/text-to-image
GET  /api/health</pre>
    </section>
  `;
}

