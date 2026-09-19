# Lab 9 Model Answers

## Verified Output

```bash
curl http://localhost:3000/verify/dave
```
```
{"username":"dave","verified":true}
```

```bash
curl http://localhost:3000/attempts/summary
```
```
{"successCount":2,"failCount":2}
```

## Key Points

- **TODO 1** is a plain `for...of` loop with an `if`/`else` counting `successCount`/
  `failCount` — identical logic to Module 2/3's original counting, just returned as an
  object from a `@Injectable()` class instead of printed with `console.log`.
- **TODO 2** adds both `AttemptsController` and `AttemptsService` to their respective
  arrays in `@Module({...})`. Both are needed — the controller so its ROUTE gets
  registered at all, the provider so the controller's constructor injection actually
  resolves.

## The Reflection Question

Registering `AttemptsController` without registering `AttemptsService` produces a
real, verified crash **at server startup**, not a silent runtime failure:

```
UnknownDependenciesException [Error]: Nest can't resolve dependencies of the
AttemptsController (?). Please make sure that the argument AttemptsService at
index [0] is available in the AppModule module.
```

This is a genuinely useful contrast with TODO 1's failure mode. Leaving `getSummary()`
unimplemented (a `throw` inside a method body) only fails when a REQUEST actually hits
that route — the server starts fine, and the bug is invisible until it's exercised.
Leaving a provider unregistered fails immediately, on `npm run start`, before a single
request can be served, with an error message that names the exact missing piece. Nest's
dependency injection is checked EAGERLY, at startup, specifically so that a whole class
of "works until someone hits the broken endpoint" bugs becomes "won't even boot" bugs
instead — caught by whoever runs the app first, not whichever user happens to hit the
right URL.
