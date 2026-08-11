package com.neueda.leap.sprint6;

import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MissionController {

    @GetMapping("/public")
    public String publicEndpoint() {
        return "No token required - anyone can see this.";
    }

    @GetMapping("/mission")
    public String missionEndpoint(@AuthenticationPrincipal Jwt jwt) {
        String username = jwt.getSubject();
        return "Classified mission data - authorised for " + username;
    }
}
