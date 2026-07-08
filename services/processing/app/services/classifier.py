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
        "scripting-momentum": [
            "scripting", "scripted", "momentum", "handicap",
            "rubber band", "rubberband", "rubber banding",
            "ai cheats", "ai is rigged", "rigged", "comeback code",
        ],
        "defending": [
            "can't defend", "cant defend", "defending is", "defending feels",
            "no way to defend", "manual defending", "jockey", "tackling is",
            "slide tackle", "stand tackle", "defenders are", "defence is",
            "defense is",
        ],
        "finishing": [
            "finishing is", "can't finish", "cant finish", "can't score",
            "cant score", "shots go wide", "finesse shot", "shooting is",
            "shooting feels", "easy chances", "missed open", "scoring is",
            "goals are too easy", "put it away",
        ],
        "dribbling": [
            "dribbling is", "dribbling feels", "skill moves", "skill move",
            "agile dribbling", "tight dribbling", "ball glued", "knock on",
            "controlled sprint",
        ],
        "game-speed": [
            "too fast", "way too fast", "game is too fast",
            "gameplay is too fast", "too quick", "game speed", "end to end",
            "sprinting nonstop", "ping pong", "frantic",
        ],
        "physicality": [
            "too physical", "physicality is", "pushing and shoving",
            "every challenge", "strength stat", "bullied off", "shoulder barge",
        ],
        "controls": [
            "controls are", "controls were", "control is", "unresponsive",
            "non responsive", "not responsive", "inputs dont register",
            "input doesn't register", "inputs don't register",
            "controller support", "controller on pc", "cant move properly",
            "can't move properly", "stuck going", "delayed controls",
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
        "menus": [
            "too many menus", "menus are", "menu navigation",
            "navigating menus", "to get to the game",
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
            "cpu difficulty", "ai defense", "ai teammates", "cpu pass",
            "90% pass", "pro club bots", "bots are", "robot wins",
            "ai is too good", "scripted ai",
        ],
    },
    "server-issue": {
        "lag-delay": [
            "input delay", "speed up lag", "latency", "ms delay",
            "server lag", "100ms", "unplayable lag", "ping spike",
            "input lag", "laggy", "lagging", "lag spike", "slow motion",
        ],
        "disconnection": [
            "disconnect", "disconnection", "connection lost",
            "server disconnect", "kicked out", "dc loss",
        ],
        "connection": [
            "ea server", "ea servers", "can't connect", "cant connect",
            "connect to ea", "server problem", "servers down",
            "servers are down", "server is down", "ea app", "matchmaking",
            "connection error", "online not working", "kicks me out",
            "online connection", "connection issues", "play with friends",
            "co-op not working", "servers suck", "servers are trash",
            "fix the server",
        ],
    },
    "technical": {
        "crashing": [
            "crash", "crashes", "crashing", "freeze", "frozen", "freezes",
            "freezing", "black screen", "blank screen", "won't launch",
            "wont launch", "doesn't launch", "won't start", "wont start",
            "won't even start", "won't run", "wont run", "no longer works",
            "verify files", "stuck on loading", "loading screen", "directx",
            "fatal error", "javelin", "anti cheat", "anticheat", "anti-cheat",
            "hard crash", "closes itself", "force shut", "force close",
            "crash to desktop", "cant launch", "can't launch",
        ],
        "performance": [
            "optimization", "optimized", "optimisation", "optimised",
            "not optimised", "badly optimised", "poor performance",
            "performance is", "performance was", "fps", "frame rate",
            "framerate", "stutter", "stuttering", "unplayable", "runs bad",
            "0 optimization", "badly optimized", "not optimized",
            "slow to load", "not smooth", "low end", "buggy", "bugged",
            "full of bug", "so many bugs", "glitch", "glitches", "glitched",
            "pile of bugs", "bug",
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
            "career mode is", "player career", "career mode remains",
            "career modes", "career mode enjoyers", "career mode player",
            "career mode unchanged",
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
        "general-praise": [
            "great game", "love this game", "love the game", "best fc",
            "best fifa", "amazing game", "so much fun", "really fun",
            "fun game", "underrated", "is peak", "best in years",
            "highly recommend",
        ],
    },
    "market": {
        "price-crash": [
            "market crash", "price drop", "card crash", "extinct card",
            "transfer market economy", "coin value", "market is dead",
        ],
    },
    "monetization": {
        "pay-to-win": [
            "pay to win", "p2w", "pay2win", "pay 2 win", "predatory",
            "microtransaction", "micro transaction", "fifa points",
            "gambling", "ultimate team is so pay", "wallet warrior",
        ],
        "value": [
            "cash grab", "money grab", "rip off", "ripoff", "copy paste",
            "copy and paste", "copy of every", "copy of the", "reskin",
            "same as fc25", "same as last year", "same game as", "same game",
            "nothing special", "full price", "not worth", "quick cash",
            "every year basically", "roster update", "worse every year",
            "worse and worse", "waste of money", "wasted money",
            "money thrown", "looted", "scam", "no license", "missing teams",
            "missing players",
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

    def classify(
        self,
        title: str,
        body: str,
        flair: str | None = None,
        exclude: set[str] | None = None,
    ) -> tuple[str, str | None]:
        """Return (category, subcategory) for a post based on its text and flair.

        Categories named in `exclude` are skipped, which lets the caller
        re-classify a post after rejecting a first guess.
        """
        exclude = exclude or set()
        text = f"{title} {body or ''}".lower()

        best_category = None
        best_subcategory = None
        best_match_score = 0

        for category, subcategories in self.rules.items():
            if category in exclude:
                continue
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

            if flair_hint and flair_hint not in exclude and best_category != flair_hint:
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