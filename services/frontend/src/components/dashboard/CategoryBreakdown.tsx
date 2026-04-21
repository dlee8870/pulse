import { useMemo } from "react";
import { Card, CardHeader } from "@/components/ui/Card";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/States";
import { useTrendsOverview } from "@/hooks/useDashboardData";
import { categoryColor } from "@/lib/tone";
import { formatCategoryLabel } from "@/lib/format";

type Aggregate = {
  category: string;
  total: number;
  share: number;
};

export function CategoryBreakdown() {
  const { data, isLoading, isError, refetch } = useTrendsOverview();

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
    <Card>
      <CardHeader
        title="Categories"
        subtitle="Share of all processed feedback"
      />

      {isLoading ? (
        <div className="px-4 pb-4 pt-1 space-y-2.5">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="flex items-center gap-2.5">
              <Skeleton className="h-3 w-24" />
              <Skeleton className="h-2 flex-1" />
              <Skeleton className="h-3 w-8" />
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
        <div className="px-4 pb-4 pt-1">
          {aggregates.map((item) => (
            <div
              key={item.category}
              className="grid grid-cols-[120px_1fr_40px] items-center gap-2.5 text-xs mb-2.5 last:mb-0"
            >
              <span className="text-[#111110] dark:text-[#F0F0EE]">
                {formatCategoryLabel(item.category)}
              </span>
              <div className="h-2 rounded-[4px] bg-track-light dark:bg-track-dark overflow-hidden">
                <div
                  className="h-full rounded-[4px]"
                  style={{
                    width: `${Math.round(item.share)}%`,
                    background: categoryColor(item.category),
                  }}
                />
              </div>
              <span className="font-mono tabular text-xs text-[#52524E] dark:text-[#9C9C98] text-right">
                {item.share.toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}