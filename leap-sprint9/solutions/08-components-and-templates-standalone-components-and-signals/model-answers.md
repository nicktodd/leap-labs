# Lab 8 Model Answers

## Verified Output

The real component (`solutions/mission-ui/src/app/holdings-summary/`) was run with
`ng serve`, screenshotted via Playwright at each step:

- Initial load: two seeded holdings, total value `34,070.00` (500×42.1 + 120×108.5).
- After "Add BP.L": three rows, total `13,980.00` after also removing ULVR.L — confirmed by
  hand: 120×108.5 + 200×4.8 = 13,980.00.

## Key Points

- **`interface Holding`**: plain TypeScript, no Angular import needed — Sprint 8 already
  covered this.
- **`signal<Holding[]>([...])`**: the component's entire local state, seeded so the template
  has something to render on first load without needing a service or HTTP call yet.
- **`computed(() => ...)`**: reads `holdings()` inside its function body — that read is what
  registers `totalValue` as *depending on* `holdings`, so Angular knows to invalidate its
  cached result whenever `holdings` actually changes.
- **`.update()` with a spread/`.filter()`**: both return a brand-new array object, never the
  same reference as before.

## The Reflection Questions — Verified, Not Guessed

**What actually happens when `addHolding()` mutates in place** (tested directly, not
theorised): change it to `current.push(...); return current;` and click "Add BP.L" three
times. The result is genuinely surprising:

- The **list grows every time** — a new `<li>` appears for each click, correctly showing
  BP.L.
- The **total value never changes** — it stays at the original `34,070.00` forever, even
  after four items are showing.

The list and the total *disagree*, and the reason is precise: template interpolations like
`{{ totalValue() }}` and control-flow blocks like `@for (holding of holdings(); ...)` are
re-evaluated on every change-detection pass — this project uses zone.js (the CLI default,
not `provideZonelessChangeDetection()`), so *any* DOM event, including this click, triggers a
full change-detection pass regardless of whether a signal "changed." During that pass,
`holdings()` is called fresh and returns the live, mutated array — so `@for`'s tracking (by
`ticker`) correctly spots a new key and inserts a new row. But `computed()` doesn't
recompute on every read the way `@for` re-evaluates its expression — it only recomputes when
the signal graph tells it a dependency actually changed, which is decided by `Object.is`
comparison inside the signal's `set()`/`update()`. Since `.update()` returned the exact same
array reference, that comparison says "unchanged," so `totalValue`'s cached value is never
invalidated — it silently goes stale, disagreeing with what's now on screen.

This is the real, concrete reason signals must be updated immutably: mutating in place
doesn't reliably fail loudly. It can produce a UI that's *partially* correct and partially
wrong at the same time, which is far more dangerous in a real application than an update that
visibly does nothing.

**What would break with a manually-`.set()` `totalValue` signal instead of `computed()`**:
nothing would break in *this* lab specifically, because `addHolding()`/`removeHolding()`
already know exactly when `holdings` changes and could call `.set()` right after. But it
introduces a maintenance burden `computed()` removes entirely: every *future* place that
modifies `holdings` — a new method, a service call in Module 9, anything — would also have
to remember to update `totalValue` by hand, and forgetting even once produces the exact same
kind of silently-stale value this question's first half just demonstrated. `computed()`
can't be forgotten, because it isn't manually triggered at all.
