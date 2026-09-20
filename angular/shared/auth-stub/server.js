const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// --- CORS is deliberately NOT enabled here yet. ---
// Module 4's lab walks through the real browser CORS failure this causes,
// then adds the fix below as one line - uncomment it (and adjust the
// origin as later modules need, e.g. http://localhost:4200 for ng serve):
//
// const cors = require('cors');
// app.use(cors({ origin: ['http://localhost:8000', 'http://localhost:4200'] }));

// A stub, not a real user store - one account is enough to demonstrate
// "valid credentials in, real JWT out" and "wrong credentials, real 401".
const USERS = {
  alice: { password: 'mission123', roles: ['MISSION_OPERATOR'] },
};

const SECRET = process.env.JWT_SECRET || 'mission-control-shared-secret-key-32-bytes-minimum';

app.post('/auth/login', (req, res) => {
  const { username, password } = req.body || {};
  const user = USERS[username];
  if (!user || user.password !== password) {
    return res.status(401).json({
      statusCode: 401,
      message: 'invalid username or password',
      error: 'Unauthorized',
    });
  }
  const accessToken = jwt.sign(
    { sub: username, roles: user.roles },
    SECRET,
    { algorithm: 'HS256', expiresIn: '1h' },
  );
  // Nothing in this course's labs ever reads refreshToken - it's returned
  // only because the response shape (accessToken + refreshToken) is what a
  // real identity service provides, and mission-ui's AuthApiService is
  // already typed against it.
  const refreshToken = crypto.randomBytes(24).toString('hex');
  res.json({ accessToken, refreshToken });
});

app.get('/health', (req, res) => res.json({ status: 'up' }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`mission auth stub (angular week) listening on http://localhost:${PORT}`);
  console.log(`Try: curl -X POST http://localhost:${PORT}/auth/login -H "Content-Type: application/json" -d '{"username":"alice","password":"mission123"}'`);
});
