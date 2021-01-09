import PlantChart from './plant-chart.js'
import App from './app.js';

async function start() {
  const app = new App({ container: document.getElementById('app') });
  await app.render();
}

start();
