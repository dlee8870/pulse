package com.pulse.analytics.service;

import com.pulse.analytics.dto.CategoryBreakdown;
import com.pulse.analytics.dto.PatchImpactResponse;
import com.pulse.analytics.dto.PatchImpactResponse.PeriodMetrics;
import com.pulse.analytics.dto.PatchRequest;
import com.pulse.analytics.dto.PatchResponse;
import com.pulse.analytics.exception.ResourceNotFoundException;
import com.pulse.analytics.model.Patch;
import com.pulse.analytics.repository.PatchRepository;
import com.pulse.analytics.repository.ProcessedPostRepository;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;

/**
 * Manages game patches and measures their impact on community sentiment.
 * Compares post metrics from the week before a patch to the week after.
 */
@Service
public class PatchService {

    private static final int IMPACT_WINDOW_DAYS = 7;

    private final PatchRepository patchRepo;
    private final ProcessedPostRepository processedPostRepo;

    public PatchService(PatchRepository patchRepo, ProcessedPostRepository processedPostRepo) {
        this.patchRepo = patchRepo;
        this.processedPostRepo = processedPostRepo;
    }

    /** Saves a new patch record to the database. */
    public PatchResponse createPatch(PatchRequest request) {
        Patch patch = new Patch();
        patch.setVersion(request.version());
        patch.setReleaseDate(request.releaseDate());
        patch.setNotes(request.notes());

        patch = patchRepo.save(patch);
        return toResponse(patch);
    }

    /** Returns all patches ordered by release date, newest first. */
    public List<PatchResponse> getAllPatches() {
        return patchRepo.findAllByOrderByReleaseDateDesc().stream()
                .map(this::toResponse)
                .toList();
    }

    /** Deletes a patch by ID. Throws if the patch doesn't exist. */
    public void deletePatch(UUID patchId) {
        if (!patchRepo.existsById(patchId)) {
            throw new ResourceNotFoundException("Patch not found: " + patchId);
        }
        patchRepo.deleteById(patchId);
    }

    /**
     * Builds a before-vs-after comparison for a patch.
     * Looks at the 7 days before and 7 days after the release date,
     * then calculates changes in volume, sentiment, and severity.
     */
    public PatchImpactResponse getImpact(UUID patchId) {
        Patch patch = patchRepo.findById(patchId)
                .orElseThrow(() -> new ResourceNotFoundException("Patch not found: " + patchId));

        LocalDate releaseDate = patch.getReleaseDate();

        OffsetDateTime preStart = releaseDate.minusDays(IMPACT_WINDOW_DAYS)
                .atStartOfDay(ZoneOffset.UTC).toOffsetDateTime();
        OffsetDateTime preEnd = releaseDate
                .atStartOfDay(ZoneOffset.UTC).toOffsetDateTime();
        OffsetDateTime postStart = preEnd;
        OffsetDateTime postEnd = releaseDate.plusDays(IMPACT_WINDOW_DAYS)
                .atStartOfDay(ZoneOffset.UTC).toOffsetDateTime();

        PeriodMetrics prePatch = buildMetrics(preStart, preEnd);
        PeriodMetrics postPatch = buildMetrics(postStart, postEnd);

        double sentimentChange = postPatch.avgSentiment() - prePatch.avgSentiment();
        double severityChange = postPatch.avgSeverity() - prePatch.avgSeverity();
        long volumeChange = postPatch.postCount() - prePatch.postCount();

        return new PatchImpactResponse(
                toResponse(patch),
                prePatch,
                postPatch,
                round(sentimentChange),
                round(severityChange),
                volumeChange
        );
    }

    /** Aggregates post count, sentiment, severity, and category breakdown for a date range. */
    private PeriodMetrics buildMetrics(OffsetDateTime start, OffsetDateTime end) {
        List<Object[]> rows = processedPostRepo.getMetricsBetween(start, end);

        long count = 0;
        double avgSentiment = 0.0;
        double avgSeverity = 0.0;

        if (!rows.isEmpty()) {
            Object[] row = rows.get(0);
            count = row[0] != null ? ((Number) row[0]).longValue() : 0;
            avgSentiment = row[1] != null ? ((Number) row[1]).doubleValue() : 0.0;
            avgSeverity = row[2] != null ? ((Number) row[2]).doubleValue() : 0.0;
        }

        List<CategoryBreakdown> categories = processedPostRepo
                .getCategoryBreakdownBetween(start, end).stream()
                .map(this::toBreakdown)
                .toList();

        return new PeriodMetrics(count, round(avgSentiment), round(avgSeverity), categories);
    }

    /** Converts a Patch entity into a PatchResponse DTO for the API. */
    private PatchResponse toResponse(Patch patch) {
        return new PatchResponse(
                patch.getId(),
                patch.getVersion(),
                patch.getReleaseDate(),
                patch.getNotes(),
                patch.getCreatedAt()
        );
    }

    /** Converts a raw database row into a typed CategoryBreakdown DTO. */
    private CategoryBreakdown toBreakdown(Object[] row) {
        return new CategoryBreakdown(
                (String) row[0],
                (String) row[1],
                ((Number) row[2]).longValue(),
                round(((Number) row[3]).doubleValue()),
                round(((Number) row[4]).doubleValue())
        );
    }

    private double round(double value) {
        return Math.round(value * 10000.0) / 10000.0;
    }
}
