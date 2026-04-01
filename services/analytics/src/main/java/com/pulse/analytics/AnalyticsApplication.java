package com.pulse.analytics;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point for the Pulse Analytics Service.
 * Bootstraps the Spring Boot application and auto-configures all components.
 */
@SpringBootApplication
public class AnalyticsApplication {

    public static void main(String[] args) {
        SpringApplication.run(AnalyticsApplication.class, args);
    }
}