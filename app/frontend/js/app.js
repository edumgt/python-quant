import { homeView } from './views/home.js';
import { crossValidationView } from './views/crossValidation.js';
import { decisionBoundaryView } from './views/decisionBoundary.js';
import { randomForestView } from './views/randomForest.js';
import { kmeansView } from './views/kmeans.js';
import { svmView } from './views/svm.js';
import { mlpView } from './views/mlp.js';
import { linearRegressionView } from './views/linearRegression.js';
import { sentimentView } from './views/sentiment.js';
import { opencvView } from './views/opencv.js';
import { huggingfaceView } from './views/huggingface.js';

const menu = document.querySelector('#menu');
const app = document.querySelector('#app');

const routes = {
  '🏠 홈': () => { app.innerHTML = homeView(); attachHomeCardListeners(); },
  'Cross Validation': () => crossValidationView(app),
  'Decision Boundary': () => decisionBoundaryView(app),
  'Random Forest': () => randomForestView(app),
  'KMeans': () => kmeansView(app),
  'SVM': () => svmView(app),
  'MLP Neural Net': () => mlpView(app),
  'Regression': () => linearRegressionView(app),
  'NLP Classify': () => sentimentView(app),
  'OpenCV': () => opencvView(app),
  'HuggingFace': () => huggingfaceView(app),
};

let activeBtn = null;

Object.entries(routes).forEach(([name, render]) => {
  const button = document.createElement('button');
  button.textContent = name;
  button.addEventListener('click', () => {
    if (activeBtn) activeBtn.classList.remove('active');
    button.classList.add('active');
    activeBtn = button;
    render();
  });
  menu.appendChild(button);
});

function attachHomeCardListeners() {
  document.querySelectorAll('.module-card[data-route]').forEach(card => {
    card.addEventListener('click', () => {
      const routeName = card.dataset.route;
      const btn = [...menu.querySelectorAll('button')].find(b => b.textContent === routeName);
      if (btn) btn.click();
    });
  });
}

// Default: home
menu.querySelector('button').click();

