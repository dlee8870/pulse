import { ReactNode } from "react";

type EmptyStateProps = {
  message: string;
  hint?: string;
};

export function EmptyState({ message, hint }: EmptyStateProps) {
  return (
    <div className="px-5 py-10 text-center">
      <p className="text-sm text-muted-light m-0">{message}</p>
      {hint ? (
        <p className="text-xs text-faint-light mt-1.5">{hint}</p>
      ) : null}
    </div>
  );
}

type ErrorStateProps = {
  message?: string;
  onRetry?: () => void;
};

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="px-5 py-8 text-center">
      <p className="text-sm text-[#C4494C] m-0">
        {message ?? "Could not load data."}
      </p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className={[
            "mt-3 h-8 px-3 rounded-lg text-xs font-semibold",
            "border border-white/60",
            "bg-raised-light",
            "text-muted-light",
            "hover:bg-white/80",
            "transition-colors",
          ].join(" ")}
        >
          Retry
        </button>
      ) : null}
    </div>
  );
}

type SkeletonProps = {
  className?: string;
  children?: ReactNode;
};

export function Skeleton({ className = "", children }: SkeletonProps) {
  return (
    <div
      className={[
        "animate-pulse bg-white/60 rounded",
        className,
      ].join(" ")}
      aria-hidden="true"
    >
      {children}
    </div>
  );
}