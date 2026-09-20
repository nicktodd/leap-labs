# Mission Auth Stub (Angular week)

A minimal Node.js/Express service that issues real JWTs for `mission-ui` to log in against.
This is a separate copy of the same idea as the Spring week's `shared/auth-stub` - same
shared-secret trust relationship, same one hardcoded account - but with the `/auth/login`
route and response shape (`accessToken` + `refreshToken`) that this week's labs are written
against, and CORS deliberately left off by default so Module 4 has a real failure to fix.

The Node week builds a full, production-shaped identity service later, in NestJS. This stub
is a deliberately small stand-in until then - not a preview of that service's internals.

## Run it

```bash
cd shared/auth-stub
npm install
npm start
```

Listens on `http://localhost:3000`.

## Get a token

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"mission123"}'
```

Returns `{"accessToken": "eyJhbGc...", "refreshToken": "..."}`. Any other username/password
returns a `401` with `{"message": "invalid username or password"}`.

## CORS is off until Module 4 turns it on

By default, nothing but `curl` (or another server-to-server tool) can call this service - a
browser page on a different origin will be blocked, and that failure is the point of Module
4's lab. The fix is uncommenting two lines in `server.js`:

```javascript
const cors = require('cors');
app.use(cors({ origin: ['http://localhost:8000', 'http://localhost:4200'] }));
```

`8000` is the plain HTML page Modules 1-4 build by hand; `4200` is `mission-ui`'s `ng serve`
dev server from Module 7 onward. Once this fix is in, it stays in for the rest of the week.

## The shared secret

Same mechanism as the Spring week's stub: this service and the mission service agree on one
HMAC secret (`mission-control-shared-secret-key-32-bytes-minimum` by default, overridable via
`JWT_SECRET`). The mission service never calls this service directly - it only checks that a
token's signature could have come from something that knows the same secret.
