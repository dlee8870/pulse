package com.pulse.analytics.dto;

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
