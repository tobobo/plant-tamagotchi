import parseQueryString from './parse-query-string.js';
import PlantChart from './plant-chart.js';
import StatusDisplay from './status-display.js';

export default class App {
  constructor({ container }) {
    this.container = container;
    this.statusDisplay = new StatusDisplay({ container: this.container.querySelector('#status') });
    this.chart = new PlantChart({ container: this.container.querySelector('#chart') });
    this.chart.setParameters(parseQueryString());
  }
  
  async render() {
    await Promise.all([this.statusDisplay.render(), this.chart.render()]); 
  }
}
