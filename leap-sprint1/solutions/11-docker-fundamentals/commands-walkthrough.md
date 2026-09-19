# Module 11 Lab — Commands Walkthrough (Instructor Reference)

```bash
cd starter
mvn clean package
# target/sprint1-greeter-app-0.1.0.jar now exists

docker build -t sprint1-greeter-app .
docker images
# REPOSITORY             TAG      IMAGE ID       SIZE
# sprint1-greeter-app    latest   ...            ~180MB

docker run -d --name greeter sprint1-greeter-app
docker ps
# CONTAINER ID   IMAGE                 ...   NAMES
# ...            sprint1-greeter-app   ...   greeter

docker logs greeter
# Good day, Sprint 1
# Container is up. Sleeping so you can docker ps / docker logs / docker exec into it.

docker exec -it greeter sh
# /app # ls
# app.jar
# /app # exit

docker stop greeter
docker rm greeter
```

## Answer key: multi-stage build

A multi-stage Dockerfile uses more than one `FROM` line, each starting a new, independent
build stage. Only the *last* stage's contents end up in the final image; earlier stages are
just used to produce artifacts (like a compiled jar) that later stages copy in with
`COPY --from=<stage>`. This means the final image doesn't carry the full Maven/JDK toolchain
used to build the jar, only the small JRE runtime needed to run it, which is why it ends up
significantly smaller.
