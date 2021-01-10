import PlantChart from './app/chart/plant-chart.js'
import App from './app/app.js';

async function start() {
  const app = new App({ el: document.getElementById('app') });
  await app.attach();
}

start();
