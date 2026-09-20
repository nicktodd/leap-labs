# Module 3 Demo Guide - Node.js Fundamentals: Event Loop, Modules & npm

Every module since Module 2 has run on Node without ever asking what Node actually IS.
This module answers that directly, then goes deeper on two things already used ad hoc
throughout the week: how Node schedules async work, and the module system underneath
every `import`/`export` and `require()` written so far.

## Part 0: What Node.js Actually Is

Three pieces, not one:

- **V8** - the same JavaScript engine Chrome uses, compiling and running the JS itself.
- **libuv** - a C library providing the event loop and async I/O (file system, network,
  timers) - the reason JavaScript, a single-threaded language, can do non-blocking I/O
  at all.
- **Node's own APIs** - `fs`, `http`, `process`, `require()` - things that exist in
  Node but NOT in browser JavaScript, and vice versa (`document`, `window` exist in a
  browser, not in Node).

**Compare to Java:** V8 + libuv together are roughly Node's JVM - the thing that
actually executes the language and manages runtime concerns beneath it. Node's
built-in APIs are roughly the JDK's standard library (`java.io`, `java.net`).

## Part 1: The Event Loop, For Real

Module 2 said JavaScript is single-threaded and `setTimeout` doesn't start a thread -
it registers a callback with the event loop. Before looking at execution ORDER, it's
worth naming the four pieces actually involved - see the accompanying diagram slide
("The Event Loop: How the Pieces Fit Together") for the visual version of this:

- **The call stack** - the ONLY place JavaScript code actually executes. One function
  frame at a time, strictly synchronous. Nothing else in this list runs code directly;
  everything else exists to get work ONTO the call stack at the right moment.
- **Node APIs / libuv** - where async work actually HAPPENS: timers counting down,
  files being read, network requests in flight - all handled by libuv's own C code and
  thread pool, completely off the JavaScript thread. This is the box `setTimeout` and
  `fs.readFile` hand work off to.
- **The microtask queue** - holds `process.nextTick` and `Promise` callbacks. Crucially,
  this queue is filled directly from code running ON the call stack (calling `.then()`
  or `process.nextTick()`), not by libuv finishing something asynchronous.
- **The macrotask (callback) queue** - where libuv puts a callback once its async work
  is actually done. `setTimeout` callbacks, completed I/O callbacks, `setInterval` ticks
  all arrive here.

**The event loop itself is just a loop**, repeatedly asking one question: *is the call
stack empty?* If yes: drain the microtask queue completely (every `nextTick`, then every
`Promise` callback, including any NEW ones queued while draining). Only once the
microtask queue is fully empty does it take exactly ONE task off the macrotask queue,
run it, and ask the same question again.

This demo shows the actual ORDER things run in, given that loop.

```bash
node event-loop-demo.cjs
```

Verified real output:

```
1: synchronous - runs immediately
2: synchronous - runs immediately, straight after line 1
3: process.nextTick callback - Node's OWN microtask queue, drained before Promise's
4: Promise.then callback - a MICROTASK
5: setTimeout callback - a MACROTASK
```

The rule this demonstrates: all SYNCHRONOUS code runs first, then Node drains its own
`process.nextTick` queue completely, then the Promise MICROTASK queue completely, and
only then does it move on to MACROTASKS like `setTimeout` - even a `setTimeout` with a
delay of `0`.

### A Genuine Surprise, Verified

Run the EXACT same code as an ES module instead:

```bash
node event-loop-demo-esm.mjs
```

Verified real output:

```
1: synchronous - runs immediately
2: synchronous - runs immediately, straight after line 1
4 (was 3 in the .cjs run): Promise.then callback
3 (was 4 in the .cjs run): process.nextTick callback
5: setTimeout callback - a MACROTASK
```

**The order is different.** Same code, same Node version, only the module system
changed. Node's ESM entry points are themselves loaded through machinery that involves
Promises, which appears to insert an extra microtask checkpoint around a module's
top-level code - the practical, honest takeaway is not a precise internal mechanism to
memorise, but a caution: **"nextTick always beats Promise.then" is a rule of thumb, not
a law** - verified here on Node 24, and worth re-verifying rather than assuming if
ordering-sensitive code is ever written for real. This is exactly the kind of claim
worth testing rather than trusting, the same discipline this whole week has applied
to every other "the docs say..." claim.

