import fetchChartData from './fetch-chart-data.js'

export default class PlantChart {
  constructor({ container }) {
    this.container = container;
    this.context = container.querySelector('#chart-canvas').getContext('2d');
  }
  
  setParameters({ start, end, resolution }) {
    this.start = start;
    this.end = end;
    this.resolution = resolution;
  }
  
  async fetchData() {
    this.chartData = await fetchChartData(this.start, this.end, this.resolution);
  }
  
  async render() {
    if (!this.chartData) {
      await this.fetchData();
    }

    new Chart(this.context, {
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
                unit: 'hour',
                displayFormats: {
                  hour: 'YYYY-MM-D:h:mm:ss'
                },
              },
            },
          ],
        },
      },
      data: this.chartData,
    });
  }
}
