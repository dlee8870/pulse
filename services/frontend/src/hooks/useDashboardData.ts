import { useQuery } from "@tanstack/react-query";
import {
  fetchPatchImpact,
  fetchPatches,
  fetchRankings,
  fetchTrendsOverview,
} from "@/api/analytics";
import { fetchIssues } from "@/api/issues";

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