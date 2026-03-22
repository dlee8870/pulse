package com.pulse.analytics.controller;

import com.pulse.analytics.dto.HealthResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

    @Value("${app.version}")
    private String version;

    @GetMapping("/health")
    public HealthResponse health() {
        return new HealthResponse("healthy", "analytics", version);
    }
}
