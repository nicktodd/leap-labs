package com.neueda.leap.mission.service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

// @RestController = @Controller + @ResponseBody: every method's return value
// is written directly to the HTTP response body (as JSON, if it's an object),
// rather than being resolved to a view template.
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from the mission service";
    }
}
