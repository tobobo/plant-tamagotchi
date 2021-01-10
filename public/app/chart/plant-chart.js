import fetchChartData from './lib/fetch-chart-data.js'

export default class PlantChart {
  constructor({ el }) {
    this.el = el;
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
    const { chartData, resolution } = await fetchChartData(this.start, this.end, this.resolution);
    this.lastFetchedData = {
      start: this.start,
      end: this.end,
      resolution: resolution,
    };
    this.chartData = chartData;
    this.resolution = resolution == 'minute' ? 'hour' : resolution;
  }
  
  getChartConfig() {
    return {
      type: 'line',
      options: {
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
                labelString: 'dryness',
              },
              ticks: {
                min: 1400,
                max: 2000,
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
      },
      data: this.chartData,
    };
  }
  
  async update() {
    await this.ensureData();
    if (!this.chart) {
      this.chart = new Chart(this.context, this.getChartConfig());
    } else {
      const { data, options } = this.getChartConfig();
      this.chart.data = data;
      this.chart.options = options;
      this.chart.update();
    }
  }
  
  async attach() {
    await this.update();
  }
}
