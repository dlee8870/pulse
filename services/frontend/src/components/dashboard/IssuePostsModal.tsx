import { useEffect, useState } from "react";
import { ExternalLink, X } from "lucide-react";
import { useIssuePosts } from "@/hooks/useDashboardData";
import { SentimentPill } from "@/components/ui/SentimentPill";
import { ErrorState, Skeleton } from "@/components/ui/States";
import type { IssuePostDetail } from "@/types/api";
import {
  formatCategoryLabel,
  formatShortDate,
  formatSubcategoryLabel,
} from "@/lib/format";

type IssuePostsModalProps = {
  issueId: string | null;
  issueTitle: string;
  category: string;
  subcategory: string | null;
  onClose: () => void;
};

export function IssuePostsModal({
  issueId,
  issueTitle,
  category,
  subcategory,
  onClose,
}: IssuePostsModalProps) {
  const { data, isLoading, isError, refetch } = useIssuePosts(issueId);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
      }
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  useEffect(() => {
    if (issueId) {
      const previous = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = previous;
      };
    }
    return undefined;
  }, [issueId]);

  if (!issueId) {
    return null;
  }

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="issue-posts-title"
      className="fixed inset-0 z-50 flex items-center justify-center px-4 py-8"
    >
      <button
        type="button"
        aria-label="Close"
        onClick={onClose}
        className="absolute inset-0 bg-[rgba(20,20,40,0.45)] backdrop-blur-[2px]"
      />

      <div
        className={[
          "relative w-full max-w-2xl max-h-[85vh] flex flex-col",
          "bg-surface-light dark:bg-surface-dark",
          "border-[0.5px] rounded-container",
          "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
          "shadow-[0_12px_48px_rgba(20,20,40,0.18)] dark:shadow-[0_12px_48px_rgba(0,0,0,0.4)]",
        ].join(" ")}
      >
        <div
          className={[
            "flex items-start justify-between gap-4",
            "px-5 pt-4 pb-3.5",
            "border-b-[0.5px] border-[rgba(0,0,0,0.06)] dark:border-[rgba(255,255,255,0.06)]",
          ].join(" ")}
        >
          <div className="min-w-0">
            <p
              id="issue-posts-title"
              className="text-sm font-medium tracking-tightish m-0 truncate"
            >
              {issueTitle}
            </p>
            <div className="mt-1.5 flex items-center gap-1.5">
              <span
                className={[
                  "inline-block px-[7px] py-[1px]",
                  "text-[10px] rounded-[3px]",
                  "bg-track-light dark:bg-track-dark",
                  "text-[#52524E] dark:text-[#9C9C98]",
                ].join(" ")}
              >
                {formatCategoryLabel(category)}
              </span>
              {subcategory ? (
                <span
                  className={[
                    "inline-block px-[7px] py-[1px]",
                    "text-[10px] rounded-[3px]",
                    "bg-track-light dark:bg-track-dark",
                    "text-[#52524E] dark:text-[#9C9C98]",
                  ].join(" ")}
                >
                  {formatSubcategoryLabel(subcategory)}
                </span>
              ) : null}
              {data ? (
                <span className="text-[11px] text-[#8A8984] dark:text-[#6A6A66]">
                  {data.length} post{data.length === 1 ? "" : "s"}
                </span>
              ) : null}
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className={[
              "w-8 h-8 rounded-md inline-flex items-center justify-center",
              "border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
              "bg-surface-light dark:bg-surface-dark",
              "text-[#52524E] dark:text-[#9C9C98]",
              "hover:bg-hover-light dark:hover:bg-hover-dark",
              "transition-colors outline-none",
              "focus:ring-2 focus:ring-accent-light/30 dark:focus:ring-accent-dark/30",
            ].join(" ")}
          >
            <X size={14} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-3">
          {isLoading ? (
            <div className="space-y-3 py-1">
              {Array.from({ length: 3 }).map((_, index) => (
                <div key={index} className="space-y-2">
                  <Skeleton className="h-3 w-3/4" />
                  <Skeleton className="h-2.5 w-full" />
                  <Skeleton className="h-2.5 w-5/6" />
                </div>
              ))}
            </div>
          ) : isError ? (
            <ErrorState
              message="Could not load posts."
              onRetry={() => refetch()}
            />
          ) : !data || data.length === 0 ? (
            <div className="px-2 py-10 text-center">
              <p className="text-sm text-[#52524E] dark:text-[#9C9C98] m-0">
                No posts linked to this issue.
              </p>
            </div>
          ) : (
            <ul className="m-0 p-0 list-none">
              {data.map((post, index) => (
                <li
                  key={post.processed_post_id}
                  className={[
                    "py-3",
                    index > 0
                      ? "border-t-[0.5px] border-[rgba(0,0,0,0.05)] dark:border-[rgba(255,255,255,0.04)]"
                      : "",
                  ].join(" ")}
                >
                  <PostCard post={post} />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

type PostCardProps = {
  post: IssuePostDetail;
};

function PostCard({ post }: PostCardProps) {
  const [expanded, setExpanded] = useState(false);
  const hasBody = Boolean(post.body && post.body.trim().length > 0);

  return (
    <div>
      <div className="flex items-start justify-between gap-3">
        <p className="text-[13px] font-medium m-0 leading-snug">{post.title}</p>
        {post.url ? (
          <a
            href={post.url}
            target="_blank"
            rel="noreferrer noopener"
            aria-label="Open original post"
            className={[
              "shrink-0 w-6 h-6 rounded inline-flex items-center justify-center",
              "text-[#8A8984] dark:text-[#6A6A66]",
              "hover:text-[#5B5FE5] dark:hover:text-[#818CF8]",
              "hover:bg-hover-light dark:hover:bg-hover-dark",
              "transition-colors",
            ].join(" ")}
          >
            <ExternalLink size={12} />
          </a>
        ) : null}
      </div>

      {hasBody ? (
        <p
          className={[
            "mt-1 text-[12px] text-[#52524E] dark:text-[#9C9C98] m-0 leading-relaxed",
            expanded ? "" : "line-clamp-2",
          ].join(" ")}
        >
          {post.body}
        </p>
      ) : null}

      {hasBody ? (
        <button
          type="button"
          onClick={() => setExpanded((current) => !current)}
          className={[
            "mt-1 text-[11px] font-medium",
            "text-[#5B5FE5] dark:text-[#818CF8]",
            "hover:underline outline-none",
            "focus:ring-2 focus:ring-accent-light/30 dark:focus:ring-accent-dark/30 rounded",
          ].join(" ")}
        >
          {expanded ? "Show less" : "Show more"}
        </button>
      ) : null}

      <div className="mt-2 flex items-center gap-3 text-[11px] text-[#8A8984] dark:text-[#6A6A66]">
        {post.subreddit ? <span>r/{post.subreddit}</span> : null}
        <span>{formatShortDate(post.posted_at)}</span>
        <span className="ml-auto inline-flex items-center gap-2">
          <span>
            sev{" "}
            <span className="font-mono tabular text-[#52524E] dark:text-[#9C9C98]">
              {post.severity_score.toFixed(2)}
            </span>
          </span>
          <SentimentPill value={post.sentiment_score} />
        </span>
      </div>
    </div>
  );
}