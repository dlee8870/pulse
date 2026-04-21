import { apiClient } from "./client";
import type { LoginRequest, TokenResponse, User } from "@/types/api";

export async function login(credentials: LoginRequest): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>(
    "/api/auth/login",
    credentials
  );
  return data;
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>("/api/auth/me");
  return data;
}