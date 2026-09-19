# Going Further — Extending Your Docker Image

Finished early? Here are some ways to build on the single-stage Dockerfile you just wrote. Pick
whichever looks interesting — you don't need to do all of them. They build roughly in order of
difficulty.

If you get stuck, the [`solutions/`](solutions) folder has worked answers — but try it yourself
first. Note the solution Dockerfiles `COPY pom.xml`/`COPY src` like a multi-stage build does, so
if you build one directly you'll need to point the build **context** at `starter/`, e.g.:

```
docker build -f solutions/Dockerfile_GoingFurther -t sprint1-greeter-app:going-further starter/
```

## 1. Write the real multi-stage version yourself

In Part A you read a multi-stage Dockerfile and explained why it produces a smaller image. Now
write one yourself for this app, so the image build no longer depends on `mvn clean package`
having already been run on the host.

**Hints:** you need two `FROM` lines — a build stage based on a Maven image that compiles the jar,
and a runtime stage (same base you already used) that copies *only* the jar out of the build stage
with `COPY --from=`. Once it's building, compare `docker images` output against your original
single-stage image and check the size difference actually shows up.

## 2. Shrink the image further

Try swapping the runtime base image for a "distroless" one (e.g. `gcr.io/distroless/java21-debian12`)
and compare sizes again.

**Hints:** distroless images have no shell — try `docker exec -it <name> sh` against a container
from this image afterwards and see what happens. Think about why that trade-off might or might not
matter for a production image versus one you need to debug.

## 3. Add a HEALTHCHECK

Right now `docker ps` only tells you the container is *running*, not whether the app inside is
actually OK.

**Hints:** the `HEALTHCHECK` instruction runs a command inside the container on an interval; a
non-zero exit code marks it unhealthy. You don't need anything fancy — checking that the `java`
process is still alive is enough to see the `STATUS` column in `docker ps` change to
`(healthy)`.

## 4. Make the greeting configurable at runtime

Currently the greeted name is hardcoded in `Main.java`. Change it so it can be set without
rebuilding the image.

**Hints:** Java reads environment variables via `System.getenv()`. Give it a sensible default so
the image still works if nobody sets anything. Once the code change is in and rebuilt, run two
containers from the *same* image passing different `-e` values and confirm they greet differently.

## 5. Persist something with a volume

Container filesystems disappear with the container. Prove that to yourself by making the app
write its greeting to a log file, then keeping that file around after the container is gone.

**Hints:** you'll need the app to write to a file path inside the container (pick something under
`/app`), and a `docker run -v` bind mount or named volume pointing at that same path. Remove the
container afterwards and check the file is still there on the host/volume.

## 6. Run as a non-root user

By default your process runs as root inside the container — not great practice.

**Hints:** look at `addgroup`/`adduser` (this base image is Alpine-based) and the `USER`
instruction. Watch out for file permissions — if your app writes anywhere (e.g. the log file from
option 5), that directory needs to be owned by the user you switch to, not root.

## Stretch: wrap it in Docker Compose

Take whichever image you've built and describe it declaratively instead of typing out a long
`docker run` command each time.

**Hints:** a minimal `docker-compose.yml` needs a service name, an `image`, and whichever of
`ports`/`environment`/`volumes` your version of the image needs. Try `docker compose up -d` and
`docker compose logs` and compare the experience to typing the equivalent `docker run` flags by
hand.
