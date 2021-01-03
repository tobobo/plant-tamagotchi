import renderChart from './render-chart.js'
import parseQueryString from './parse-query-string.js'

async function start() {
  const appElement = document.getElementById('app');
  const chartContainer = document.createElement('div');
  chartContainer.style.width = '800px';
  chartContainer.style.height = '600px';
  appElement.appendChild(chartContainer);
  const canvas = document.createElement('canvas');
  canvas.id = 'chart';
  chartContainer.appendChild(canvas);
  const context = canvas.getContext('2d');

  const { start, end, resolution } = parseQueryString();
  renderChart(context, start, end, resolution);
}

start();
