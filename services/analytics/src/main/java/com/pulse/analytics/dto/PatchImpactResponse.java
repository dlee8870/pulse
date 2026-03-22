package com.pulse.analytics.dto;

import java.util.List;

public record PatchImpactResponse(
        PatchResponse patch,
        PeriodMetrics prePatch,
        PeriodMetrics postPatch,
        double sentimentChange,
        double severityChange,
        long volumeChange
) {

    public record PeriodMetrics(
            long postCount,
            double avgSentiment,
            double avgSeverity,
            List<CategoryBreakdown> categories
    ) {
    }
}
