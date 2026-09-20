# Lab 5: NestJS Fundamentals - Modules, Controllers, Providers & DI

## Setup

```bash
npm install
```

## Task

`VerificationController`/`VerificationService` are given, complete, unchanged - the
exact pair from the demo. Two TODOs, adding a SECOND provider/controller pair
following the same pattern:

1. **`attempts.service.ts`** - implement `getSummary()` to return
   `{ successCount, failCount }`, counted from the given `attempts` array (identical
   logic to Module 2/3's counting).
2. **`app.module.ts`** - add `AttemptsController` to `controllers` and
   `AttemptsService` to `providers`, alongside the `Verification` pieces already
   there.

Build and run this now, before changing anything:

```bash
npm run build
npm run start
```

`GET /verify/dave` already works:

```bash
curl http://localhost:3000/verify/dave
```

```
{"username":"dave","verified":true}
```

`GET /attempts/summary` does NOT - verified real result:

```bash
curl http://localhost:3000/attempts/summary
```

```
{"message":"Cannot GET /attempts/summary","error":"Not Found","statusCode":404}
```

That 404 is TODO 2, not TODO 1 - `AttemptsController`'s route is never even
REGISTERED yet, so Nest doesn't know the path exists at all. Do TODO 2 first, rebuild,
and the 404 becomes a real 500 from TODO 1's `throw`. Then do TODO 1.

**Always rebuild with `npm run build` and run `node dist/main.js`** - do not use
`tsx` for this lab. This module's demo showed exactly why: `tsx`'s `esbuild` compiler
doesn't support `emitDecoratorMetadata`, and Nest's dependency injection silently
breaks without it.

## Expected Output (once both TODOs are done)

```bash
curl http://localhost:3000/attempts/summary
```

```
{"successCount":2,"failCount":2}
```

## A Question Worth Sitting With

If `AttemptsService` were left OUT of `app.module.ts`'s `providers` array, but
`AttemptsController` WAS added to `controllers`, what would actually happen when the
server starts - a silent failure like TODO 1's runtime `undefined`, or something else
entirely? Try it and see before reading the model answer.
