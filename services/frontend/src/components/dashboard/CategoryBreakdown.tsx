import { useMemo, useState } from "react";
import { Card, CardHeader } from "@/components/ui/Card";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/States";
import { useTrendsOverview } from "@/hooks/useDashboardData";
import { CategoryPostsModal } from "@/components/dashboard/CategoryPostsModal";
import { categoryColor } from "@/lib/tone";
import { formatCategoryLabel } from "@/lib/format";

type Aggregate = {
  category: string;
  total: number;
  share: number;
};

export function CategoryBreakdown() {
  const { data, isLoading, isError, refetch } = useTrendsOverview();
  const [selected, setSelected] = useState<string | null>(null);

  const aggregates = useMemo<Aggregate[]>(() => {
    if (!data) {
      return [];
    }
    const byCategory = new Map<string, number>();
    for (const item of data.categories) {
      byCategory.set(
        item.category,
        (byCategory.get(item.category) ?? 0) + item.count
      );
    }
    const total = Array.from(byCategory.values()).reduce(
      (sum, value) => sum + value,
      0
    );
    if (total === 0) {
      return [];
    }
    return Array.from(byCategory.entries())
      .map(([category, count]) => ({
        category,
        total: count,
        share: (count / total) * 100,
      }))
      .sort((a, b) => b.total - a.total);
  }, [data]);

  return (
    <>
      <Card>
        <CardHeader
          title="Categories"
          subtitle="Share of all processed feedback"
        />

        {isLoading ? (
          <div className="px-5 pb-5 pt-1 space-y-3">
            {Array.from({ length: 6 }).map((_, index) => (
              <div key={index} className="flex items-center gap-3">
                <Skeleton className="h-3.5 w-24" />
                <Skeleton className="h-2 flex-1" />
                <Skeleton className="h-3.5 w-10" />
              </div>
            ))}
          </div>
        ) : isError ? (
          <ErrorState
            message="Could not load categories."
            onRetry={() => refetch()}
          />
        ) : aggregates.length === 0 ? (
          <EmptyState message="No processed posts yet." />
        ) : (
          <div className="px-5 pb-5 pt-1">
            {aggregates.map((item) => (
              <button
                type="button"
                key={item.category}
                onClick={() => setSelected(item.category)}
                aria-label={`View ${formatCategoryLabel(item.category)} reviews`}
                className={[
                  "w-full grid grid-cols-[130px_1fr_48px] items-center gap-3",
                  "text-[13px] mb-1.5 last:mb-0 text-left",
                  "rounded-lg px-1.5 py-1.5 -mx-1.5",
                  "hover:bg-white/50 transition-colors",
                  "outline-none focus:ring-2 focus:ring-accent-light/30",
                ].join(" ")}
              >
                <span className="text-ink font-semibold truncate">
                  {formatCategoryLabel(item.category)}
                </span>
                <div className="h-[7px] rounded-full bg-white/70 overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${Math.round(item.share)}%`,
                      background: categoryColor(item.category),
                    }}
                  />
                </div>
                <span className="tabular text-[13px] text-muted-light text-right">
                  {item.share.toFixed(1)}%
                </span>
              </button>
            ))}
          </div>
        )}
      </Card>

      <CategoryPostsModal
        category={selected}
        subcategory={null}
        onClose={() => setSelected(null)}
      />
    </>
  );
}