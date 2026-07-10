package com.fidelity.leap.sprint6;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// @SpringBootApplication is three annotations in one:
// - @Configuration: this class can define Spring beans
// - @EnableAutoConfiguration: Spring Boot configures things for you based on
//   what's on the classpath (spring-boot-starter-web on the classpath -> an
//   embedded Tomcat gets configured automatically, no XML, no manual wiring)
// - @ComponentScan: Spring looks for @Controller, @Service, etc. in this
//   package and everything under it
@SpringBootApplication
public class MissionServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(MissionServiceApplication.class, args);
    }
}
