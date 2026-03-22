package com.pulse.analytics.repository;

import com.pulse.analytics.model.RawPost;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RawPostRepository extends JpaRepository<RawPost, UUID> {
}
