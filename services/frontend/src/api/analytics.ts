import { apiClient } from "./client";
import type {
  PatchImpact,
  Patch,
  RankingEntry,
  TrendsOverview,
} from "@/types/api";

export async function fetchTrendsOverview(): Promise<TrendsOverview> {
  const { data } = await apiClient.get<TrendsOverview>("/api/trends/overview");
  return data;
}

export async function fetchRankings(): Promise<RankingEntry[]> {
  const { data } = await apiClient.get<RankingEntry[]>("/api/rankings");
  return data;
}

export async function fetchPatches(): Promise<Patch[]> {
  const { data } = await apiClient.get<Patch[]>("/api/patches");
  return data;
}

export async function fetchPatchImpact(patchId: string): Promise<PatchImpact> {
  const { data } = await apiClient.get<PatchImpact>(
    `/api/patches/${patchId}/impact`
  );
  return data;
}