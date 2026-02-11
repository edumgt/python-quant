import { homeView } from './views/home.js';
import { crossValidationView } from './views/crossValidation.js';
import { decisionBoundaryView } from './views/decisionBoundary.js';
import { randomForestView } from './views/randomForest.js';
import { opencvView } from './views/opencv.js';
import { huggingfaceView } from './views/huggingface.js';

const menu = document.querySelector('#menu');
const app = document.querySelector('#app');

const routes = {
  홈: () => { app.innerHTML = homeView(); },
  CrossValidation: () => crossValidationView(app),
  DecisionBoundary: () => decisionBoundaryView(app),
  RandomForest: () => randomForestView(app),
  OpenCV: () => opencvView(app),
  HuggingFace: () => huggingfaceView(app),
};

Object.entries(routes).forEach(([name, render]) => {
  const button = document.createElement('button');
  button.textContent = name;
  button.addEventListener('click', render);
  menu.appendChild(button);
});

routes['홈']();
