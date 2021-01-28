import fetchChartData from './lib/fetch-chart-data.js'

const THRESHOLD_COLORS = {
  moist: '#4e7b8a',
  dry: '#755845',
  'very-dry': '#9c8870',
};

export default class PlantChart {
  constructor({ el, configFetcher }) {
    this.el = el;
    this.configFetcher = configFetcher;
    this.context = el.querySelector('#chart-canvas').getContext('2d');
  }
  
  setParameters({ start, end, resolution }) {
    if (start) this.start = start;
    if (end) this.end = end;
    if (resolution) this.resolution = resolution;
  }
  
  needsFetch() {
    return !this.hasFetched ||
      this.start !== this.lastFetchedData?.start ||
      this.end !== this.lastFetchedData?.end ||
      this.resolution !== this.lastFetchedData?.resolution;
  }
  
  async ensureData() {
    if (!this.needsFetch()) {
      return;
    }
    this.hasFetched = true;
    const [{ chartData, resolution }, { thresholds }] = await Promise.all([
      fetchChartData(this.start, this.end, this.resolution),
      this.configFetcher.fetch()
    ]);
    this.lastFetchedData = {
      start: this.start,
      end: this.end,
      resolution: resolution,
    };
    this.chartData = chartData;
    this.resolution = resolution == 'minute' ? 'hour' : resolution;
    this.thresholds = thresholds;
  }

  getAnnotations() {
    return Object.keys(this.thresholds).map(state => ({
      type: 'line',
      mode: 'horizontal',
      scaleID: 'y-axis-0',
      value: this.thresholds[state],
      borderColor: THRESHOLD_COLORS[state],
      borderWidth: 2,
    }));
  }
  
  getChartConfig() {
    return {
      type: 'line',
      options: {
        maintainAspectRatio: false,
        adapters: {
          time: window.moment,
        },
        legend: {
          display: false,
        },
        scales: {
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'moisture level',
              },
              ticks: {
                min: this.chartData.datasets[0].length ? null : 1000,
                max: this.chartData.datasets[0].length ? null : 2000,
              },
            },
          ],
          xAxes: [
            {
              type: 'time',
              time: {
                unit: this.resolution,
                displayFormats: {
                  day: 'YYYY-MM-D',
                  hour: 'YYYY-MM-D:h:mm:ss',
                },
              },
            },
          ],
        },
        annotation: {
          annotations: this.getAnnotations(),
        }
      },
      data: this.chartData,
    };
  }
  
  async update() {
    await this.ensureData();
    this.chart = new Chart(this.context, this.getChartConfig());
  }
  
  async attach() {
    await this.update();
  }
}
