const CATEGORY_COLORS: Record<string, string> = {
  "gameplay-bug": "#EF5354",
  "ui-bug": "#9379F4",
  positive: "#83E7C5",
  balance: "#F4C474",
  "feature-request": "#97BAF4",
  "server-issue": "#EF8355",
  technical: "#6E7BF2",
  monetization: "#82DEED",
  market: "#82DEED",
  other: "#A9B2D6",
};

export function categoryColor(category: string): string {
  return CATEGORY_COLORS[category] ?? "#A9B2D6";
}

export function severityColor(value: number): string {
  if (value >= 0.7) {
    return "#EF5354";
  }
  if (value >= 0.45) {
    return "#F1B958";
  }
  return "#97BAF4";
}

type SentimentTone = {
  bg: string;
  fg: string;
};

export function sentimentTone(value: number, _isDark = false): SentimentTone {
  if (value <= -0.15) {
    return { bg: "#FCE9EA", fg: "#C4494C" };
  }
  if (value >= 0.15) {
    return { bg: "#E2F7EE", fg: "#0E8F62" };
  }
  return { bg: "rgba(255,255,255,0.7)", fg: "#5B679D" };
}