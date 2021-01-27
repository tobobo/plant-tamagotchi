import parseQueryString from './lib/parse-query-string.js';
import ChartControl from './chart/chart-control.js';
import StatusDisplay from './status/status-display.js';
import ConfigFetcher from './lib/config-fetcher.js';

export default class App {
  constructor({ el }) {
    this.el = el;

    const configFetcher = new ConfigFetcher();

    this.statusDisplay = new StatusDisplay({ el: this.el.querySelector('#status') });
    this.chartControl = new ChartControl({ el: this.el.querySelector('#chart-control'), configFetcher });
    this.chartControl.setParameters(parseQueryString());
  }
  
  attach() {
    this.statusDisplay.attach();
    this.chartControl.attach();
  }
}
