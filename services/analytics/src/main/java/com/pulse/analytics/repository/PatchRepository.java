package com.pulse.analytics.repository;

import com.pulse.analytics.model.Patch;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PatchRepository extends JpaRepository<Patch, UUID> {

    List<Patch> findAllByOrderByReleaseDateDesc();
}
