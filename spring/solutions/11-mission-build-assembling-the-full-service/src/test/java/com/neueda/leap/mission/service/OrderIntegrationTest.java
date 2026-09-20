package com.neueda.leap.mission.service;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import static org.junit.jupiter.api.Assertions.*;

// Pre-written - do not modify. Exercises the REAL, assembled service: real
// Postgres (via AccountMapper), a real JWT from the real running auth stub,
// real domain logic. Prerequisites (see README): the local mission Postgres
// database and the auth stub must both be running before you run this.
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderIntegrationTest {

    @Autowired
    private TestRestTemplate rest;

    private static String token;

    @BeforeAll
    static void fetchToken() throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:4000/login"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString("{\"username\":\"alice\",\"password\":\"mission123\"}"))
                .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        assertEquals(200, response.statusCode(),
                "Could not reach the auth stub on localhost:4000 - is it running? (npm start in shared/auth-stub)");
        String body = response.body();
        token = body.substring(body.indexOf(":\"") + 2, body.lastIndexOf("\""));
    }

    private HttpEntity<String> authedJson(String body) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(token);
        return new HttpEntity<>(body, headers);
    }

    private HttpEntity<String> unauthedJson(String body) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return new HttpEntity<>(body, headers);
    }

    @Test
    void aRequestWithNoTokenIsRejected() {
        ResponseEntity<String> response = rest.postForEntity("/accounts/1/orders",
                unauthedJson("{\"ticker\":\"ULVR.L\",\"instrumentType\":\"EQUITY\",\"quantity\":10,\"price\":40.0,\"side\":\"BUY\"}"),
                String.class);
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }

    @Test
    void aValidBuyOrderIsAcceptedAndPersisted() {
        ResponseEntity<OrderResponseDto> response = rest.exchange("/accounts/1/orders",
                org.springframework.http.HttpMethod.POST,
                authedJson("{\"ticker\":\"ULVR.L\",\"instrumentType\":\"EQUITY\",\"quantity\":10,\"price\":40.0,\"side\":\"BUY\"}"),
                OrderResponseDto.class);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("ACCEPTED", response.getBody().status());
        assertEquals(0.4, response.getBody().fee(), 0.001); // 10 * 40.0 * 0.001 (equity commission)
    }

    @Test
    void sellingMoreThanHeldIsRejected() {
        ResponseEntity<ErrorResponse> response = rest.exchange("/accounts/1/orders",
                org.springframework.http.HttpMethod.POST,
                authedJson("{\"ticker\":\"ULVR.L\",\"instrumentType\":\"EQUITY\",\"quantity\":999999,\"price\":40.0,\"side\":\"SELL\"}"),
                ErrorResponse.class);

        assertEquals(HttpStatus.UNPROCESSABLE_ENTITY, response.getStatusCode());
        assertEquals(422, response.getBody().status());
    }

    @Test
    void anUnknownTickerReturns404() {
        ResponseEntity<ErrorResponse> response = rest.exchange("/accounts/1/orders",
                org.springframework.http.HttpMethod.POST,
                authedJson("{\"ticker\":\"NOTREAL\",\"instrumentType\":\"EQUITY\",\"quantity\":10,\"price\":1.0,\"side\":\"BUY\"}"),
                ErrorResponse.class);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void aMalformedRequestReturns400WithFieldErrors() {
        ResponseEntity<ErrorResponse> response = rest.exchange("/accounts/1/orders",
                org.springframework.http.HttpMethod.POST,
                authedJson("{\"instrumentType\":\"EQUITY\",\"quantity\":-5,\"price\":40.0,\"side\":\"BUY\"}"),
                ErrorResponse.class);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertFalse(response.getBody().fieldErrors().isEmpty());
    }
}
