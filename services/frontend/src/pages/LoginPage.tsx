import { FormEvent, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { Logo } from "@/components/ui/Logo";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import { useAuth } from "@/auth/useAuth";
import type { ApiError } from "@/types/api";

type LocationState = {
  from?: { pathname: string };
};

function extractErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    const status = error.response?.status;
    if (status === 429) {
      return "Too many attempts. Wait a moment and try again.";
    }
    if (status === 401) {
      return "Invalid username or password.";
    }
    const data = error.response?.data as ApiError | undefined;
    if (typeof data?.detail === "string") {
      return data.detail;
    }
    if (Array.isArray(data?.detail) && data.detail[0]?.msg) {
      return data.detail[0].msg;
    }
    return "Could not reach the server.";
  }
  return "Something went wrong. Please try again.";
}

export function LoginPage() {
  const { status, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (status === "authenticated") {
    const from = (location.state as LocationState | null)?.from?.pathname;
    return <Navigate to={from ?? "/dashboard"} replace />;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(username.trim(), password);
      const from = (location.state as LocationState | null)?.from?.pathname;
      navigate(from ?? "/dashboard", { replace: true });
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-page-light dark:bg-page-dark">
      <div className="absolute top-5 right-5">
        <ThemeToggle />
      </div>

      <div className="min-h-screen flex items-center justify-center px-5">
        <div
          className={[
            "w-full max-w-sm",
            "bg-surface-light dark:bg-surface-dark",
            "border-[0.5px] rounded-container",
            "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
            "p-7",
          ].join(" ")}
        >
          <div className="flex items-center gap-2.5 mb-5">
            <Logo size={20} />
            <span className="text-sm font-medium tracking-tightish">
              Pulse
            </span>
          </div>

          <h1 className="text-base font-medium mb-1 tracking-tightish">
            Sign in
          </h1>
          <p className="text-xs text-[#52524E] dark:text-[#9C9C98] mb-6">
            Access the community intelligence dashboard.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <Input
              id="username"
              label="Username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              autoFocus
            />
            <Input
              id="password"
              label="Password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />

            {error ? (
              <p className="text-xs text-[#B91C1C] dark:text-[#FCA5A5] -mt-1">
                {error}
              </p>
            ) : null}

            <Button
              type="submit"
              disabled={submitting || !username || !password}
              className="w-full mt-1"
            >
              {submitting ? "Signing in" : "Sign in"}
            </Button>
          </form>

          <div
            className={[
              "mt-5 pt-4",
              "border-t-[0.5px] border-[rgba(0,0,0,0.05)] dark:border-[rgba(255,255,255,0.04)]",
              "text-[11px] text-[#8A8984] dark:text-[#6A6A66] text-center",
            ].join(" ")}
          >
            Demo credentials: pulse_admin / pulse_admin
          </div>
        </div>
      </div>
    </div>
  );
}