export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function formatSignedNumber(value: number, decimals = 2): string {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(decimals)}`;
}

export function formatPercent(value: number, decimals = 1): string {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(decimals)}%`;
}

export function formatSentiment(value: number): string {
  return value.toFixed(2);
}

export function formatSeverity(value: number): string {
  return value.toFixed(2);
}

export function formatIsoDate(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function formatShortDate(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}

export function formatCategoryLabel(category: string): string {
  return category
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function formatSubcategoryLabel(subcategory: string): string {
  return subcategory
    .split(/[-_]/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function categoryGroup(category: string): string {
  if (category.includes("bug") && category !== "ui-bug") {
    return "bug";
  }
  if (category === "ui-bug") {
    return "ui";
  }
  if (category === "balance") {
    return "balance";
  }
  if (category === "server-issue") {
    return "server";
  }
  if (category === "feature-request") {
    return "feature";
  }
  if (category === "positive") {
    return "positive";
  }
  return "other";
}

export function relativeTime(iso: string | null | undefined): string {
  if (!iso) {
    return "never";
  }
  const then = new Date(iso).getTime();
  const now = Date.now();
  const diffSeconds = Math.floor((now - then) / 1000);

  if (diffSeconds < 60) {
    return "just now";
  }
  if (diffSeconds < 3600) {
    const minutes = Math.floor(diffSeconds / 60);
    return `${minutes} minute${minutes === 1 ? "" : "s"} ago`;
  }
  if (diffSeconds < 86400) {
    const hours = Math.floor(diffSeconds / 3600);
    return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  }
  const days = Math.floor(diffSeconds / 86400);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}