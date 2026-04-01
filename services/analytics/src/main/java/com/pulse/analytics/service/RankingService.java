package com.pulse.analytics.service;

import com.pulse.analytics.dto.RankingEntry;
import com.pulse.analytics.repository.ProcessedPostRepository;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import org.springframework.stereotype.Service;

/** Ranks community issues by a composite score combining severity, sentiment, and volume. */
@Service
public class RankingService {

    private final ProcessedPostRepository processedPostRepo;

    public RankingService(ProcessedPostRepository processedPostRepo) {
        this.processedPostRepo = processedPostRepo;
    }

    /** Scores and ranks all non-positive subcategories, returning them from most severe to least. */
    public List<RankingEntry> getRankings() {
        List<Object[]> data = processedPostRepo.getRankingData();

        List<RankingEntry> entries = new ArrayList<>();
        for (Object[] row : data) {
            String category = (String) row[0];
            String subcategory = (String) row[1];
            long count = ((Number) row[2]).longValue();
            double avgSentiment = ((Number) row[3]).doubleValue();
            double avgSeverity = ((Number) row[4]).doubleValue();

            double compositeScore = computeComposite(count, avgSentiment, avgSeverity);

            entries.add(new RankingEntry(
                    0,
                    category,
                    subcategory,
                    count,
                    round(avgSentiment),
                    round(avgSeverity),
                    round(compositeScore)
            ));
        }

        entries.sort(Comparator.comparingDouble(RankingEntry::compositeScore).reversed());

        List<RankingEntry> ranked = new ArrayList<>();
        for (int i = 0; i < entries.size(); i++) {
            RankingEntry e = entries.get(i);
            ranked.add(new RankingEntry(
                    i + 1,
                    e.category(),
                    e.subcategory(),
                    e.postCount(),
                    e.avgSentiment(),
                    e.avgSeverity(),
                    e.compositeScore()
            ));
        }

        return ranked;
    }

    /**
     * Calculates a composite score from 0.0 to ~1.0.
     * Weights: 40% severity, 30% negative sentiment intensity, 30% log-scaled volume.
     */
    private double computeComposite(long count, double avgSentiment, double avgSeverity) {
        double volumeFactor = Math.log1p(count) / Math.log1p(100);
        double sentimentFactor = Math.abs(Math.min(0, avgSentiment));
        return (avgSeverity * 0.4) + (sentimentFactor * 0.3) + (volumeFactor * 0.3);
    }

    private double round(double value) {
        return Math.round(value * 10000.0) / 10000.0;
    }
}