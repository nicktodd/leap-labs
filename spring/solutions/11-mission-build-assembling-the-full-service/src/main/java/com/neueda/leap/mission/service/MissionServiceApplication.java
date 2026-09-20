package com.neueda.leap.mission.service;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.neueda.leap.mission.service")
public class MissionServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(MissionServiceApplication.class, args);
    }
}
