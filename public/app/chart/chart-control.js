import PlantChart from './plant-chart.js';

export default class ChartControl {
  constructor({ el, configFetcher }) {
    this.el = el;
    this.chart = new PlantChart({ el: this.el.querySelector('#chart'), configFetcher });
    this.showDataButton = this.el.querySelector('#show_data');
    this.resolutionSelect = this.el.querySelector('#resolution');
    this.startDateInput = this.el.querySelector('#start');
    this.loadingStateIndicator = this.el.querySelector('#loading_state');
  }
  
  setParameters(...args) {
    this.chart.setParameters(...args);
  }
  
  async onShowClick(e) {
    e.preventDefault();
    this.showDataButton.setAttribute('hidden', '');
    this.loadingStateIndicator.removeAttribute('hidden');
    try {
      if (!this.chartAttached) {
        await this.chart.attach();
        this.chartAttached = true;
      } else {
        await this.chart.update();
      }
    } catch (e) {
      this.showDataButton.removeAttribute('hidden');
      // show an error message or something
    }
    this.loadingStateIndicator.setAttribute('hidden', '');
  }
  
  showOrHideButton() {
    if (this.chart.needsFetch()) {
      this.showDataButton.removeAttribute('hidden');
    } else {
      this.showDataButton.setAttribute('hidden', '');
    }
  }
  
  onStartDateChange(e) {
    e.preventDefault();
    this.chart.start = e.target.value;
    this.showOrHideButton();
  }
  
  onResolutionChange(e) {
    e.preventDefault();
    this.chart.resolution = e.target.value;
    this.showOrHideButton();
  }
  
  initializeDatePickers() {
    const now = new Date();
    this.startDateInput.setAttribute('max', now.toISOString().split('T')[0])
    const startDate = this.chart.start ?
      new Date(this.chart.start) :
      (() => {
        const twoWeeksInMs = 14 * 24 * 60 * 60 * 1000;
        return new Date(now.getTime() - twoWeeksInMs);
      })();
    const startDateString = startDate.toISOString().split('T')[0];
    this.startDateInput.value = startDateString;
    this.chart.start = startDateString;
  }
  
  bindEvents() {
    this.showDataButton.addEventListener('click', this.onShowClick.bind(this));
    this.startDateInput.addEventListener('change', this.onStartDateChange.bind(this));
    this.resolutionSelect.addEventListener('change', this.onResolutionChange.bind(this));
  }
  
  attach() {
    this.bindEvents();
    this.initializeDatePickers();
  }
}
