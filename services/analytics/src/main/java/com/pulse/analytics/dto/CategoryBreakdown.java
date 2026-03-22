package com.pulse.analytics.dto;

public record CategoryBreakdown(
        String category,
        String subcategory,
        long count,
        double avgSentiment,
        double avgSeverity
) {
}
