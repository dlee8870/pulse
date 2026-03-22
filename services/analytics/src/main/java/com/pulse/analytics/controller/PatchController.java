package com.pulse.analytics.controller;

import com.pulse.analytics.dto.PatchImpactResponse;
import com.pulse.analytics.dto.PatchRequest;
import com.pulse.analytics.dto.PatchResponse;
import com.pulse.analytics.service.PatchService;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/patches")
public class PatchController {

    private final PatchService patchService;

    public PatchController(PatchService patchService) {
        this.patchService = patchService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public PatchResponse createPatch(@RequestBody PatchRequest request) {
        return patchService.createPatch(request);
    }

    @GetMapping
    public List<PatchResponse> getAllPatches() {
        return patchService.getAllPatches();
    }

    @GetMapping("/{id}/impact")
    public PatchImpactResponse getPatchImpact(@PathVariable UUID id) {
        return patchService.getImpact(id);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deletePatch(@PathVariable UUID id) {
        patchService.deletePatch(id);
    }
}