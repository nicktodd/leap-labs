# Module 9 Demo Guide — NestJS Fundamentals: Modules, Controllers, Providers & DI

Everything so far this sprint has been plain Node or plain TypeScript. This is the
first real FRAMEWORK — the one Sprint 8's actual mission (replacing Sprint 6's
`auth-stub`) is built on. Four files, four concepts: a provider, a controller, a
module, and the bootstrap that ties them together.

**Compare to Java, up front:** everyone in this room has used Spring Boot in some form
by now (via earlier sprints' Java work, or general familiarity). NestJS was
DELIBERATELY designed to feel like Spring for the Node ecosystem — decorators instead
of annotations, dependency injection as the default, modules instead of Spring's
component scanning. The vocabulary maps closely enough that most of this module is
translation, not new ideas.

## Part 1: A Provider — the Work

```typescript
import { Injectable } from "@nestjs/common";

@Injectable()
export class VerificationService {
  private readonly knownUsers = ["alice", "bob", "carol"];

  verify(username: string): boolean {
    return this.knownUsers.includes(username);
  }
}
```

A **provider** is a class Nest can create and hand to anything that asks for it.
`@Injectable()` is what marks a class as something Nest is willing to manage — without
it, Nest has no idea this class exists as an injectable dependency.

**Compare to Java:** `@Injectable()` is NestJS's `@Service` (or `@Component`) — same
idea, same purpose: mark a class as something the framework's container should manage
and be able to hand out.

## Part 2: A Controller — the Front Door

```typescript
import { Controller, Get, Param } from "@nestjs/common";
import { VerificationService } from "./verification.service";

@Controller("verify")
export class VerificationController {
  constructor(private readonly verificationService: VerificationService) {}

  @Get(":username")
  checkUsername(@Param("username") username: string) {
    const verified = this.verificationService.verify(username);
    return { username, verified };
  }
}
```

A **controller** handles incoming HTTP requests and delegates the actual work to a
provider. `@Controller("verify")` prefixes every route below with `/verify`;
`@Get(":username")` maps `GET /verify/:username`.

**The constructor is doing something important**: `verificationService` is never
created with `new VerificationService()` anywhere in this class. Nest sees the
constructor needs a `VerificationService` and supplies one automatically — this is
**constructor injection**, dependency injection's most common form.

**Compare to Java:** `@Controller` is NestJS's `@RestController`; `@Get` is `@GetMapping`;
`@Param` is `@PathVariable`. Constructor injection works IDENTICALLY to Spring's own
constructor injection — Spring popularised exactly this pattern, and NestJS adopted it
directly.

## Part 3: A Module — Wiring It Together

```typescript
import { Module } from "@nestjs/common";
import { VerificationController } from "./verification.controller";
import { VerificationService } from "./verification.service";

@Module({
  controllers: [VerificationController],
  providers: [VerificationService],
})
export class AppModule {}
```

A **module** wires controllers to the providers they need. Nest reads this to know
which `VerificationService` instance to hand `VerificationController` — leaving
`VerificationService` out of `providers` here would make the injection in Part 2 fail,
even though the class itself is written correctly.

**Compare to Java:** this is the closest NestJS gets to Spring's `@Configuration` /
component scanning — except explicit, not automatic. Spring Boot scans packages
looking for annotated classes; NestJS requires every controller and provider to be
LISTED in a module. More typing, but no "why isn't my bean being picked up" mystery
from a missed `@ComponentScan` path.

## Part 4: Bootstrapping the Application

```typescript
import "reflect-metadata";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}

bootstrap();
```

**Compare to Java:** `NestFactory.create(AppModule)` is `SpringApplication.run(...)` —
the framework reads the root module/class, builds every provider and controller it
needs, wires the dependency graph, and starts listening.

`import "reflect-metadata"` at the very top is NOT optional — Nest's dependency
injection works by reading TYPE METADATA the TypeScript compiler attaches to each
class's constructor parameters, and `reflect-metadata` is the library that makes that
metadata readable at runtime. Which leads to a real, verified gotcha:

## A Real Gotcha: `tsx` Silently Breaks Dependency Injection

```bash
npm run dev:broken    # runs: tsx src/main.ts
curl http://localhost:3000/verify/alice
```

Verified real result: the server starts, logs the route as mapped, and then throws on
every request:

```
TypeError: Cannot read properties of undefined (reading 'verify')
    at VerificationController.checkUsername
```

`verificationService` is `undefined` inside the controller. The class is written
correctly, the module lists the provider correctly — the problem is `tsx`. Module 6
introduced `tsx` as a fast way to run TypeScript without a build step; `tsx` compiles
using `esbuild`, and **esbuild does not support `emitDecoratorMetadata`** — the exact
compiler feature Nest's DI depends on to know what type each constructor parameter
needs. `tsc` supports it; `tsx` silently does not, and gives no warning that anything
is wrong.

```bash
npm run build    # tsc
npm run start    # node dist/main.js
curl http://localhost:3000/verify/alice
curl http://localhost:3000/verify/mallory
```

Verified real output:

```
{"username":"alice","verified":true}
{"username":"mallory","verified":false}
```

**The lesson, stated directly:** `tsx` is genuinely useful for plain TypeScript (every
prior module in this sprint used it safely), but NestJS specifically needs a real `tsc`
build. This is exactly the kind of thing Module 6 warned about in the abstract — "a
lenient setup doesn't prevent bugs, it just moves them later" — except here the bug
isn't a compile error at all, it's a silent runtime failure with no error until a route
is actually hit.

## Transition to the Lab

Learners add a second provider and controller to this same module — following the
identical Provider → Controller → Module pattern — verified by building with `tsc` and
hitting the new route with `curl`, not `tsx`.
