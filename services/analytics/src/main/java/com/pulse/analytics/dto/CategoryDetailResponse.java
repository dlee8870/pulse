package com.pulse.analytics.dto;

import java.util.List;

public record CategoryDetailResponse(
        String category,
        long totalPosts,
        double avgSentiment,
        double avgSeverity,
        List<CategoryBreakdown> subcategories
) {
}
