import { FormEvent, useState } from "react";
import { AxiosError } from "axios";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/useAuth";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import type { ApiError } from "@/types/api";

type LocationState = {
  from?: {
    pathname?: string;
  };
};

function extractErrorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    const data = err.response?.data as ApiError | undefined;
    if (data?.detail) {
      if (typeof data.detail === "string") {
        return data.detail;
      }
      if (Array.isArray(data.detail) && data.detail[0]?.msg) {
        return data.detail[0].msg;
      }
    }
    return err.message;
  }
  if (err instanceof Error) {
    return err.message;
  }
  return "Sign in failed. Please try again.";
}

export function LoginPage() {
  const { user, login } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (user) {
    return <Navigate to={(location.state as LocationState | null)?.from?.pathname ?? "/dashboard"} replace />;
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
    <div className="min-h-screen">
      <div className="absolute top-5 right-5">
        <ThemeToggle />
      </div>

      <div className="min-h-screen flex items-center justify-center px-5">
        <div
          className={[
            "w-full max-w-sm",
            "bg-surface-light/95 dark:bg-surface-dark/95",
            "backdrop-blur-sm",
            "border-[0.5px] rounded-container",
            "border-[rgba(0,0,0,0.06)] dark:border-[rgba(255,255,255,0.06)]",
            "shadow-[0_2px_12px_rgba(91,95,229,0.08)] dark:shadow-[0_2px_12px_rgba(0,0,0,0.3)]",
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
          <p className="text-xs text-[#6B6FB8] dark:text-[#9C9CB8] mb-6">
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