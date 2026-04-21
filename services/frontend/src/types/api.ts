export type LoginRequest = {
  username: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
  expires_in_seconds: number;
};

export type User = {
  id: string;
  username: string;
  is_active: boolean;
  created_at: string;
};

export type ApiError = {
  error?: string;
  detail?: string | { msg: string }[];
  path?: string;
  timestamp?: string;
};

export type CategoryBreakdownItem = {
  category: string;
  subcategory: string | null;
  count: number;
  avgSentiment: number;
  avgSeverity: number;
};

export type TrendsOverview = {
  totalProcessed: number;
  totalRaw: number;
  avgSentiment: number;
  avgSeverity: number;
  categories: CategoryBreakdownItem[];
};

export type RankingEntry = {
  rank: number;
  category: string;
  subcategory: string | null;
  postCount: number;
  avgSentiment: number;
  avgSeverity: number;
  compositeScore: number;
};

export type Issue = {
  id: string;
  title: string;
  description: string | null;
  category: string;
  subcategory: string | null;
  status: "open" | "acknowledged" | "investigating" | "resolved" | "closed";
  severity: "low" | "medium" | "high" | "critical";
  post_count: number;
  avg_sentiment: number;
  avg_severity: number;
  first_reported_at: string;
  last_activity_at: string;
  created_at: string;
  updated_at: string;
};

export type PaginatedIssues = {
  items: Issue[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export type Patch = {
  id: string;
  version: string;
  releaseDate: string;
  notes: string | null;
  createdAt: string;
};

export type PatchPeriodMetrics = {
  postCount: number;
  avgSentiment: number;
  avgSeverity: number;
  categories: CategoryBreakdownItem[];
};

export type PatchImpact = {
  patch: Patch;
  prePatch: PatchPeriodMetrics;
  postPatch: PatchPeriodMetrics;
  sentimentChange: number;
  severityChange: number;
  volumeChange: number;
};