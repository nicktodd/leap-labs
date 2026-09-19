// Solution for goingfurther.md options 4 (configurable greeting via env var) and 5 (persist a
// log to a mounted volume). Drop this in as starter/src/main/java/com/neueda/leap/Main.java in
// place of the original, rebuild the jar, then rebuild the image from Dockerfile_GoingFurther
// (which already declares GREETING_NAME and VOLUME /app/logs to match).
//
// Try it with, e.g.:
//   docker run -d --name greeter -e GREETING_NAME=Class -v greeter-logs:/app/logs sprint1-greeter-app:going-further

package com.neueda.leap;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Main {
    public static void main(String[] args) throws InterruptedException, IOException {
        String name = System.getenv().getOrDefault("GREETING_NAME", "Sprint 1");
        Greeter greeter = new Greeter();
        String message = greeter.greet(name);
        System.out.println(message);

        try (PrintWriter log = new PrintWriter(new FileWriter("/app/logs/greeting.log", true))) {
            log.println(message);
        }

        System.out.println("Container is up. Sleeping so you can docker ps / docker logs / docker exec into it.");
        Thread.sleep(600_000);
    }
}
