import { ReactNode } from "react";

type EmptyStateProps = {
  message: string;
  hint?: string;
};

export function EmptyState({ message, hint }: EmptyStateProps) {
  return (
    <div className="px-5 py-10 text-center">
      <p className="text-sm text-[#52524E] dark:text-[#9C9C98] m-0">
        {message}
      </p>
      {hint ? (
        <p className="text-xs text-[#8A8984] dark:text-[#6A6A66] mt-1.5">
          {hint}
        </p>
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
      <p className="text-sm text-[#B91C1C] dark:text-[#FCA5A5] m-0">
        {message ?? "Could not load data."}
      </p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className={[
            "mt-3 h-8 px-3 rounded-md text-xs font-medium",
            "border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
            "bg-surface-light dark:bg-surface-dark",
            "text-[#52524E] dark:text-[#9C9C98]",
            "hover:bg-hover-light dark:hover:bg-hover-dark",
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
        "animate-pulse bg-track-light dark:bg-track-dark rounded",
        className,
      ].join(" ")}
      aria-hidden="true"
    >
      {children}
    </div>
  );
}