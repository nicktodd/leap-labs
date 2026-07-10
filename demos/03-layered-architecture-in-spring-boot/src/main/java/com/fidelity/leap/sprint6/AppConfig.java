package com.fidelity.leap.sprint6;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Clock;

// Not every bean comes from a @Component/@Service/@Repository stereotype on a
// class you own. Clock is a JDK class - you can't annotate it. A @Configuration
// class with @Bean methods is how you tell Spring "manage this object too,"
// for anything you didn't write yourself, or want to configure explicitly.
@Configuration
public class AppConfig {

    @Bean
    public Clock clock() {
        return Clock.systemUTC();
    }
}
