"""Sentiment analysis using a pre-trained HuggingFace model with gaming-context corrections."""

import logging
import re

from transformers import pipeline

logger = logging.getLogger(__name__)

SARCASM_PATTERNS = [
    r"literally perfect",
    r"absurdly perfect",
    r"perfectly\b.*\bunfair",
    r"perfect.*\bbut\b",
    r"perfect.*\bfeel",
    r"\bperfect\b.*\brather than\b",
]

NEGATIVE_CONTEXT_PHRASES = [
    "broken", "ruined", "worst", "terrible", "unplayable", "embarrassing",
    "frustrating", "useless", "clueless", "dead", "unfair", "ridiculous",
    "absurd", "needs to change", "needs a complete", "needs to be fixed",
    "how is there still", "still a thing", "wrong fix", "completely broken",
]


class SentimentAnalyzer:
    """Scores text from -1.0 (very negative) to +1.0 (very positive).

    Layers domain-specific corrections on top of the model's raw output
    to handle sarcasm and gaming language the model doesn't understand.
    """

    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """Load the sentiment model into memory."""
        logger.info("Loading sentiment model: %s", model_name)
        self._pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name,
            truncation=True,
            max_length=512,
            top_k=None,
        )
        logger.info("Sentiment model loaded")

    def _detect_sarcasm(self, text: str) -> bool:
        """Check for sarcasm patterns like 'literally perfect' used as complaints."""
        text_lower = text.lower()
        for pattern in SARCASM_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False

    def _count_negative_context(self, text: str) -> int:
        """Count negative gaming phrases in the text."""
        text_lower = text.lower()
        return sum(1 for phrase in NEGATIVE_CONTEXT_PHRASES if phrase in text_lower)

    def analyze(self, text: str, category: str | None = None) -> float:
        """Return a sentiment score from -1.0 to +1.0 for the given text."""
        if not text or not text.strip():
            return 0.0

        results = self._pipeline(text[:512])[0]

        scores_by_label = {}
        for item in results:
            label = item["label"].lower()
            scores_by_label[label] = item["score"]

        positive = scores_by_label.get("positive", 0.0)
        negative = scores_by_label.get("negative", 0.0)
        neutral = scores_by_label.get("neutral", 0.0)

        sentiment = positive - negative

        if neutral > 0.4:
            sentiment *= (1.0 - neutral * 0.4)

        negative_count = self._count_negative_context(text)
        if negative_count >= 2 and sentiment > 0:
            sentiment = -0.3 * min(1.0, negative_count / 4)

        if self._detect_sarcasm(text):
            if sentiment > 0:
                sentiment = -sentiment * 0.6

        if category == "positive" and sentiment < 0:
            sentiment = abs(sentiment) * 0.5

        if category in ("gameplay-bug", "ui-bug", "server-issue") and sentiment > 0.3:
            if negative_count >= 1:
                sentiment = -0.2 * min(1.0, negative_count / 3)

        return round(max(-1.0, min(1.0, sentiment)), 4)