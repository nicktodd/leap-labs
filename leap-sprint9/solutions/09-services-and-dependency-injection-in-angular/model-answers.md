# Lab 9 Model Answers

## Verified Output

Built and run for real (`solutions/mission-ui`, `Holdings` service + `HoldingsSummary` +
`PortfolioBadge`):

- Initial load: holdings list total `34,070.00`, header badge `Portfolio: 34,070.00` — match.
- After one "Add BP.L" click in the holdings list: both read `35,030.00` — still match,
  updated from a single event in a component the badge has no reference to.

## Key Points

- **`private readonly holdings`, exposed via `.asReadonly()`**: `private` is a TypeScript
  compile-time check only — it stops *other TypeScript code in this project* from writing
  `this.holdingsService.holdings.set(...)`, because the compiler refuses to let code outside
  the class reference a private member at all. It does **not** stop something written in
  plain JavaScript, or code that bypasses the type checker, from reaching the same object at
  runtime. `.asReadonly()` is the real functional protection: it returns a *different*
  signal object that only has a getter, with no `.set()`/`.update()` on it at all — even if
  something got a reference to it, there's no method to call. Together: `private` protects
  intent at compile time, `.asReadonly()` protects behaviour at runtime.
- **Trying to make `holdings` public and calling `.set()` from `PortfolioBadge`**: this
  *would* compile and work — nothing in Angular itself prevents a consumer from mutating a
  service's public writable signal directly. The whole reason to keep it private and expose
  only `add()`/`remove()`/`all` is discipline the *class author* enforces, not something
  Angular enforces automatically. This is the real reason it's worth doing even though
  Angular "lets" you skip it: an app with a dozen components allowed to `.set()` a shared
  signal directly has no single place left to reason about how its value can change.

## The Reflection Questions

**Why `inject(Holdings)` in two unrelated components returns the same instance**:
`@Injectable({ providedIn: 'root' })` registers the class
with Angular's **root injector** — a single injector instance shared by the entire
application. The first time anything asks for `Holdings` (via `inject()` or a constructor
parameter), the root injector constructs *one* instance and caches it. Every subsequent
request for `Holdings`, from any component anywhere in the app, receives that same cached
instance back rather than a new one. Nothing about `HoldingsSummary` or `PortfolioBadge`
needs to know about each other, a parent component, or any wiring — the sharing is a property
of the injector, not something either component arranges.

**What a third component would need to do differently to add a holding**: nothing beyond
what `HoldingsSummary` already does — `inject(Holdings)` and call `.add(...)`. That's the
actual point of extracting the logic into a service in the first place: the *rules* for what
counts as a valid update (here, trivial — just appending; in a real app, perhaps validation
or an API call) live in exactly one place, and every component that needs to trigger them
calls the same method rather than re-implementing the logic itself. A fourth, fifth, or
tenth component would look identical in this respect.
