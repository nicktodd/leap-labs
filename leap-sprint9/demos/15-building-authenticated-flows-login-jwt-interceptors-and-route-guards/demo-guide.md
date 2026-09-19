# Module 15 Demo Guide — Building Authenticated Flows: Login, JWT Interceptors & Route Guards

**Duration:** 35 minutes
**Prerequisite:** Module 14's routed `/holdings` and `/orders`. Same running backends as
Modules 11-14. Every earlier module hardcoded `alice`/`mission123` inside `MissionApi` — today
replaces that with a real login screen nothing else depends on secretly logging in for you.

Three pieces work together today: a login form, a service holding the token in memory, an
interceptor that attaches it automatically, and a guard that keeps unauthenticated visitors
off the protected routes. Building all three together is the point — a login form alone does
nothing without somewhere to keep the token and something reading it back out.

## Part 0: Where the Token Lives (5 min)

```typescript
// token-store.ts
@Injectable({ providedIn: 'root' })
export class TokenStore {
  private readonly token = signal<string | null>(null);
  private readonly username = signal<string | null>(null);

  readonly isAuthenticated = computed(() => this.token() !== null);
  readonly currentUsername = this.username.asReadonly();

  setToken(token: string, username: string): void { ... }
  getToken(): string | null { return this.token(); }
  clear(): void { ... }
}
```

Module 9's exact pattern — a service, `providedIn: 'root'`, shared by anything that injects
it. Deliberately **in-memory only**: no `localStorage`, no cookie. A page refresh loses the
session, which is correct scope for this module — a persistent session is a separate concern
this sprint doesn't build.

## Part 1: A Real Login Form (7 min)

```typescript
// login-page.ts
protected submit(): void {
  if (this.loginForm.invalid) {
    this.loginForm.markAllAsTouched();
    return;
  }
  const { username, password } = this.loginForm.getRawValue();
  this.authApi.login(username!, password!).subscribe({
    next: (response) => {
      this.tokenStore.setToken(response.accessToken, username!);
      this.router.navigate(['/holdings']);
    },
    error: () => this.error.set('Invalid username or password.'),
  });
}
```

Module 13's reactive-form pattern exactly, calling `AuthApi.login()` (a thin service wrapping
one `HttpClient.post` to the Sprint 8 auth service's real `/auth/login`). Success stores the
token and navigates away; failure shows a message — nothing new here that Modules 10 and 13
didn't already teach.

## Part 2: The Interceptor — Attaching the Token Automatically (8 min)

```typescript
// auth-interceptor.ts
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenStore = inject(TokenStore);
  const token = tokenStore.getToken();

  if (token && req.url.startsWith(MISSION_SERVICE_BASE)) {
    const authedReq = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
    return next(authedReq);
  }
  return next(req);
};
```

This replaces every earlier module's manual header-attaching. Module 11 set a header on one
`http.post` call by hand; Module 12 set `configuration.credentials` once, manually, right
after login. An interceptor runs on **every** outgoing HTTP request, application-wide — the
generated `OrderControllerService`, any future service, none of them need to know a token
exists. The `req.url.startsWith(...)` check matters specifically: without it, the token would
also attach to the *login* request itself, which needs no token at all.

Registering it:

```typescript
// app.config.ts
provideHttpClient(withInterceptors([authInterceptor])),
```

## Part 3: The Guard — Protecting Routes (6 min)

```typescript
// auth-guard.ts
export const authGuard: CanActivateFn = () => {
  const tokenStore = inject(TokenStore);
  const router = inject(Router);

  if (tokenStore.isAuthenticated()) return true;

  router.navigate(['/login']);
  return false;
};
```

```typescript
// app.routes.ts
{ path: 'holdings', canActivate: [authGuard], loadComponent: () => ... },
{ path: 'orders', canActivate: [authGuard], loadComponent: () => ... },
```

`canActivate` runs *before* Angular loads the route's component at all — an unauthenticated
visitor never even downloads `HoldingsSummary`'s lazy chunk, let alone sees it. Returning
`false` alone would leave the user stuck on a blank page; the guard also has to redirect
somewhere useful.

## Part 4: Verified — the Whole Flow, Live (9 min)

Visit `/holdings` directly, with no prior login:

![The guard redirects an unauthenticated visitor to /login](screenshots/guard-redirect.png)

Log in with `alice`/`mission123`. The URL moves to `/holdings`, and the header now shows
"Logged in as alice" with a Log Out button. Navigate to "Place Order" and submit a real order:

![A real order, submitted with a token the interceptor attached automatically](screenshots/order-submitted.png)

The request's real `Authorization` header, captured directly from the network layer during
this exact click:

```
POST http://localhost:8090/accounts/1/orders
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

No code in `PlaceOrder` or `MissionApi` set that header — the interceptor did, reading
`TokenStore`, which the login form populated minutes earlier. Postgres confirms the same order
landed: `513` → `514`. Click "Log Out": the token clears, and the URL moves back to `/login`
— the guard would now block `/holdings` again, exactly as it did before logging in at all.

## Key message

Three small, separately-testable pieces combine into one flow: a form that only knows how to
call `/auth/login` and store what comes back; an interceptor that only knows how to read the
stored token and attach it; a guard that only knows how to check whether a token exists. None
of them know about each other directly — they all depend on the same `TokenStore`, which is
the only thing that actually connects them.

## Transition to the Lab

Learners build this same three-piece flow themselves — a login form, an interceptor, a guard
on at least one route — and verify it the way today's demo did: a real redirect when
unauthenticated, a real token attached automatically after login, and a real order accepted
by the actual backend.
