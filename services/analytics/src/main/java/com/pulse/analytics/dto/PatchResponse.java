package com.pulse.analytics.dto;

import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

public record PatchResponse(
        UUID id,
        String version,
        LocalDate releaseDate,
        String notes,
        Instant createdAt
) {
}
