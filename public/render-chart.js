import fetchChartData from './fetch-chart-data.js'

export default async function renderChart(context, start, end, resolution) {
  const chart = new Chart(context, {
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
    data: await fetchChartData(start, end, resolution),
  });
}
