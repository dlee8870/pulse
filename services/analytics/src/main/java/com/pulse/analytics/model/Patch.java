package com.pulse.analytics.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

/** Represents a game patch or title update, used for before-vs-after impact analysis. */
@Entity
@Table(name = "patches")
public class Patch {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String version;

    @Column(name = "release_date", nullable = false)
    private LocalDate releaseDate;

    private String notes;

    @Column(name = "created_at")
    private Instant createdAt = Instant.now();

    public UUID getId() { return id; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public LocalDate getReleaseDate() { return releaseDate; }
    public void setReleaseDate(LocalDate releaseDate) { this.releaseDate = releaseDate; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }

    public Instant getCreatedAt() { return createdAt; }
}