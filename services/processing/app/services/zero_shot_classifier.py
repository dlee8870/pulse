"""Zero-shot category classification with keyword-based subcategory selection.

Top-level categories are chosen semantically by an NLI model, so the classifier
understands meaning (including negation) instead of matching strings. Subcategories
are then picked by keyword rules within the winning category only, where precise
vocabulary matching is reliable.
"""

import logging

from transformers import pipeline

from app.services.classifier import CATEGORY_RULES
from app.services.sentiment import normalize_censored_text

logger = logging.getLogger(__name__)

CATEGORY_LABELS = {
    "technical": "game crashes, freezes, or bad technical performance",
    "server-issue": "online servers, connection, or matchmaking problems",
    "gameplay-bug": "complaints about gameplay mechanics or how the game plays",
    "balance": "gameplay balance problems like overpowered mechanics or unreasonable AI difficulty",
    "ui-bug": "problems with menus or the user interface",
    "monetization": "pay to win microtransactions, or a cash grab that is not worth the money",
    "feature-request": "requests for new features or improvements",
    "positive": "praise for the game",
    "other": "general anger or insults with no specific topic",
}

CONFIDENCE_FLOOR = 0.25


class ZeroShotClassifier:
    """Classifies posts by meaning using facebook/bart-large-mnli."""

    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """Load the zero-shot model into memory."""
        logger.info("Loading zero-shot model: %s", model_name)
        self._pipeline = pipeline(
            "zero-shot-classification",
            model=model_name,
        )
        self._label_to_category = {v: k for k, v in CATEGORY_LABELS.items()}
        logger.info("Zero-shot model loaded")

    def classify(
        self,
        title: str,
        body: str,
        flair: str | None = None,
        exclude: set[str] | None = None,
    ) -> tuple[str, str | None]:
        """Return (category, subcategory) for a post based on its meaning.

        Categories named in `exclude` are removed from the candidate labels,
        which lets the caller re-classify after rejecting a first guess.
        """
        exclude = exclude or set()
        text = normalize_censored_text(f"{title} {body or ''}".strip())
        if not text:
            return "other", None

        labels = [
            label
            for category, label in CATEGORY_LABELS.items()
            if category not in exclude
        ]

        result = self._pipeline(text[:1500], labels)
        top_label = result["labels"][0]
        top_score = result["scores"][0]
        category = self._label_to_category[top_label]

        if top_score < CONFIDENCE_FLOOR:
            category = "other"

        if category == "other":
            return "other", None

        subcategory = self._pick_subcategory(text.lower(), category)
        return category, subcategory

    @staticmethod
    def _pick_subcategory(text_lower: str, category: str) -> str | None:
        """Pick the best-matching subcategory within a category using keyword rules."""
        subcategories = dict(CATEGORY_RULES.get(category, {}))
        if category == "monetization":
            subcategories.update(CATEGORY_RULES.get("market", {}))

        best_subcategory = None
        best_score = 0

        for subcategory, keywords in subcategories.items():
            matched = [kw for kw in keywords if kw in text_lower]
            if matched:
                score = len(matched) * 10 + sum(len(kw) for kw in matched)
                if score > best_score:
                    best_score = score
                    best_subcategory = subcategory

        return best_subcategory