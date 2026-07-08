"""Severity scoring driven by sentiment intensity, weighted by category, with engagement as a bonus."""

import math


class SeverityScorer:
    """Produces a 0.0 to 1.0 urgency score for a single post."""

    CATEGORY_MULTIPLIERS = {
        "gameplay-bug": 0.9,
        "server-issue": 0.85,
        "technical": 0.85,
        "balance": 0.7,
        "monetization": 0.55,
        "ui-bug": 0.6,
        "market": 0.5,
        "feature-request": 0.4,
        "other": 0.3,
    }

    def score(
        self,
        sentiment_score: float,
        post_score: int,
        comment_count: int,
        category: str,
    ) -> float:
        """Calculate severity from 0.0 (not urgent) to 1.0 (critical)."""
        if category == "positive":
            return round(max(0.0, 0.05 + abs(sentiment_score) * 0.1), 3)

        sentiment_severity = abs(min(0.0, sentiment_score))
        category_severity = self.CATEGORY_MULTIPLIERS.get(category, 0.4)

        engagement_raw = post_score + (comment_count * 2)
        engagement_bonus = min(0.1, math.log1p(engagement_raw) / math.log1p(500) * 0.1)

        raw_score = sentiment_severity * (0.7 + 0.3 * category_severity) + engagement_bonus

        return round(min(1.0, max(0.0, raw_score)), 3)