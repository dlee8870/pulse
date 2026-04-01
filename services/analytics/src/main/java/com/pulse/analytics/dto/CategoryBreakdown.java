package com.pulse.analytics.dto;

/** A single category or subcategory with its post count and average scores. */
public record CategoryBreakdown(
        String category,
        String subcategory,
        long count,
        double avgSentiment,
        double avgSeverity
) {
}