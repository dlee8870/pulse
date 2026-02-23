import re
from collections import Counter

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "because", "but", "and",
    "or", "if", "while", "about", "up", "its", "it", "this", "that",
    "these", "those", "i", "me", "my", "we", "our", "you", "your", "he",
    "him", "his", "she", "her", "they", "them", "their", "what", "which",
    "who", "whom", "dont", "doesnt", "didnt", "cant", "wont", "isnt",
    "arent", "wasnt", "werent", "im", "ive", "like", "get", "got",
    "even", "still", "also", "just", "much", "well", "way", "back",
    "make", "made", "know", "think", "want", "need", "really", "going",
    "thing", "things", "game", "games", "play", "playing", "player",
    "players", "one", "two", "three", "first", "last", "year", "years",
}

GAMING_TERMS = {
    "goalkeeper", "keeper", "gk", "fullback", "cb", "cdm", "cam",
    "striker", "lw", "rw", "lb", "rb",
    "playstyle", "playstyles", "sbc",
    "fut", "rivals", "champs", "weekend league", "squad battles",
    "career mode", "rush mode",
    "division", "seasons", "pack", "promo", "toty", "tots",
    "icon", "legend", "evo", "evolution", "chemistry",
    "pace", "dribbling", "passing", "shooting", "defending", "physical",
    "heading", "offside", "penalty", "corner", "free kick", "throw in",
    "disconnect", "lag", "input delay", "server", "latency",
    "companion app", "transfer market", "coin", "fifa points",
}


class KeywordExtractor:
    def __init__(self):
        self.stop_words = STOP_WORDS
        self.gaming_terms = GAMING_TERMS

    def extract(self, title: str, body: str, max_keywords: int = 8) -> list[str]:
        text = f"{title} {body or ''}".lower()
        clean_text = re.sub(r"[^a-z0-9\s]", " ", text)

        found_terms = []
        for term in sorted(self.gaming_terms, key=len, reverse=True):
            if " " in term:
                if term in clean_text:
                    found_terms.append(term)
            else:
                pattern = rf"\b{re.escape(term)}\b"
                if re.search(pattern, clean_text):
                    found_terms.append(term)

        words = clean_text.split()
        filtered_words = [w for w in words if w not in self.stop_words and len(w) > 2]
        word_counts = Counter(filtered_words)

        existing_words = set()
        for term in found_terms:
            existing_words.update(term.split())

        frequent_words = [
            word for word, count in word_counts.most_common(20)
            if count >= 2 and word not in existing_words
        ]

        keywords = found_terms + frequent_words
        return keywords[:max_keywords]