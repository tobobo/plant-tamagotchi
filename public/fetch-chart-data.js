const chartResolutions = {
  minute: 60 * 1000,
  hour: 60 * 60 * 1000,
  day: 24 * 60 * 60 * 1000,
};

export default async function getChartData(start, end, resolution) {
  const query = new URLSearchParams({
    ...(start && { start }),
    ...(end && { end }),
    ...(resolution && { resolution }),
  });
  debugger;
  const responseData = await (await fetch(`./moisture?${query}`)).json();
  
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
