package com.pulse.analytics.repository;

import com.pulse.analytics.model.RawPost;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

/** Provides read-only access to raw_posts. Only uses the inherited count() method. */
public interface RawPostRepository extends JpaRepository<RawPost, UUID> {
}