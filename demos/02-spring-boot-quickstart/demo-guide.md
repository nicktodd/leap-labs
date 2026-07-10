# Module 2 Demo Guide — Spring Boot Quickstart

Live-build this from an empty folder if time allows — otherwise walk through the finished
project in this order, as if building it.

```bash
mvn spring-boot:run
# in a second terminal:
curl http://localhost:8080/hello
```

Expect: `Hello from the mission service`.

## Step 1: `pom.xml` — the Parent Is Doing Most of the Work

Point at `<parent>spring-boot-starter-parent</parent>` first. This is a **dependency management
BOM (Bill of Materials)** — it doesn't add any dependencies itself, but it pins compatible
versions for every Spring Boot dependency you add later, so you never have to figure out which
version of `spring-web` matches which version of `spring-context` by hand.

Then point at the single dependency: `spring-boot-starter-web`. **Say explicitly**: this one
"starter" transitively pulls in Spring MVC, an embedded Tomcat server, and Jackson (for JSON) —
compare this to a plain Java web app, where you'd configure a servlet container, a dispatcher
servlet, and a JSON library by hand.

## Step 2: `MissionServiceApplication` — What `@SpringBootApplication` Actually Does

This one annotation is three:
- `@Configuration` — this class can define Spring beans
- `@EnableAutoConfiguration` — Spring Boot looks at what's on the classpath and configures things
  automatically (web starter present → configure an embedded Tomcat, no XML, no manual wiring)
- `@ComponentScan` — Spring scans this package and everything under it for `@Controller`,
  `@Service`, and other Spring-managed classes

**The `main` method really is that short.** `SpringApplication.run(...)` starts the whole
application context, the embedded server, and auto-configuration in one call.

## Step 3: `HelloController` — the Fastest Possible Endpoint

`@RestController` = `@Controller` + `@ResponseBody`: every method's return value is written
directly to the response body, not resolved to a view template. `@GetMapping("/hello")` maps
`GET /hello` to this method. Returning a plain `String` here is deliberate — the response is
`text/plain`, not JSON, because there's no object to serialize yet. That changes in Module 6
when DTOs show up.

## Step 4: `application.properties` — Configuration, Not Code

`server.port=8080` and `spring.application.name=mission-service` are both plain key-value
config, read at startup — no annotations, no code changes needed to alter them. Point out: this
is where Module 9's JWT secret and Module 7's database connection details will eventually live
too, though never as plain text in a real system (that's its own future conversation).

## Points to Make Explicitly

- **This is the fastest possible confidence-building win, deliberately.** No persistence, no
  security, no business logic yet — just "does the service start, does an endpoint respond."
  Everything harder gets layered on top of this working skeleton, one module at a time.
- **Auto-configuration is convenience, not magic.** Everything Spring Boot configures
  automatically here could be configured by hand — the framework is making a reasonable default
  choice based on what's on the classpath, not doing anything it couldn't be told to do explicitly.

## Transition to the Lab

Learners bootstrap their own first Spring Boot service from scratch and get their own `hello`
endpoint running — the same fast win, built by their own hands this time.
