import { homeView }            from './views/home.js';
import { crossValidationView } from './views/crossValidation.js';
import { decisionBoundaryView } from './views/decisionBoundary.js';
import { randomForestView }    from './views/randomForest.js';
import { kmeansView }          from './views/kmeans.js';
import { svmView }             from './views/svm.js';
import { mlpView }             from './views/mlp.js';
import { linearRegressionView } from './views/linearRegression.js';
import { textClassifyView }    from './views/textClassify.js';
import { opencvView }          from './views/opencv.js';
import { cnnTimeseriesView }   from './views/cnnTimeseries.js';
import { lstmView }            from './views/lstm.js';
import { transformerView }     from './views/transformer.js';
import { backtestView }        from './views/backtest.js';
import { portfolioView }       from './views/portfolio.js';
import { pipelineView }        from './views/pipeline.js';
import { riskView }            from './views/risk.js';
import { huggingfaceView }     from './views/huggingface.js';
import { macroRealtimeView }    from './views/macroRealtime.js';
import { macroSimulationView }  from './views/macroSimulation.js';
import { industryAnalysisView } from './views/industryAnalysis.js';
import { financialStatementView } from './views/financialStatement.js';
import { dartCompanySearchView } from './views/dartCompanySearch.js';
import { groupNetworkView }      from './views/groupNetwork.js';
import { valuationView }        from './views/valuation.js';
import { technicalChartView }  from './views/technicalChart.js';
import { financialKnowledgeView } from './views/financialKnowledge.js';
import { investmentTreeView }   from './views/investmentTree.js';
import { quizHomeView, quizDayView } from './views/quiz.js';
import { api }                 from './api.js';

const app        = document.getElementById('app');
const breadcrumb = document.getElementById('breadcrumb');

const routes = {
  'home':              { label: '홈',                     render: () => homeView(app, navigate) },
  'cross-validation':  { label: 'Cross Validation',       render: () => crossValidationView(app) },
  'decision-boundary': { label: 'Decision Boundary',      render: () => decisionBoundaryView(app) },
  'random-forest':     { label: 'Random Forest',          render: () => randomForestView(app) },
  'kmeans':            { label: 'KMeans 클러스터링',       render: () => kmeansView(app) },
  'svm':               { label: 'SVM 분류기',             render: () => svmView(app) },
  'mlp':               { label: 'MLP 신경망',             render: () => mlpView(app) },
  'linear-regression': { label: '선형 회귀',              render: () => linearRegressionView(app) },
  'text-classify':     { label: '텍스트 분류 (TF-IDF)',   render: () => textClassifyView(app) },
  'opencv':            { label: 'OpenCV 애니메이션',      render: () => opencvView(app) },
  'cnn-timeseries':    { label: '1D CNN 시계열',          render: () => cnnTimeseriesView(app) },
  'lstm':              { label: 'LSTM 예측기',            render: () => lstmView(app) },
  'transformer':       { label: 'Transformer',            render: () => transformerView(app) },
  'backtest':          { label: '백테스트 엔진',          render: () => backtestView(app) },
  'portfolio':         { label: '포트폴리오 최적화',      render: () => portfolioView(app) },
  'pipeline':          { label: '퀀트 파이프라인',        render: () => pipelineView(app) },
  'risk':              { label: '리스크 분석 (VaR)',       render: () => riskView(app) },
  'huggingface':       { label: 'HuggingFace 이미지 생성', render: () => huggingfaceView(app) },
  'macro-realtime':    { label: '거시경제현황 1 (실시간)',    render: () => macroRealtimeView(app) },
  'macro-simulation':  { label: '거시경제현황 2 (시뮬레이션)', render: () => macroSimulationView(app) },
  'industry-analysis': { label: '산업 경쟁력 분석',           render: () => industryAnalysisView(app) },
  'financial-statement': { label: '재무제표분석',              render: () => financialStatementView(app) },
  'dart-company-search': { label: 'DART 상장기업 검색',        render: () => dartCompanySearchView(app) },
  'group-network':       { label: '그룹사 계열사 네트워크',      render: () => groupNetworkView(app) },
  'valuation':           { label: '밸류에이션 실습',            render: () => valuationView(app) },
  'technical-chart':     { label: '기술적 분석 실습',            render: () => technicalChartView(app) },
  'financial-knowledge': { label: '금융상품·자산배분',           render: () => financialKnowledgeView(app) },
  'investment-tree':     { label: '투자 성향 분석',              render: () => investmentTreeView(app) },
  'quiz-home':           { label: '퀴즈 · 통합 모의고사',        render: () => quizHomeView(app, navigate) },
  'quiz-day-1':          { label: '통합 모의고사 응시',          render: () => quizDayView(app, 1, navigate) },
};

let currentView = null;

function navigate(view) {
  const route = routes[view] || routes['home'];
  currentView = view;

  // Update active sidebar link
  document.querySelectorAll('.sidebar-link').forEach(a => {
    a.classList.toggle('active', a.dataset.view === view);
  });

  // Update breadcrumb
  if (breadcrumb) breadcrumb.textContent = route.label;

  route.render();

  if (typeof closeSidebar === 'function') closeSidebar();
}

// Wire up sidebar links
document.querySelectorAll('.sidebar-link[data-view]').forEach(a => {
  a.addEventListener('click', (e) => {
    e.preventDefault();
    navigate(a.dataset.view);
  });
});

document.querySelectorAll('[data-view="home"].brand').forEach((button) => {
  button.addEventListener('click', () => navigate('home'));
});

// Health check
async function checkHealth() {
  const dot  = document.getElementById('health-dot');
  const text = document.getElementById('health-text');
  try {
    await api.health();
    if (dot)  dot.style.background  = '#22c55e';
    if (text) text.textContent = '백엔드 연결됨';
  } catch {
    if (dot)  dot.style.background  = '#ef4444';
    if (text) text.textContent = '백엔드 오프라인';
  }
}

checkHealth();
setInterval(checkHealth, 30000);

// Boot
navigate('home');
