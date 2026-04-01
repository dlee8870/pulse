package com.pulse.analytics.dto;

/** Health check response containing service status, name, and version. */
public record HealthResponse(String status, String service, String version) {
}