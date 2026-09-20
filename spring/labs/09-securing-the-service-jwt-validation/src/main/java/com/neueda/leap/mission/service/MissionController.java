package com.neueda.leap.mission.service;

import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MissionController {

    @GetMapping("/public")
    public String publicEndpoint() {
        return "No token required - anyone can see this.";
    }

    // KATA B: this endpoint compiles and (once SecurityConfig is correct)
    // correctly rejects requests with no token. But test it with a REAL,
    // valid token from the auth stub and you'll get a 500 with a stack
    // trace that doesn't look like a JWT problem at all. Use GenAI to help
    // you interpret what's actually happening before you fix it yourself -
    // see the lab README for the exact prompt to try.
    @GetMapping("/mission")
    public String missionEndpoint(Jwt jwt) {
        String username = jwt.getSubject();
        return "Classified mission data - authorised for " + username;
    }
}
