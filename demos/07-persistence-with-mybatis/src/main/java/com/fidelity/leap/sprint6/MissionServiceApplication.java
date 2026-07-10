package com.fidelity.leap.sprint6;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// @MapperScan registers every mapper interface in this package as a Spring
// bean - both the annotation-based InstrumentMapper and the XML-based
// HoldingMapper, which has no @Mapper annotation of its own.
@SpringBootApplication
@MapperScan("com.fidelity.leap.sprint6")
public class MissionServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(MissionServiceApplication.class, args);
    }
}
