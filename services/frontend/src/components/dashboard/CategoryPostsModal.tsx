import { useEffect } from "react";
import { ExternalLink, X } from "lucide-react";
import { useCategoryPosts } from "@/hooks/useDashboardData";
import { SentimentPill } from "@/components/ui/SentimentPill";
import { ErrorState, Skeleton } from "@/components/ui/States";
import {
  formatCategoryLabel,
  formatSeverity,
  formatShortDate,
  formatSubcategoryLabel,
} from "@/lib/format";

type CategoryPostsModalProps = {
  category: string | null;
  subcategory?: string | null;
  onClose: () => void;
};

export function CategoryPostsModal({
  category,
  subcategory,
  onClose,
}: CategoryPostsModalProps) {
  const { data, isLoading, isError, refetch } = useCategoryPosts(
    category,
    subcategory
  );

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
    if (category) {
      const previous = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = previous;
      };
    }
    return undefined;
  }, [category]);

  if (!category) {
    return null;
  }

  const heading = subcategory
    ? formatSubcategoryLabel(subcategory)
    : formatCategoryLabel(category);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="category-posts-title"
      className="fixed inset-0 z-50 flex items-center justify-center px-4 py-8"
    >
      <button
        type="button"
        aria-label="Close"
        onClick={onClose}
        className="absolute inset-0 bg-[rgba(70,80,150,0.35)] backdrop-blur-[3px]"
      />

      <div
        className={[
          "relative w-full max-w-2xl max-h-[85vh] flex flex-col",
          "bg-[#EFF1FB]/95 backdrop-blur-md",
          "border border-white/60 rounded-[20px]",
          "shadow-[0_16px_60px_rgba(60,70,140,0.25)]",
        ].join(" ")}
      >
        <div className="flex items-start justify-between gap-4 px-6 pt-5 pb-4 border-b border-white/60">
          <div className="min-w-0">
            <p
              id="category-posts-title"
              className="text-[17px] font-bold tracking-tightish m-0 truncate"
            >
              {heading}
            </p>
            <div className="mt-1.5 flex items-center gap-2">
              {subcategory ? (
                <span
                  className={[
                    "inline-block px-2.5 py-[2px]",
                    "text-[11px] rounded-full",
                    "bg-white/70 border border-white/60",
                    "text-[#5F6893] font-semibold",
                  ].join(" ")}
                >
                  {formatCategoryLabel(category)}
                </span>
              ) : null}
              <span className="text-[12px] text-muted-light">
                {data
                  ? `${data.length} review${data.length === 1 ? "" : "s"}`
                  : "Loading reviews"}
              </span>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className={[
              "w-8 h-8 rounded-lg inline-flex items-center justify-center",
              "border border-white/60 bg-white/60",
              "text-muted-light",
              "hover:bg-white/90",
              "transition-colors outline-none",
              "focus:ring-2 focus:ring-accent-light/30",
            ].join(" ")}
          >
            <X size={14} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-4">
          {isLoading ? (
            <div className="space-y-3 py-1">
              {Array.from({ length: 4 }).map((_, index) => (
                <div key={index} className="space-y-2">
                  <Skeleton className="h-3.5 w-3/4" />
                  <Skeleton className="h-3 w-full" />
                  <Skeleton className="h-3 w-5/6" />
                </div>
              ))}
            </div>
          ) : isError ? (
            <ErrorState
              message="Could not load reviews."
              onRetry={() => refetch()}
            />
          ) : !data || data.length === 0 ? (
            <p className="text-[13px] text-muted-light py-6 text-center">
              No reviews in this category yet.
            </p>
          ) : (
            <ul className="m-0 p-0 list-none space-y-3">
              {data.map((post) => (
                <li
                  key={post.id}
                  className={[
                    "rounded-[14px] px-4 py-3.5",
                    "border border-white/60",
                    "bg-white/60",
                  ].join(" ")}
                >
                  <div className="flex items-start justify-between gap-3">
                    <p className="text-[14px] font-bold m-0 leading-snug text-ink">
                      {post.title}
                    </p>
                    {post.url ? (
                      <a
                        href={post.url}
                        target="_blank"
                        rel="noreferrer"
                        aria-label="Open original review"
                        className="shrink-0 mt-0.5 text-faint-light hover:text-muted-light transition-colors"
                      >
                        <ExternalLink size={13} />
                      </a>
                    ) : null}
                  </div>

                  {post.body ? (
                    <p className="mt-1.5 text-[13px] leading-relaxed text-ink-soft m-0 line-clamp-4">
                      {post.body}
                    </p>
                  ) : null}

                  <div className="mt-2.5 flex flex-wrap items-center gap-3 text-[12px] text-muted-light">
                    <SentimentPill value={post.sentiment_score} />
                    <span className="tabular">
                      sev {formatSeverity(post.severity_score)}
                    </span>
                    <span>{post.subreddit ?? post.source}</span>
                    <span>{formatShortDate(post.posted_at)}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}