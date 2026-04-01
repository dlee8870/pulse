package com.pulse.analytics.controller;

import com.pulse.analytics.dto.HealthResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Exposes a health check endpoint for monitoring and Docker health probes. */
@RestController
public class HealthController {

    @Value("${app.version}")
    private String version;

    /** Returns the current health status, service name, and version. */
    @GetMapping("/health")
    public HealthResponse health() {
        return new HealthResponse("healthy", "analytics", version);
    }
}