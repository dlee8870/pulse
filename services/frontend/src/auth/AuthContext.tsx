import {
  createContext,
  ReactNode,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  clearStoredToken,
  getStoredToken,
  setStoredToken,
  setUnauthorizedHandler,
} from "@/api/client";
import { fetchCurrentUser, login as loginRequest } from "@/api/auth";
import type { User } from "@/types/api";

type AuthState = {
  user: User | null;
  token: string | null;
  status: "loading" | "authenticated" | "unauthenticated";
};

type AuthContextValue = AuthState & {
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextValue | null>(null);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: getStoredToken(),
    status: getStoredToken() ? "loading" : "unauthenticated",
  });

  const logout = useCallback(() => {
    clearStoredToken();
    setState({ user: null, token: null, status: "unauthenticated" });
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(() => {
      setState({ user: null, token: null, status: "unauthenticated" });
    });
  }, []);

  useEffect(() => {
    const token = getStoredToken();
    if (!token) {
      return;
    }

    let cancelled = false;
    fetchCurrentUser()
      .then((user) => {
        if (!cancelled) {
          setState({ user, token, status: "authenticated" });
        }
      })
      .catch(() => {
        if (!cancelled) {
          clearStoredToken();
          setState({ user: null, token: null, status: "unauthenticated" });
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const tokenResponse = await loginRequest({ username, password });
    setStoredToken(tokenResponse.access_token);
    const user = await fetchCurrentUser();
    setState({
      user,
      token: tokenResponse.access_token,
      status: "authenticated",
    });
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      login,
      logout,
    }),
    [state, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}