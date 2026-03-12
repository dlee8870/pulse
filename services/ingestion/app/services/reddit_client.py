"""Reddit API client using PRAW."""

import logging
from datetime import datetime, timezone

import praw

logger = logging.getLogger(__name__)


class RedditClient:
    """Fetches posts from Reddit and normalizes them to match our RawPost schema."""

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def fetch_posts(self, subreddit: str, sort: str = "hot", limit: int = 100) -> list[dict]:
        """Pull posts from a subreddit. Skips stickied/pinned posts."""
        logger.info("Fetching %d %s posts from r/%s", limit, sort, subreddit)
        sub = self.reddit.subreddit(subreddit)

        sort_methods = {
            "hot": sub.hot,
            "new": sub.new,
            "top": sub.top,
            "rising": sub.rising,
        }

        fetch_method = sort_methods.get(sort, sub.hot)
        submissions = fetch_method(limit=limit)

        posts = []
        for submission in submissions:
            if submission.stickied:
                continue

            post = {
                "source": "reddit",
                "source_id": f"reddit_{submission.id}",
                "subreddit": subreddit,
                "title": submission.title,
                "body": submission.selftext or "",
                "author": str(submission.author) if submission.author else "[deleted]",
                "score": submission.score,
                "comment_count": submission.num_comments,
                "flair": submission.link_flair_text,
                "url": f"https://reddit.com{submission.permalink}",
                "posted_at": datetime.fromtimestamp(
                    submission.created_utc, tz=timezone.utc
                ),
            }
            posts.append(post)

        logger.info("Fetched %d posts from r/%s", len(posts), subreddit)
        return posts