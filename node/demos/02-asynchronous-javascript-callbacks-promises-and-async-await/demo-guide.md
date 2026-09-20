# Module 2 Demo Guide - Asynchronous JavaScript: Callbacks, Promises & Async/Await

Three files, three ways of writing the exact same thing: check a username against a
fake network call, in sequence, then check three usernames concurrently. The
underlying "network call" (`verifyCredentials` / `verifyCredentialsCallback` in
`verify-credentials.mjs`) never changes - only the syntax wrapped around it does. This
mirrors what the Spring week's real `auth-stub` does for real: an HTTP call that takes time
and doesn't resolve immediately.

**Compare to Java and Python throughout:** JavaScript is single-threaded - there's no
`Thread`, no `ExecutorService`, no thread pool. `setTimeout` doesn't spin up a thread;
it registers a callback with the JavaScript engine's **event loop**, which runs it
once the timer expires and the current synchronous code has finished. This is the one
idea every comparison below builds on.

## Part 1: Callbacks - the Original Pattern

```bash
node callback-demo.mjs
```

Verified real output:

```
--- a single callback ---
Checking alice...
This line runs BEFORE the callback above - verifyCredentialsCallback returns immediately
Verified: alice
```

`verifyCredentialsCallback(username, callback)` returns immediately - before the fake
network delay finishes - and the console.log AFTER the function call runs first. The
callback function only runs later, once `setTimeout`'s delay expires. This is
**non-blocking**: the rest of the program keeps running instead of freezing while it
waits.

**Compare to Java:** the nearest equivalent is a `Runnable` or `Callback` interface
passed to something like `CompletableFuture.runAsync(runnable, executor)` - a function
handed to something else to call later. The difference is what "later" means: Java's
version runs on a separate thread from a thread pool; JavaScript's callback runs on
the SAME single thread, just at a later point in the event loop, after the current
code finishes.

**Compare to Python:** closest to passing a function into `threading.Timer(delay,
callback).start()` - same "call this later" idea, but again, Python's `Timer` uses an
actual separate thread; JavaScript's `setTimeout` doesn't.

### Callback Hell

```
--- callback hell: three checks, nested ---
Verified: alice
Verified: bob
Error: Unknown user: dave
```

Three checks that must happen in order, each depending on the last, nest three
callbacks deep - the "pyramid of doom." Every level needs its own error check
(`if (err1) ...`, `if (err2) ...`, `if (err3) ...`), and adding a fourth check means
nesting a fourth level. This isn't a JavaScript-specific mistake - Java code doing the
equivalent with nested `CompletableFuture` callbacks (`thenAccept` inside
`thenAccept`) reads exactly the same way. Promises exist specifically to flatten this.

## Part 2: Promises - Flattening the Pyramid

```bash
node promise-demo.mjs
```

Verified real output:

```
--- the same three checks, as a Promise chain ---
Verified: alice
Verified: bob
Error: Unknown user: dave

--- Promise.all: same three checks, running concurrently ---
[ 'alice', 'bob', 'carol' ]
```

Same three checks, same order, same error - but `.then()` chains flatten the pyramid
into a straight line, and one `.catch()` at the end handles an error from ANY step in
the chain, instead of a separate check at every level.

**Compare to Java:** a `Promise` is JavaScript's `CompletableFuture<T>`. `.then()` is
`.thenApply()`/`.thenCompose()`; `.catch()` is `.exceptionally()`. The chaining shape
is genuinely almost identical between the two.

**Compare to Python:** closest to `asyncio.Future`, though Python code rarely chains
futures with `.then()`-style methods directly - Python's ecosystem leans on
`async`/`await` (Part 3) even more heavily than JavaScript's does.

### Promise.all - Running Things Concurrently

The three checks in the second half don't depend on each other, so there's no reason
to wait for one before starting the next. `Promise.all([...])` starts all three fake
network calls at once and resolves when every one of them has finished.

**Compare to Java:** `CompletableFuture.allOf(future1, future2, future3)`. Same idea:
start everything, wait for all of it.

**Compare to Python:** `asyncio.gather(coro1, coro2, coro3)` - again, close to a
direct syntactic match.

## Part 3: Async/Await - Promises, Written to Look Synchronous

```bash
node async-await-demo.mjs
```

Verified real output:

```
--- the same three checks, as async/await ---
Verified: alice
Verified: bob
Error: Unknown user: dave

--- await Promise.all: same three checks, concurrently ---
[ 'alice', 'bob', 'carol' ]
```

Same three checks, same result, same error - this time written to read top-to-bottom
like ordinary synchronous code. `await` pauses the `async function` at that line until
the Promise resolves, without blocking anything else in the program. `try`/`catch`
replaces `.catch()` - ordinary JavaScript error handling, not a Promise-specific
mechanism.

**Compare to Java:** Java has no built-in `async`/`await` keyword pair. The closest
mechanisms are chained `CompletableFuture` calls (Part 2's comparison) or, in modern
Java (21+), virtual threads, which let blocking-style code run without tying up an OS
thread - a different mechanism reaching for a similar readability goal.

**Compare to Python:** this is the closest match of the whole module. Python's
`async def` / `await` is closer to JavaScript's `async`/`await` than almost anything
else compared this week - the keywords are even spelled almost the same, and
`try`/`except` around an `await` behaves the same way `try`/`catch` does here.

`await Promise.all([...])` at the end combines both ideas from Part 2: concurrent
execution, written with the synchronous-looking `await` syntax instead of `.then()`.

## A Running Comparison

| JavaScript | Java | Python |
|---|---|---|
| Callback function | `Runnable`/functional interface passed to an executor | Function passed to `threading.Timer` |
| `Promise` | `CompletableFuture<T>` | `asyncio.Future` |
| `.then()` / `.catch()` | `.thenApply()` / `.exceptionally()` | (rarely chained directly - `async`/`await` preferred) |
| `Promise.all([...])` | `CompletableFuture.allOf(...)` | `asyncio.gather(...)` |
| `async function` / `await` | No direct equivalent (virtual threads in 21+) | `async def` / `await` - closest match in this table |
| `try`/`catch` around `await` | `try`/`catch` around `.get()` | `try`/`except` around `await` |

**The one idea underneath all of it:** JavaScript is single-threaded. Every mechanism
above (`setTimeout`, `Promise`, `async`/`await`) is a way of saying "do this later,
once some condition is met, without blocking the one thread this program has" - never
"do this on a different thread," the way Java's approach almost always does.

## Transition to the Lab

Learners write an async function (their choice: Promise chain or async/await) that
checks a list of usernames against `verifyCredentials`, reporting which ones verify
successfully and which don't - first sequentially, then refactored to run
concurrently with `Promise.all`, verified by comparing output between the two
versions.
