package com.neueda.leap.sprint6;

// Given - result-mapping class for Kata A. Field names deliberately match
// the (snake_case-to-camelCase-converted) columns on the advisors table.
public class Advisor {
    private int advisorId;
    private String name;
    private String region;

    public int getAdvisorId() {
        return advisorId;
    }

    public void setAdvisorId(int advisorId) {
        this.advisorId = advisorId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }
}