## Part 2: Modules - CommonJS vs ES Modules

Every `.mjs` file since Module 2 has used ES Modules (`import`/`export`). Node's
ORIGINAL module system - still the default for any `.js` file without `"type":
"module"` in `package.json` - is CommonJS.

`verify-utils.cjs`:

```javascript
function isKnownUser(username) {
  return KNOWN_USERS.includes(username);
}

module.exports = { isKnownUser, KNOWN_USERS };
```

`main.cjs`:

```javascript
const { isKnownUser, KNOWN_USERS } = require("./verify-utils.cjs");
console.log(KNOWN_USERS);
console.log(isKnownUser("alice"));
console.log(isKnownUser("mallory"));
```

```bash
node main.cjs
```

Verified real output:

```
[ 'alice', 'bob', 'carol' ]
true
false
```

Three real differences from every `.mjs` file this week has used:

- **`module.exports`** is the file's ENTIRE public surface, assigned once - there's no
  per-declaration `export` keyword the way ESM has.
- **`require()`** is synchronous and resolved at the exact line it's called, not
  hoisted to the top of the file the way `import` effectively is.
- **No file extension requirement** - `require("./verify-utils.cjs")` works with or
  without the extension, unlike Module 4's `NodeNext` resolution rule for ESM, which
  made the extension mandatory.

**Compare to Java:** CommonJS's `require()` behaves closer to Java's `import` in one
specific way - both resolve synchronously, at load time, rather than ESM's more
asynchronous module graph resolution. Neither language comparison is exact; this is
genuinely a JavaScript-specific wrinkle (two competing module systems in the same
runtime) that Java and Python don't have.

## Part 3: npm - Beyond `npm install`

Every module since 4 has run `npm install`. This part looks at what's actually in
`package.json` once it exists.

```json
{
  "name": "04-the-typescript-build-process-tsconfig-compiling-and-tooling",
  "version": "1.0.0",
  "description": "",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "tsx": "^4.23.1",
    "typescript": "^7.0.2"
  }
}
```

(Module 4's real, actual `package.json`.)

- **`dependencies` vs `devDependencies`** - `dependencies` ship with the running
  application; `devDependencies` (like `typescript` here) are needed only to BUILD or
  TEST it, never installed in a production deployment that skips dev dependencies.
- **`"^7.0.2"`** - semver range syntax. `^` allows any version compatible with `7.0.2`
  without a MAJOR version bump (so `7.1.0` is fine, `8.0.0` is not). `~7.0.2` would only
  allow patch-level updates (`7.0.x`). An exact `"7.0.2"` with no prefix pins it
  precisely.
- **`scripts`** - arbitrary named shell commands, run via `npm run <name>` (Module 4
  used `build`, `start`, and `dev` this way).
- **`package-lock.json`** (generated alongside `package.json`, not hand-written) - pins
  the EXACT resolved version of every dependency AND every dependency's dependencies,
  so `npm install` produces an identical `node_modules/` on every machine, not just one
  compatible with the semver ranges.

**Compare to Java:** `package.json` + `package-lock.json` together do the job of
`pom.xml` + a resolved dependency tree - `dependencies`/`devDependencies` map onto
Maven's `<dependencies>` with `<scope>compile</scope>` vs `<scope>test</scope>`.
**Compare to Python:** closest to `pyproject.toml`/`requirements.txt`, though Python's
ecosystem has historically been looser about lockfiles - `package-lock.json`'s
exhaustive pinning is closer to what a `pip freeze > requirements.txt` snapshot
achieves, except npm generates and maintains it automatically.

## Transition to the Lab

Learners write a small CommonJS module and a script that requires it, add a `scripts`
entry to a `package.json`, and predict (then verify) the print order of a small
mixed sync/microtask/macrotask snippet - checked against real `node` output, not
their prediction alone.
