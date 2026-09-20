# Module 6 Demo Guide - DTOs & Validation in NestJS

Module 5's `VerificationController` trusted whatever the client sent completely - a
`GET` request with a username in the URL. This module adds a `POST` route with a real
request BODY, and asks the question Module 5 never had to: what happens when that body
is wrong, missing fields, or has fields it shouldn't?

## Part 1: A DTO - the Shape of a Request

```typescript
import { IsString, IsNotEmpty, MinLength } from "class-validator";

export class VerifyCredentialsDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;
}
```

A **DTO (Data Transfer Object)** is a plain class describing the SHAPE an incoming
request body must have, decorated with `class-validator` rules describing what makes
that shape VALID. This is Module 4's `interface Attempt` idea, one step further -
`interface` only describes shape at COMPILE time; a DTO's decorators are checked at
RUNTIME, against data that's arriving from outside the program entirely, where
TypeScript's compile-time checking has no power at all.

**Compare to Java:** this is a request DTO plus **Bean Validation** - `@IsString()` is
`@NotBlank`-adjacent, `@IsNotEmpty()` is `@NotEmpty`, `@MinLength(3)` is `@Size(min =
3)`. The whole `class-validator` library exists specifically to bring Java's Bean
Validation pattern to TypeScript.

## Part 2: Using the DTO in a Controller

```typescript
@Controller("verify")
export class VerificationController {
  constructor(private readonly verificationService: VerificationService) {}

  @Post()
  checkCredentials(@Body() body: VerifyCredentialsDto) {
    const verified = this.verificationService.verify(body.username);
    return { username: body.username, verified };
  }
}
```

`@Body()` extracts the request body and, combined with `@Post()`'s type annotation,
tells Nest to validate the incoming JSON against `VerifyCredentialsDto` BEFORE
`checkCredentials` runs. If validation fails, this method body never executes at all -
the request is rejected before the controller sees it.

**Compare to Java:** `@Body() body: VerifyCredentialsDto` combined with the global
pipe (Part 3) is doing Spring's `@Valid @RequestBody VerifyCredentialsDto body` - Spring
needs `@Valid` spelled out on every parameter; Nest turns validation on globally
instead (Part 3).

## Part 3: The Global ValidationPipe

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
  }),
);
```

Applied ONCE, in `main.ts`, to every route in the entire application - not opted into
per-route the way Spring's `@Valid` is. `whitelist: true` strips any property NOT
declared on the DTO; `forbidNonWhitelisted: true` goes further and REJECTS the whole
request outright if an undeclared property shows up, instead of silently dropping it.

## Part 4: Five Real Requests, Five Real Responses

```bash
curl -X POST http://localhost:3000/verify -H "Content-Type: application/json" \
  -d '{"username":"alice"}'
```

```
{"username":"alice","verified":true}
```

A valid request passes straight through - nothing about this response looks any
different from Module 5's version.

```bash
curl -X POST http://localhost:3000/verify -H "Content-Type: application/json" -d '{}'
```

```
{"message":["username must be longer than or equal to 3 characters","username should not
be empty","username must be a string"],"error":"Bad Request","statusCode":400}
```

A missing field fails ALL THREE decorators at once - `class-validator` doesn't stop at
the first failure, it reports everything wrong in one response.

```bash
curl -X POST http://localhost:3000/verify -H "Content-Type: application/json" \
  -d '{"username":"ab"}'
```

```
{"message":["username must be longer than or equal to 3 characters"],"error":"Bad
Request","statusCode":400}
```

Too short - only `@MinLength(3)` fails; `@IsString()` and `@IsNotEmpty()` both pass,
so only one message appears.

```bash
curl -X POST http://localhost:3000/verify -H "Content-Type: application/json" \
  -d '{"username":123}'
```

```
{"message":["username must be longer than or equal to 3 characters","username must be a
string"],"error":"Bad Request","statusCode":400}
```

Wrong TYPE - a number instead of a string. This is exactly the runtime version of
the Angular week's compile-time `TS2345` error, except this data came from outside the program
entirely, where TypeScript's compiler has no power at all.

```bash
curl -X POST http://localhost:3000/verify -H "Content-Type: application/json" \
  -d '{"username":"alice","isAdmin":true}'
```

```
{"message":["property isAdmin should not exist"],"error":"Bad Request","statusCode":400}
```

An extra field - `isAdmin`, never declared on the DTO - rejected outright because of
`forbidNonWhitelisted: true`. This one is worth naming directly: a request that tries
to sneak an unexpected field like `isAdmin` into a login request is EXACTLY the kind of
thing a real attacker would attempt against a real auth endpoint (Module 7's mission
touches exactly this). Rejecting unknown fields outright, rather than silently
ignoring them, is a real security control, not just tidiness.

## A Running Comparison

| NestJS | Java (Spring + Bean Validation) |
|---|---|
| DTO class + class-validator decorators | Request DTO + Bean Validation annotations |
| `@IsString()` | `@NotBlank` (closest equivalent) |
| `@IsNotEmpty()` | `@NotEmpty` |
| `@MinLength(3)` | `@Size(min = 3)` |
| `@Body() body: Dto` + global ValidationPipe | `@Valid @RequestBody Dto body` (per-parameter opt-in) |
| `whitelist` / `forbidNonWhitelisted` | Jackson's `FAIL_ON_UNKNOWN_PROPERTIES` (closest equivalent) |

## Transition to the Lab

Learners add a second DTO and route - a `RegisterDto` with more fields and stricter
rules than `VerifyCredentialsDto` - verified against several real requests (valid,
missing field, wrong type, extra field), matching this demo's five-scenario pattern.
