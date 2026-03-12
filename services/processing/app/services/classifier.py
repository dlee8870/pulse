"""Rule-based post classifier for EA FC community feedback categories."""

CATEGORY_RULES = {
    "gameplay-bug": {
        "goalkeeper-logic": [
            "goalkeeper", "keeper", "gk logic", "gk movement", "gk ai",
            "keeper rating", "keeper save", "courtois", "neuer", "donnarumma",
            "manual gk", "gk positioning",
        ],
        "fullback-tracking": [
            "fullback", "full back", "lb tracking", "rb tracking",
            "tracking runs", "defensive tracking", "robertson", "jogging",
            "fullbacks jogging", "stop tracking",
        ],
        "player-switching": [
            "player switching", "player switch", "switch to", "l1 switch",
            "right stick switch", "auto switch", "switching mechanic",
        ],
        "offside-logic": [
            "offside", "offside line", "offside call", "offside trap",
            "onside", "var offside",
        ],
        "auto-lunge": [
            "auto lunge", "auto-lunge", "auto tackle", "lunging",
            "unwanted tackle", "ai tackle", "auto-tackle",
        ],
        "first-touch": [
            "first touch", "ball control", "heavy touch", "bad touch",
            "touch is terrible", "touch sends",
        ],
        "passing-accuracy": [
            "passing accuracy", "pass goes wrong", "wrong player pass",
            "assisted passing", "pass direction", "pass assist",
            "passing needs", "pass goes to",
        ],
        "kickoff-goals": [
            "kick off goal", "kickoff goal", "kick-off goal",
            "kickoff boost", "kickoff glitch", "from kick off",
            "after kick off",
        ],
        "referee-logic": [
            "referee", "ref logic", "red card", "foul call",
            "advantage play", "penalty call", "booking",
            "referee logic", "refs are",
        ],
        "heading": [
            "heading accuracy", "header", "aerial",
            "win a header", "heading is",
            "cross into box",
        ],
        "corners": [
            "corner kick", "corner delivery", "corners are",
            "scoring from corner",
        ],
    },
    "ui-bug": {
        "sbc-interface": [
            "sbc filter", "sbc menu", "sbc position", "squad building challenge",
            "sbc broken", "sbc glitch",
        ],
        "scoreboard-overlay": [
            "substitution graphic", "scoreboard bug", "overlay stuck",
            "stuck on screen", "hud bug", "display bug",
        ],
        "replay-camera": [
            "goal replay bug", "replay shows", "replay bug",
            "center circle replay", "wrong camera angle replay",
        ],
        "companion-app": [
            "companion app", "web app crash", "mobile app crash",
            "app crash", "transfer market app",
        ],
    },
    "balance": {
        "playstyle-dependency": [
            "playstyle", "play style", "incisive pass", "tiki taka",
            "trivela", "aerial+", "playstyle+", "without playstyle",
            "need playstyle", "playstyles are",
        ],
        "pace-meta": [
            "pace meta", "pace abuse", "pace is", "only pace",
            "pacey winger", "sprint speed", "through ball spam",
            "pace still", "pace nerf",
        ],
        "body-type": [
            "body type", "unique body", "average body", "body model",
            "player model", "feels clunky", "body types",
        ],
        "ai-difficulty": [
            "squad battles", "world class", "legendary difficulty",
            "ultimate difficulty", "ai defending", "ai perfect",
            "cpu difficulty", "ai defense",
        ],
    },
    "server-issue": {
        "lag-delay": [
            "input delay", "speed up lag", "latency", "ms delay",
            "server lag", "100ms", "unplayable lag", "ping spike",
        ],
        "disconnection": [
            "disconnect", "disconnection", "connection lost",
            "server disconnect", "kicked out", "dc loss",
        ],
    },
    "feature-request": {
        "skip-cutscenes": [
            "skip celebration", "skip replay", "skip cutscene", "skip all",
            "unskippable", "waste time celebration", "skip option",
            "respect time", "no way to skip",
        ],
        "practice-mode": [
            "training mode", "practice mode", "training ground",
            "skill arena", "practice drill", "practice area",
        ],
        "career-mode": [
            "career mode transfer", "transfer logic", "ai transfer",
            "release clause", "contract negotiation", "manager mode",
            "career mode is",
        ],
    },
    "positive": {
        "evolution-system": [
            "evolution system", "evo system", "evolved card", "evo player",
            "evolution is", "love the evo",
        ],
        "chemistry-system": [
            "chemistry system", "chem system", "chemistry feels",
            "chemistry is", "chem this year",
        ],
        "rush-mode": [
            "rush mode", "rush is", "rush with friends",
        ],
        "content-quality": [
            "content this year", "content team", "daily sbc",
            "objective player", "promo concept", "content is",
            "good content", "great content", "best content",
        ],
    },
    "market": {
        "price-crash": [
            "market crash", "price drop", "card crash", "extinct card",
            "transfer market economy", "coin value", "market is dead",
        ],
    },
}

FLAIR_CATEGORY_HINTS = {
    "feature request": "feature-request",
    "suggestion": "feature-request",
    "positive": "positive",
    "praise": "positive",
    "bug": "ui-bug",
    "servers": "server-issue",
    "career mode": "feature-request",
    "ultimate team": None,
    "gameplay": None,
}


class PostClassifier:
    """Classifies posts using keyword matching with flair-based overrides."""

    def __init__(self):
        self.rules = CATEGORY_RULES
        self.flair_hints = FLAIR_CATEGORY_HINTS

    def classify(self, title: str, body: str, flair: str | None = None) -> tuple[str, str | None]:
        """Return (category, subcategory) for a post based on its text and flair."""
        text = f"{title} {body or ''}".lower()

        best_category = None
        best_subcategory = None
        best_match_score = 0

        for category, subcategories in self.rules.items():
            for subcategory, keywords in subcategories.items():
                match_count = sum(1 for kw in keywords if kw in text)
                if match_count > 0:
                    keyword_specificity = sum(len(kw) for kw in keywords if kw in text)
                    match_score = match_count * 10 + keyword_specificity

                    if match_score > best_match_score:
                        best_match_score = match_score
                        best_category = category
                        best_subcategory = subcategory

        if flair:
            flair_lower = flair.lower().strip()
            flair_hint = self.flair_hints.get(flair_lower)

            if flair_hint and best_category != flair_hint:
                flair_rules = self.rules.get(flair_hint, {})
                for subcategory, keywords in flair_rules.items():
                    match_count = sum(1 for kw in keywords if kw in text)
                    if match_count > 0:
                        best_category = flair_hint
                        best_subcategory = subcategory
                        break

                if best_category != flair_hint and flair_hint in self.rules:
                    best_category = flair_hint
                    best_subcategory = None

        if best_category is None:
            return "other", None

        return best_category, best_subcategory