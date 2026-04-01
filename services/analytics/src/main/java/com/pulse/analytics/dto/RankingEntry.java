package com.pulse.analytics.dto;

/** A ranked community issue with its position, metrics, and composite severity score. */
public record RankingEntry(
        int rank,
        String category,
        String subcategory,
        long postCount,
        double avgSentiment,
        double avgSeverity,
        double compositeScore
) {
}