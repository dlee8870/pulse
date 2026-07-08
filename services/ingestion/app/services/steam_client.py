"""Steam reviews client. Pulls user reviews and normalizes them to match our RawPost schema."""

import hashlib
import logging
import time
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/{app_id}"


class SteamClient:
    """Fetches reviews from the Steam storefront and normalizes them to RawPost dicts."""

    def __init__(self, user_agent: str, min_review_length: int = 40):
        self.user_agent = user_agent
        self.min_review_length = min_review_length

    def fetch_reviews(self, app_id: int, limit: int = 300, language: str = "english") -> list[dict]:
        """Pull the most helpful English reviews for an app, skipping very short ones."""
        logger.info("Fetching up to %d reviews for Steam app %d", limit, app_id)

        url = STEAM_REVIEWS_URL.format(app_id=app_id)
        headers = {"User-Agent": self.user_agent}
        cursor = "*"
        seen_ids = set()
        posts = []
        max_pages = 40

        for _ in range(max_pages):
            if len(posts) >= limit:
                break

            params = {
                "json": 1,
                "language": language,
                "filter": "all",
                "num_per_page": 100,
                "cursor": cursor,
                "purchase_type": "all",
            }
            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            payload = response.json()

            if payload.get("success") != 1:
                raise RuntimeError(f"Steam returned success={payload.get('success')}")

            reviews = payload.get("reviews", [])
            if not reviews:
                break

            for review in reviews:
                recommendation_id = review.get("recommendationid")
                if not recommendation_id or recommendation_id in seen_ids:
                    continue
                seen_ids.add(recommendation_id)

                normalized = self._normalize(review, app_id)
                if normalized is None:
                    continue

                posts.append(normalized)
                if len(posts) >= limit:
                    break

            next_cursor = payload.get("cursor")
            if not next_cursor or next_cursor == cursor:
                break

            cursor = next_cursor
            time.sleep(0.5)

        logger.info("Fetched %d usable reviews for Steam app %d", len(posts), app_id)
        return posts

    def _normalize(self, review: dict, app_id: int) -> dict | None:
        """Convert a Steam review into a RawPost-shaped dict, or None if unusable."""
        text = (review.get("review") or "").strip()
        if len(text) < self.min_review_length:
            return None

        if not review.get("timestamp_created"):
            return None

        author = review.get("author") or {}
        steam_id = str(author.get("steamid", "unknown"))
        handle = "steam_" + hashlib.sha1(steam_id.encode()).hexdigest()[:8]

        recommended = "Recommended" if review.get("voted_up") else "Not Recommended"

        return {
            "source": "steam",
            "source_id": f"steam_{review['recommendationid']}",
            "subreddit": "EA SPORTS FC 26",
            "title": self._make_title(text),
            "body": text,
            "author": handle,
            "score": int(review.get("votes_up", 0)),
            "comment_count": int(review.get("comment_count", 0)),
            "flair": recommended,
            "url": f"https://steamcommunity.com/profiles/{steam_id}/recommended/{app_id}/",
            "posted_at": datetime.fromtimestamp(
                int(review["timestamp_created"]), tz=timezone.utc
            ),
        }

    @staticmethod
    def _make_title(text: str, max_length: int = 90) -> str:
        """Build a short title from the first line of the review text."""
        first_line = text.splitlines()[0].strip()
        if not first_line:
            first_line = text.strip()
        if len(first_line) <= max_length:
            return first_line
        return first_line[:max_length].rstrip() + "..."