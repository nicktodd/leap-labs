// A tiny, dependency-free mock API - plain Node http, no Express.
// GET /api/holdings         -> 200, a real JSON array
// GET /api/holdings/error   -> 500, a real JSON error body
const http = require('http');

const holdings = [
  { ticker: 'VOD.L', quantity: 800, price: 0.72 },
  { ticker: 'HSBA.L', quantity: 300, price: 6.4 },
];

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (req.url === '/api/holdings') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(holdings));
    return;
  }

  if (req.url === '/api/holdings/error') {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: 'Mock server error' }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ message: 'Not found' }));
});

const PORT = 3500;
server.listen(PORT, () => {
  console.log(`Mock holdings API listening on http://localhost:${PORT}`);
});
