package com.neueda.leap;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Greeter greeter = new Greeter();
        System.out.println(greeter.greet("Week 2"));
        System.out.println("Container is up. Sleeping so you can docker ps / docker logs / docker exec into it.");
        Thread.sleep(600_000);
    }
}
