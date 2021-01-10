import PlantChart from './plant-chart.js';

export default class ChartControl {
  constructor({ container }) {
    this.container = container;
    this.chart = new PlantChart({ container: this.container.querySelector('#chart') });
    this.showDataButton = this.container.querySelector('#show_data');
    this.resolutionSelect = this.container.querySelector('#resolution');
    this.loadingStateIndicator = this.container.querySelector('#loading_state');
  }
  
  setParameters(...args) {
    this.chart.setParameters(...args);
  }
  
  async onShowClick(e) {
    e.preventDefault();
    this.loadingStateIndicator.removeAttribute('hidden');
    if (!this.chartAttached) {
      await this.chart.attach();
      this.chartAttached = true;
    } else {
      await this.chart.update();
    }
    this.loadingStateIndicator.setAttribute('hidden', true);
  }
  
  onResolutionChange(e) {
    e.preventDefault();
    this.chart.setParameters({ resolution: e.target.value });
  }
  
  bindEvents() {
    this.showDataButton.addEventListener('click', this.onShowClick.bind(this));
    this.resolutionSelect.addEventListener('change', this.onResolutionChange.bind(this));
  }
  
  attach() {
    this.bindEvents();
  }
}
