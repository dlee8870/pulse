package com.pulse.analytics.dto;

import java.time.LocalDate;

public record PatchRequest(
        String version,
        LocalDate releaseDate,
        String notes
) {
}
