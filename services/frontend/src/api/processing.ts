import { apiClient } from "./client";

export type CategoryPost = {
  id: string;
  title: string;
  body: string | null;
  source: string;
  subreddit: string | null;
  url: string | null;
  posted_at: string;
  category: string;
  subcategory: string | null;
  sentiment_score: number;
  severity_score: number;
};

type PaginatedProcessed = {
  items: CategoryPost[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export type AnalyzeResult = {
  category: string;
  subcategory: string | null;
  sentiment_score: number;
  severity_score: number;
  keywords: string[];
};

export async function fetchProcessedPosts(
  category: string,
  subcategory?: string | null
): Promise<CategoryPost[]> {
  const params: Record<string, string | number> = {
    category,
    page_size: 100,
    sort_by: "severity_score",
    sort_order: "desc",
  };
  if (subcategory) {
    params.subcategory = subcategory;
  }

  const { data } = await apiClient.get<PaginatedProcessed>("/api/processed", {
    params,
  });
  return data.items;
}

export async function analyzeText(text: string): Promise<AnalyzeResult> {
  const { data } = await apiClient.post<AnalyzeResult>(
    "/api/process/analyze",
    { text },
    { timeout: 180000 }
  );
  return data;
}