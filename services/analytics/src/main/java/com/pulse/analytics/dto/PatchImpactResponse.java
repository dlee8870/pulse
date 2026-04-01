package com.pulse.analytics.dto;

import java.util.List;

/** Before-vs-after comparison showing how a patch affected community sentiment and volume. */
public record PatchImpactResponse(
        PatchResponse patch,
        PeriodMetrics prePatch,
        PeriodMetrics postPatch,
        double sentimentChange,
        double severityChange,
        long volumeChange
) {

    /** Aggregated metrics for a specific time period (e.g., the week before or after a patch). */
    public record PeriodMetrics(
            long postCount,
            double avgSentiment,
            double avgSeverity,
            List<CategoryBreakdown> categories
    ) {
    }
}