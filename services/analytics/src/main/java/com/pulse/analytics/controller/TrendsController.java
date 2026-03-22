package com.pulse.analytics.controller;

import com.pulse.analytics.dto.CategoryDetailResponse;
import com.pulse.analytics.dto.OverviewResponse;
import com.pulse.analytics.service.TrendsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/trends")
public class TrendsController {

    private final TrendsService trendsService;

    public TrendsController(TrendsService trendsService) {
        this.trendsService = trendsService;
    }

    @GetMapping("/overview")
    public OverviewResponse getOverview() {
        return trendsService.getOverview();
    }

    @GetMapping("/{category}")
    public CategoryDetailResponse getCategoryDetail(@PathVariable String category) {
        return trendsService.getCategoryDetail(category);
    }
}
