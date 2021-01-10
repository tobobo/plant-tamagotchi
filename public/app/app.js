import parseQueryString from './lib/parse-query-string.js';
import ChartControl from './chart/chart-control.js';
import StatusDisplay from './status/status-display.js';

export default class App {
  constructor({ container }) {
    this.container = container;
    this.statusDisplay = new StatusDisplay({ container: this.container.querySelector('#status') });
    this.chartControl = new ChartControl({ container: this.container.querySelector('#chart-control') });
    this.chartControl.setParameters(parseQueryString());
  }
  
  attach() {
    this.statusDisplay.attach();
    this.chartControl.attach();
  }
}
