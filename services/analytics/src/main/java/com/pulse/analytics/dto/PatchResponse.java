package com.pulse.analytics.dto;

import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

/** API response for a registered game patch. */
public record PatchResponse(
        UUID id,
        String version,
        LocalDate releaseDate,
        String notes,
        Instant createdAt
) {
}