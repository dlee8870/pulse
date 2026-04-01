package com.pulse.analytics.repository;

import com.pulse.analytics.model.Patch;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

/** Provides CRUD access to the patches table. */
public interface PatchRepository extends JpaRepository<Patch, UUID> {

    /** Returns all patches sorted by release date, newest first. */
    List<Patch> findAllByOrderByReleaseDateDesc();
}