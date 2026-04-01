package com.pulse.analytics.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

/**
 * Read-only mapping of the processed_posts table.
 * This table is owned by the Processing Service — Analytics only reads from it.
 * Each processed post links back to its original raw post.
 */
@Entity
@Table(name = "processed_posts")
public class ProcessedPost {

    @Id
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "raw_post_id", nullable = false)
    private RawPost rawPost;

    private String category;
    private String subcategory;

    @Column(name = "sentiment_score")
    private double sentimentScore;

    @Column(name = "severity_score")
    private double severityScore;

    @JdbcTypeCode(SqlTypes.JSON)
    private List<String> keywords;

    @Column(name = "processed_at")
    private Instant processedAt;

    public UUID getId() { return id; }
    public RawPost getRawPost() { return rawPost; }
    public String getCategory() { return category; }
    public String getSubcategory() { return subcategory; }
    public double getSentimentScore() { return sentimentScore; }
    public double getSeverityScore() { return severityScore; }
    public List<String> getKeywords() { return keywords; }
    public Instant getProcessedAt() { return processedAt; }
}