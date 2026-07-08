import { useQuery } from "@tanstack/react-query";
import {
  fetchPatchImpact,
  fetchPatches,
  fetchRankings,
  fetchTrendsOverview,
} from "@/api/analytics";
import { fetchIssuePosts, fetchIssues } from "@/api/issues";
import { fetchProcessedPosts } from "@/api/processing";

export function useTrendsOverview() {
  return useQuery({
    queryKey: ["trends", "overview"],
    queryFn: fetchTrendsOverview,
  });
}

export function useRankings() {
  return useQuery({
    queryKey: ["rankings"],
    queryFn: fetchRankings,
  });
}

export function useIssuesSummary() {
  return useQuery({
    queryKey: ["issues", "summary"],
    queryFn: () => fetchIssues({ page: 1, pageSize: 100 }),
  });
}

export function useIssuePosts(issueId: string | null) {
  return useQuery({
    queryKey: ["issues", "posts", issueId],
    queryFn: () => fetchIssuePosts(issueId as string),
    enabled: Boolean(issueId),
  });
}

export function useCategoryPosts(
  category: string | null,
  subcategory?: string | null
) {
  return useQuery({
    queryKey: ["processed", "category", category, subcategory ?? null],
    queryFn: () => fetchProcessedPosts(category as string, subcategory ?? null),
    enabled: Boolean(category),
  });
}

export function usePatches() {
  return useQuery({
    queryKey: ["patches"],
    queryFn: fetchPatches,
  });
}

export function usePatchImpact(patchId: string | null) {
  return useQuery({
    queryKey: ["patches", "impact", patchId],
    queryFn: () => fetchPatchImpact(patchId as string),
    enabled: Boolean(patchId),
  });
}