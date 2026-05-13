import { apiClient } from "./client";
import type { IssuePostDetail, PaginatedIssues } from "@/types/api";

export type IssuesQuery = {
  page?: number;
  pageSize?: number;
  status?: string;
  severity?: string;
  category?: string;
  subcategory?: string;
};

export async function fetchIssues(
  query: IssuesQuery = {}
): Promise<PaginatedIssues> {
  const params: Record<string, string | number> = {
    page: query.page ?? 1,
    page_size: query.pageSize ?? 20,
  };
  if (query.status) {
    params.status = query.status;
  }
  if (query.severity) {
    params.severity = query.severity;
  }
  if (query.category) {
    params.category = query.category;
  }
  if (query.subcategory) {
    params.subcategory = query.subcategory;
  }

  const { data } = await apiClient.get<PaginatedIssues>("/api/issues", {
    params,
  });
  return data;
}

export async function fetchIssuePosts(
  issueId: string
): Promise<IssuePostDetail[]> {
  const { data } = await apiClient.get<IssuePostDetail[]>(
    `/api/issues/${issueId}/posts`
  );
  return data;
}