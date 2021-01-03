function parseDate(qsDate) {
  return qsDate && new Date(qsDate).toISOString()
}

export default function parseQueryString() {
  const query = new URLSearchParams(window.location.search.slice(1));
  
  const start = parseDate(query.get('start'));
  const end = parseDate(query.get('end'));
  
  return {
    start,
    end,
    resolution: query.get('resolution'),
  };
}
