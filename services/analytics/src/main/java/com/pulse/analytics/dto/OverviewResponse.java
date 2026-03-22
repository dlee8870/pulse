package com.pulse.analytics.dto;

import java.util.List;

public record OverviewResponse(
        long totalProcessed,
        long totalRaw,
        double avgSentiment,
        double avgSeverity,
        List<CategoryBreakdown> categories
) {
}
