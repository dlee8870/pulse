export type SentimentTone = {
  bg: string;
  fg: string;
};

export function sentimentTone(value: number, isDark: boolean): SentimentTone {
  if (value <= -0.6) {
    return isDark
      ? { bg: "rgba(220,38,38,0.18)", fg: "#FCA5A5" }
      : { bg: "#FEF2F2", fg: "#B91C1C" };
  }
  if (value < 0) {
    return isDark
      ? { bg: "rgba(245,158,11,0.16)", fg: "#FCD34D" }
      : { bg: "#FFFBEB", fg: "#B45309" };
  }
  return isDark
    ? { bg: "rgba(16,185,129,0.16)", fg: "#6EE7B7" }
    : { bg: "#ECFDF5", fg: "#047857" };
}

export function severityColor(value: number): string {
  if (value >= 0.8) {
    return "#DC2626";
  }
  if (value >= 0.6) {
    return "#F59E0B";
  }
  return "#6366F1";
}

export const categoryColors: Record<string, string> = {
  "gameplay-bug": "#DC2626",
  "server-issue": "#EF4444",
  balance: "#F59E0B",
  "ui-bug": "#8B5CF6",
  "feature-request": "#3B82F6",
  market: "#06B6D4",
  positive: "#10B981",
  other: "#9CA3AF",
};

export function categoryColor(category: string): string {
  return categoryColors[category] ?? "#9CA3AF";
}