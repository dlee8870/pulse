package com.pulse.analytics.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

/**
 * Read-only mapping of the raw_posts table.
 * This table is owned by the Ingestion Service — Analytics only reads from it.
 */
@Entity
@Table(name = "raw_posts")
public class RawPost {

    @Id
    private UUID id;

    private String source;

    @Column(name = "source_id")
    private String sourceId;

    private String subreddit;
    private String title;
    private String body;
    private String author;
    private int score;

    @Column(name = "comment_count")
    private int commentCount;

    private String flair;
    private String url;

    @Column(name = "posted_at")
    private Instant postedAt;

    @Column(name = "ingested_at")
    private Instant ingestedAt;

    private boolean processed;

    public UUID getId() { return id; }
    public String getSource() { return source; }
    public String getSourceId() { return sourceId; }
    public String getSubreddit() { return subreddit; }
    public String getTitle() { return title; }
    public String getBody() { return body; }
    public String getAuthor() { return author; }
    public int getScore() { return score; }
    public int getCommentCount() { return commentCount; }
    public String getFlair() { return flair; }
    public String getUrl() { return url; }
    public Instant getPostedAt() { return postedAt; }
    public Instant getIngestedAt() { return ingestedAt; }
    public boolean isProcessed() { return processed; }
}