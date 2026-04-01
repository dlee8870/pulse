package com.pulse.analytics.repository;

import com.pulse.analytics.model.ProcessedPost;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

/** Queries processed_posts for aggregated metrics, category breakdowns, and ranking data. */
public interface ProcessedPostRepository extends JpaRepository<ProcessedPost, UUID> {

    /** Groups all posts by top-level category and returns counts with average scores. */
    @Query(value = """
            SELECT pp.category, CAST(NULL AS VARCHAR) AS subcategory, COUNT(*) AS cnt,
                   AVG(pp.sentiment_score) AS avg_sentiment, AVG(pp.severity_score) AS avg_severity
            FROM processed_posts pp
            GROUP BY pp.category
            ORDER BY cnt DESC
            """, nativeQuery = true)
    List<Object[]> getCategoryBreakdown();

    /** Breaks a single category into its subcategories with counts and average scores. */
    @Query(value = """
            SELECT pp.category, pp.subcategory, COUNT(*) AS cnt,
                   AVG(pp.sentiment_score) AS avg_sentiment, AVG(pp.severity_score) AS avg_severity
            FROM processed_posts pp
            WHERE pp.category = :category
            GROUP BY pp.category, pp.subcategory
            ORDER BY cnt DESC
            """, nativeQuery = true)
    List<Object[]> getSubcategoryBreakdown(@Param("category") String category);

    /** Returns ranking data for all non-positive subcategories, used by the severity ranker. */
    @Query(value = """
            SELECT pp.category, pp.subcategory, COUNT(*) AS cnt,
                   AVG(pp.sentiment_score) AS avg_sentiment, AVG(pp.severity_score) AS avg_severity
            FROM processed_posts pp
            WHERE pp.category != 'positive'
            GROUP BY pp.category, pp.subcategory
            ORDER BY cnt DESC
            """, nativeQuery = true)
    List<Object[]> getRankingData();

    /** Returns the average sentiment score across all processed posts. */
    @Query("SELECT AVG(p.sentimentScore) FROM ProcessedPost p")
    Double getAverageSentiment();

    /** Returns the average severity score across all processed posts. */
    @Query("SELECT AVG(p.severityScore) FROM ProcessedPost p")
    Double getAverageSeverity();

    /** Returns post count, average sentiment, and average severity for a given date range. */
    @Query(value = """
            SELECT COUNT(*), AVG(pp.sentiment_score), AVG(pp.severity_score)
            FROM processed_posts pp
            JOIN raw_posts rp ON pp.raw_post_id = rp.id
            WHERE rp.posted_at >= :startDate AND rp.posted_at < :endDate
            """, nativeQuery = true)
    List<Object[]> getMetricsBetween(@Param("startDate") OffsetDateTime startDate,
                                     @Param("endDate") OffsetDateTime endDate);

    /** Returns category/subcategory breakdown for posts within a specific date range. */
    @Query(value = """
            SELECT pp.category, pp.subcategory, COUNT(*) AS cnt,
                   AVG(pp.sentiment_score) AS avg_sentiment, AVG(pp.severity_score) AS avg_severity
            FROM processed_posts pp
            JOIN raw_posts rp ON pp.raw_post_id = rp.id
            WHERE rp.posted_at >= :startDate AND rp.posted_at < :endDate
            GROUP BY pp.category, pp.subcategory
            ORDER BY cnt DESC
            """, nativeQuery = true)
    List<Object[]> getCategoryBreakdownBetween(@Param("startDate") OffsetDateTime startDate,
                                               @Param("endDate") OffsetDateTime endDate);

    /** Counts how many processed posts belong to a given category. */
    long countByCategory(String category);
}