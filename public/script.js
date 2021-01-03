const chartResolutions = {
  minute: 60 * 1000,
  hour: 60 * 60 * 1000,
  day: 24 * 60 * 60 * 1000,
};

async function getChartData(start, end, resolution) {
  const responseData = await (await fetch('./moisture')).json();
  
  const labels = [];
  const data = [];
  
  let dataIndex = 0;
  const dateCursor = new Date(responseData.start);
  const endDate = new Date(responseData.end);
  
  while (dateCursor < endDate) {
    const [dataLabel, dataValue] = responseData.data[dataIndex] || [];
    labels.push(dateCursor.toISOString());
    if (dataLabel && new Date(dataLabel) <= dateCursor) {
      data.push(dataValue);
      dataIndex += 1;
    } else {
      data.push(null)
    }
    dateCursor.setTime(dateCursor.getTime() + chartResolutions[responseData.resolution])
  }

  debugger;
  return {
    labels,
    datasets: [
      {
        label: 'moisture',
        spanGaps: false,
        data,
      }
    ]
  }
}

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
    data: await getChartData(),
  }); 
}

start();
