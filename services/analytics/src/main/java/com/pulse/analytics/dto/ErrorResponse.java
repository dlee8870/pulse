package com.pulse.analytics.dto;

import java.time.OffsetDateTime;

/** Standard API error response. */
public record ErrorResponse(
        OffsetDateTime timestamp,
        int status,
        String error,
        String message,
        String path
) {
}
