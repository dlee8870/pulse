import { useMemo, useState } from "react";
import { useRankings } from "@/hooks/useDashboardData";
import { Card, CardHeader } from "@/components/ui/Card";
import { SeverityBar } from "@/components/ui/SeverityBar";
import { SentimentPill } from "@/components/ui/SentimentPill";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/States";
import {
  categoryGroup,
  formatCategoryLabel,
  formatNumber,
  formatSubcategoryLabel,
} from "@/lib/format";

type FilterKey = "all" | "bug" | "balance" | "ui";

const FILTERS: { key: FilterKey; label: string }[] = [
  { key: "all", label: "All" },
  { key: "bug", label: "Bugs" },
  { key: "balance", label: "Balance" },
  { key: "ui", label: "UI" },
];

function FilterTabs({
  active,
  onChange,
}: {
  active: FilterKey;
  onChange: (key: FilterKey) => void;
}) {
  return (
    <div
      className={[
        "inline-flex gap-0.5 p-0.5",
        "bg-track-light dark:bg-track-dark",
        "rounded-md",
        "border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
      ].join(" ")}
    >
      {FILTERS.map((filter) => (
        <button
          key={filter.key}
          type="button"
          onClick={() => onChange(filter.key)}
          className={[
            "text-[11px] px-2.5 py-[3px] rounded font-medium transition-colors",
            active === filter.key
              ? "bg-surface-light dark:bg-surface-dark text-[#111110] dark:text-[#F0F0EE] border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]"
              : "text-[#52524E] dark:text-[#9C9C98]",
          ].join(" ")}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}

function TableSkeleton() {
  return (
    <div className="px-4 py-3 space-y-3">
      {Array.from({ length: 5 }).map((_, index) => (
        <div key={index} className="flex items-center gap-3">
          <Skeleton className="h-3 w-5" />
          <Skeleton className="h-3 flex-1" />
          <Skeleton className="h-3 w-8" />
          <Skeleton className="h-3 w-24" />
          <Skeleton className="h-3 w-10" />
        </div>
      ))}
    </div>
  );
}

export function TopIssuesTable() {
  const [filter, setFilter] = useState<FilterKey>("all");
  const { data, isLoading, isError, refetch } = useRankings();

  const filtered = useMemo(() => {
    if (!data) {
      return [];
    }
    const rows = filter === "all"
      ? data
      : data.filter((row) => categoryGroup(row.category) === filter);
    return rows.slice(0, 8);
  }, [data, filter]);

  return (
    <Card>
      <CardHeader
        title="Top issues"
        subtitle="Ranked by severity, sentiment intensity, and volume"
        right={<FilterTabs active={filter} onChange={setFilter} />}
      />

      {isLoading ? (
        <TableSkeleton />
      ) : isError ? (
        <ErrorState
          message="Could not load rankings."
          onRetry={() => refetch()}
        />
      ) : filtered.length === 0 ? (
        <EmptyState
          message="No issues match this filter."
          hint="Try the All tab or seed more data."
        />
      ) : (
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th
                className={[
                  "w-6 text-left text-[11px] font-medium",
                  "text-[#8A8984] dark:text-[#6A6A66]",
                  "px-4 py-1.5",
                  "border-t-[0.5px] border-b-[0.5px]",
                  "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
                  "bg-page-light dark:bg-page-dark",
                ].join(" ")}
              />
              <th
                className={[
                  "text-left text-[11px] font-medium",
                  "text-[#8A8984] dark:text-[#6A6A66]",
                  "px-4 py-1.5",
                  "border-t-[0.5px] border-b-[0.5px]",
                  "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
                  "bg-page-light dark:bg-page-dark",
                ].join(" ")}
              >
                Issue
              </th>
              <th
                className={[
                  "text-right text-[11px] font-medium",
                  "text-[#8A8984] dark:text-[#6A6A66]",
                  "px-4 py-1.5 w-14",
                  "border-t-[0.5px] border-b-[0.5px]",
                  "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
                  "bg-page-light dark:bg-page-dark",
                ].join(" ")}
              >
                Posts
              </th>
              <th
                className={[
                  "text-left text-[11px] font-medium",
                  "text-[#8A8984] dark:text-[#6A6A66]",
                  "px-4 py-1.5 w-36",
                  "border-t-[0.5px] border-b-[0.5px]",
                  "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
                  "bg-page-light dark:bg-page-dark",
                ].join(" ")}
              >
                Severity
              </th>
              <th
                className={[
                  "text-right text-[11px] font-medium",
                  "text-[#8A8984] dark:text-[#6A6A66]",
                  "px-4 py-1.5 w-[68px]",
                  "border-t-[0.5px] border-b-[0.5px]",
                  "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
                  "bg-page-light dark:bg-page-dark",
                ].join(" ")}
              >
                Sentiment
              </th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row, index) => (
              <tr
                key={`${row.category}-${row.subcategory ?? index}`}
                className={[
                  "border-b-[0.5px] last:border-b-0",
                  "border-[rgba(0,0,0,0.05)] dark:border-[rgba(255,255,255,0.04)]",
                  "hover:bg-hover-light dark:hover:bg-hover-dark",
                  "transition-colors",
                ].join(" ")}
              >
                <td className="px-4 py-2.5 font-mono tabular text-[12px] text-[#8A8984] dark:text-[#6A6A66]">
                  {String(row.rank).padStart(2, "0")}
                </td>
                <td className="px-4 py-2.5">
                  <div className="text-[13px] font-medium">
                    {row.subcategory
                      ? formatSubcategoryLabel(row.subcategory)
                      : formatCategoryLabel(row.category)}
                  </div>
                  <div className="mt-0.5">
                    <span
                      className={[
                        "inline-block px-[7px] py-[1px]",
                        "text-[10px] rounded-[3px]",
                        "bg-track-light dark:bg-track-dark",
                        "text-[#52524E] dark:text-[#9C9C98]",
                      ].join(" ")}
                    >
                      {formatCategoryLabel(row.category)}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-2.5 text-right font-mono tabular text-[13px] text-[#52524E] dark:text-[#9C9C98]">
                  {formatNumber(row.postCount)}
                </td>
                <td className="px-4 py-2.5">
                  <SeverityBar value={row.avgSeverity} />
                </td>
                <td className="px-4 py-2.5 text-right">
                  <SentimentPill value={row.avgSentiment} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  );
}