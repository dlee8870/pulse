package com.pulse.analytics.dto;

import java.time.LocalDate;

/** Request body for registering a new game patch. */
public record PatchRequest(
        String version,
        LocalDate releaseDate,
        String notes
) {
}