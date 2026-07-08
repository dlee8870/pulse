import { FormEvent, useState } from "react";
import { AxiosError } from "axios";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/auth/useAuth";
import { Logo } from "@/components/ui/Logo";
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

const inputClasses = [
  "w-full rounded-xl px-3.5 py-3",
  "text-[14px]",
  "bg-[#F6F6F6]",
  "border border-white/70",
  "text-ink placeholder:text-faint-light",
  "outline-none focus:ring-2 focus:ring-accent-light/40",
].join(" ");

export function LoginPage() {
  const { user, login } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (user) {
    return (
      <Navigate
        to={(location.state as LocationState | null)?.from?.pathname ?? "/dashboard"}
        replace
      />
    );
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
    <div className="min-h-screen flex items-center justify-center px-5">
      <div
        className={[
          "w-full max-w-md",
          "bg-surface-light backdrop-blur-sm",
          "border border-white/50 rounded-[24px]",
          "shadow-[0_8px_40px_rgba(80,90,180,0.12)]",
          "px-8 py-9",
        ].join(" ")}
      >
        <div className="flex items-center gap-2.5 mb-7">
          <Logo size={22} />
          <span className="text-[17px] font-bold tracking-tightish">Pulse</span>
        </div>

        <h1 className="text-[26px] font-bold m-0 mb-1.5 tracking-tightish">
          Sign in
        </h1>
        <p className="text-[14px] text-muted-light mb-7">
          Access the community intelligence dashboard.
        </p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div>
            <label
              htmlFor="username"
              className="block text-[14px] text-muted-light mb-2"
            >
              Username
            </label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              autoFocus
              className={inputClasses}
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-[14px] text-muted-light mb-2"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              className={inputClasses}
            />
          </div>

          {error ? (
            <p className="text-xs text-[#C4494C] -mt-2 m-0">{error}</p>
          ) : null}

          <button
            type="submit"
            disabled={submitting || !username || !password}
            className={[
              "w-full mt-1 py-3 rounded-xl",
              "bg-accent-light text-white",
              "text-[15px] font-semibold",
              "transition-opacity",
              "hover:opacity-90",
              "disabled:opacity-50 disabled:cursor-not-allowed",
              "outline-none focus:ring-2 focus:ring-accent-light/40",
            ].join(" ")}
          >
            {submitting ? "Signing in" : "Sign in"}
          </button>
        </form>

        <div className="mt-7 pt-5 border-t border-white/60 text-[13px] text-muted-light text-center">
          Demo credential: pulse_admin / pulse_admin
        </div>
      </div>
    </div>
  );
}