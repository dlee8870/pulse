package com.pulse.analytics.service;

import com.pulse.analytics.dto.CategoryBreakdown;
import com.pulse.analytics.dto.CategoryDetailResponse;
import com.pulse.analytics.dto.OverviewResponse;
import com.pulse.analytics.repository.ProcessedPostRepository;
import com.pulse.analytics.repository.RawPostRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class TrendsService {

    private final ProcessedPostRepository processedPostRepo;
    private final RawPostRepository rawPostRepo;

    public TrendsService(ProcessedPostRepository processedPostRepo, RawPostRepository rawPostRepo) {
        this.processedPostRepo = processedPostRepo;
        this.rawPostRepo = rawPostRepo;
    }

    public OverviewResponse getOverview() {
        long totalProcessed = processedPostRepo.count();
        long totalRaw = rawPostRepo.count();

        Double avgSentiment = processedPostRepo.getAverageSentiment();
        Double avgSeverity = processedPostRepo.getAverageSeverity();

        List<CategoryBreakdown> categories = processedPostRepo.getCategoryBreakdown().stream()
                .map(this::toBreakdown)
                .toList();

        return new OverviewResponse(
                totalProcessed,
                totalRaw,
                avgSentiment != null ? round(avgSentiment) : 0.0,
                avgSeverity != null ? round(avgSeverity) : 0.0,
                categories
        );
    }

    public CategoryDetailResponse getCategoryDetail(String category) {
        long totalPosts = processedPostRepo.countByCategory(category);

        List<CategoryBreakdown> subcategories = processedPostRepo.getSubcategoryBreakdown(category).stream()
                .map(this::toBreakdown)
                .toList();

        double avgSentiment = subcategories.stream()
                .mapToDouble(b -> b.avgSentiment() * b.count())
                .sum() / Math.max(1, totalPosts);

        double avgSeverity = subcategories.stream()
                .mapToDouble(b -> b.avgSeverity() * b.count())
                .sum() / Math.max(1, totalPosts);

        return new CategoryDetailResponse(
                category,
                totalPosts,
                round(avgSentiment),
                round(avgSeverity),
                subcategories
        );
    }

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
