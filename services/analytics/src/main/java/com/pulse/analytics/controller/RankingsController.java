package com.pulse.analytics.controller;

import com.pulse.analytics.dto.RankingEntry;
import com.pulse.analytics.service.RankingService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Serves the ranked list of community issues ordered by composite severity. */
@RestController
@RequestMapping("/api/rankings")
public class RankingsController {

    private final RankingService rankingService;

    public RankingsController(RankingService rankingService) {
        this.rankingService = rankingService;
    }

    /** Returns all issue subcategories ranked from most severe to least severe. */
    @GetMapping
    public List<RankingEntry> getRankings() {
        return rankingService.getRankings();
    }
}