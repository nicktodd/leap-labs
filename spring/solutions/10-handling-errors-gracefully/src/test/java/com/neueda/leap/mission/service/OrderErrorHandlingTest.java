package com.neueda.leap.mission.service;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

// Pre-written - do not modify. Exercises every handler in
// GlobalExceptionHandler against the real, running service.
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderErrorHandlingTest {

    @Autowired
    private TestRestTemplate rest;

    private HttpEntity<String> json(String body) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return new HttpEntity<>(body, headers);
    }

    @Test
    void aValidOrderIsAccepted() {
        var response = rest.postForEntity("/orders",
                json("{\"ticker\":\"AAPL\",\"instrumentType\":\"EQUITY\",\"quantity\":100,\"price\":150.0,\"side\":\"BUY\"}"),
                OrderResponseDto.class);
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
    }

    @Test
    void aMalformedOrderReturns400WithFieldErrors() {
        ResponseEntity<ErrorResponse> response = rest.postForEntity("/orders",
                json("{\"instrumentType\":\"EQUITY\",\"quantity\":-5,\"price\":150.0,\"side\":\"BUY\"}"),
                ErrorResponse.class);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        ErrorResponse body = response.getBody();
        assertEquals(400, body.status());
        assertFalse(body.fieldErrors().isEmpty(), "expected at least one field error");
    }

    @Test
    void anUnknownOrderIdReturns404() {
        ResponseEntity<ErrorResponse> response = rest.getForEntity("/orders/does-not-exist", ErrorResponse.class);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals(404, response.getBody().status());
        assertTrue(response.getBody().message().contains("does-not-exist"));
    }

    @Test
    void anUnknownTickerReturns404() {
        ResponseEntity<ErrorResponse> response = rest.postForEntity("/orders",
                json("{\"ticker\":\"NOTREAL\",\"instrumentType\":\"EQUITY\",\"quantity\":100,\"price\":150.0,\"side\":\"BUY\"}"),
                ErrorResponse.class);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertEquals(404, response.getBody().status());
    }

    @Test
    void aTradeOverTheLimitReturns422() {
        ResponseEntity<ErrorResponse> response = rest.postForEntity("/orders",
                json("{\"ticker\":\"AAPL\",\"instrumentType\":\"EQUITY\",\"quantity\":100000,\"price\":150.0,\"side\":\"BUY\"}"),
                ErrorResponse.class);

        assertEquals(HttpStatus.UNPROCESSABLE_ENTITY, response.getStatusCode());
        assertEquals(422, response.getBody().status());
    }
}
