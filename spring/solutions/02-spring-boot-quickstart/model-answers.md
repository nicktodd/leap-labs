# Model Answers - Spring Boot Quickstart

## What each part of `@SpringBootApplication` does

| Part | What it does | What breaks without it |
|---|---|---|
| `@Configuration` | Marks this class as a source of Spring bean definitions | Any `@Bean` methods you add later on this class would be ignored |
| `@EnableAutoConfiguration` | Spring Boot inspects the classpath and configures things automatically (web starter present → embedded Tomcat configured) | No embedded server would start - `mvn spring-boot:run` would do nothing useful |
| `@ComponentScan` | Spring scans this package (and sub-packages) for `@Controller`, `@Service`, `@Repository`, etc. | `HelloController` would exist as a class, but Spring would never find it or register its `/hello` mapping |

## Why `server.port` and `spring.application.name` live in `application.properties`, not code

Configuration that might change between environments (a different port in a container, a
different service name in production monitoring) belongs outside compiled code - changing a
properties file doesn't require a rebuild. This is the same principle the Java week's Module 7 named
constants for (a value with meaning, kept in exactly one place) applied at the application level
instead of the class level.

## Why the endpoint returns a plain `String`, not a JSON object

There's nothing to structure yet - this lab has no domain data. Returning `String` from a
`@RestController` method produces a `text/plain` response by default. Module 6 (DTOs & Request
Validation) is where a real object gets returned, and Spring Boot's auto-configured Jackson
integration serializes it to JSON automatically, with zero extra configuration.

## What you should NOT have needed to write

No servlet configuration, no `web.xml`, no manual Tomcat setup, no JSON library configuration.
All of that is what `spring-boot-starter-web` and `@EnableAutoConfiguration` handle - worth
naming explicitly what you were spared from, since it's easy to take for granted immediately
after using it once.
