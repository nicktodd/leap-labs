# Lab 14 Model Answers

## Verified Output

Built and run for real:

- `ng build` listed `place-order` (42.62 kB) and `holdings-summary` (1.97 kB) under **Lazy
  chunk files**, separate from `main.js` — confirmed neither ships in the initial bundle.
- Loading `/` redirected to `/holdings` automatically; clicking "Place Order" changed the URL
  to `/orders` with no full page reload, and moved the `routerLinkActive` styling to the
  second link.
- Removing `pathMatch: 'full'` from the `''` redirect and reloading produced a real, fatal
  runtime error — Angular refused to even start the router:

  ```
  RuntimeError: NG04014: Invalid configuration of route '{path: "", redirectTo: "holdings"}':
  please provide 'pathMatch'. The default value of 'pathMatch' is 'prefix', but often the
  intent is to use 'full'.
  ```

  This is more precise than "an infinite redirect loop" — Angular 21 actually validates route
  configuration at startup and throws immediately rather than letting a broken redirect run.

## Key Points

- **`redirectTo` + `pathMatch: 'full'`**: without `pathMatch: 'full'`, the default matching
  mode (`'prefix'`) treats `''` as a match for *any* URL that starts with nothing extra
  required — which is every URL — creating an ambiguous, invalid configuration Angular now
  refuses to run at all, rather than silently doing the wrong thing.
- **`loadComponent`**: a function returning a dynamic `import()`, not a static top-of-file
  `import` — the component's code is fetched only when its route is visited, verified by the
  real `ng build` chunk listing above.

## The Reflection Questions

**What breaks without `pathMatch: 'full'`**: verified directly — Angular 21 throws
`NG04014` at application startup, a hard runtime error, not a subtle bug. The route
configuration is invalid the moment the app tries to boot, because an ambiguous `redirectTo`
on a prefix-matched empty path has no well-defined meaning the router is willing to guess at.
`pathMatch: 'full'` resolves the ambiguity by saying "only redirect when the URL is *exactly*
empty," leaving `/holdings` and `/orders` alone.

**When lazy loading a route makes the user's experience worse**: the most common real case is
a route a user visits *immediately* after the app first loads — for example, if `/holdings`
(this app's default, redirected-to route) were lazy-loaded instead of the root route eagerly
bundling it. The very first thing most users see would require a *second* network round-trip
after the initial page load completes, adding a visible delay (and a loading flicker) exactly
where a user is least willing to wait — the first thing they see. Angular's `PreloadAllModules`
strategy (or a custom preloading strategy) exists specifically to soften this: it still lazy-
loads for the initial bundle-size win, but starts fetching the other routes' chunks in the
background immediately after the app boots, so by the time a user actually clicks, the chunk
is often already there.
