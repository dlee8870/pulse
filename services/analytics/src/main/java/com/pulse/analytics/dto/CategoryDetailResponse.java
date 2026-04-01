package com.pulse.analytics.dto;

import java.util.List;

/** Detailed view of a single category, including its subcategories and aggregated metrics. */
public record CategoryDetailResponse(
        String category,
        long totalPosts,
        double avgSentiment,
        double avgSeverity,
        List<CategoryBreakdown> subcategories
) {
}