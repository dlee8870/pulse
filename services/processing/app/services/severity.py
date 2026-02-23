import math


class SeverityScorer:
    def __init__(
        self,
        sentiment_weight: float = 0.30,
        engagement_weight: float = 0.35,
        keyword_weight: float = 0.20,
        volume_weight: float = 0.15,
    ):
        self.sentiment_weight = sentiment_weight
        self.engagement_weight = engagement_weight
        self.keyword_weight = keyword_weight
        self.volume_weight = volume_weight

    def score(
        self,
        sentiment_score: float,
        post_score: int,
        comment_count: int,
        category: str,
    ) -> float:
        if category == "positive":
            return round(max(0.0, 0.05 + abs(sentiment_score) * 0.1), 3)

        sentiment_severity = abs(min(0.0, sentiment_score))

        engagement_raw = post_score + (comment_count * 2)
        engagement_severity = min(1.0, math.log1p(engagement_raw) / math.log1p(10000))

        category_multipliers = {
            "gameplay-bug": 0.9,
            "server-issue": 0.85,
            "balance": 0.7,
            "ui-bug": 0.6,
            "market": 0.5,
            "feature-request": 0.4,
            "other": 0.3,
        }
        category_severity = category_multipliers.get(category, 0.4)

        comment_ratio = min(1.0, comment_count / max(1, post_score)) if post_score > 0 else 0.5
        volume_severity = min(1.0, comment_ratio * 1.5)

        raw_score = (
            self.sentiment_weight * sentiment_severity
            + self.engagement_weight * engagement_severity
            + self.keyword_weight * category_severity
            + self.volume_weight * volume_severity
        )

        return round(min(1.0, max(0.0, raw_score)), 3)