import { useMemo, useState } from "react";
import { useRankings } from "@/hooks/useDashboardData";
import { Card, CardHeader } from "@/components/ui/Card";
import { SeverityBar } from "@/components/ui/SeverityBar";
import { SentimentPill } from "@/components/ui/SentimentPill";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/States";
import { CategoryPostsModal } from "@/components/dashboard/CategoryPostsModal";
import {
  categoryGroup,
  formatCategoryLabel,
  formatNumber,
  formatSubcategoryLabel,
} from "@/lib/format";
import type { RankingEntry } from "@/types/api";

type FilterKey = "all" | "bug" | "balance" | "ui";

const FILTERS: { key: FilterKey; label: string }[] = [
  { key: "all", label: "All" },
  { key: "bug", label: "Bugs" },
  { key: "balance", label: "Balance" },
  { key: "ui", label: "UI" },
];

type Selected = {
  category: string;
  subcategory: string | null;
};

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
        "bg-white/50",
        "rounded-lg",
        "border border-white/60",
      ].join(" ")}
    >
      {FILTERS.map((filter) => (
        <button
          key={filter.key}
          type="button"
          onClick={() => onChange(filter.key)}
          className={[
            "text-[12px] px-3 py-1 rounded-md font-semibold transition-colors",
            active === filter.key
              ? "bg-white text-ink shadow-[0_1px_4px_rgba(80,90,180,0.10)]"
              : "text-muted-light",
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
    <div className="px-5 py-4 space-y-3.5">
      {Array.from({ length: 5 }).map((_, index) => (
        <div key={index} className="flex items-center gap-3">
          <Skeleton className="h-3.5 w-6" />
          <Skeleton className="h-3.5 flex-1" />
          <Skeleton className="h-3.5 w-8" />
          <Skeleton className="h-3.5 w-24" />
          <Skeleton className="h-3.5 w-12" />
        </div>
      ))}
    </div>
  );
}

const headerCell = [
  "text-[12px] font-semibold",
  "text-muted-light",
  "px-5 py-2",
  "border-t border-b border-white/50",
  "bg-white/40",
].join(" ");

export function TopIssuesTable() {
  const [filter, setFilter] = useState<FilterKey>("all");
  const [selected, setSelected] = useState<Selected | null>(null);
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

  function handleRowClick(row: RankingEntry) {
    setSelected({ category: row.category, subcategory: row.subcategory });
  }

  return (
    <>
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
            hint="Try the All tab."
          />
        ) : (
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className={[headerCell, "w-8 text-left"].join(" ")} />
                <th className={[headerCell, "text-left"].join(" ")}>Issue</th>
                <th className={[headerCell, "text-right w-16"].join(" ")}>
                  Posts
                </th>
                <th className={[headerCell, "text-left w-40"].join(" ")}>
                  Severity
                </th>
                <th className={[headerCell, "text-right w-[76px]"].join(" ")}>
                  Sentiment
                </th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row, index) => (
                <tr
                  key={`${row.category}-${row.subcategory ?? index}`}
                  onClick={() => handleRowClick(row)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                      handleRowClick(row);
                    }
                  }}
                  aria-label={`View reviews behind ${
                    row.subcategory
                      ? formatSubcategoryLabel(row.subcategory)
                      : formatCategoryLabel(row.category)
                  }`}
                  className={[
                    "border-b border-white/40 last:border-b-0",
                    "hover:bg-white/40",
                    "transition-colors outline-none cursor-pointer",
                    "focus:bg-white/40",
                  ].join(" ")}
                >
                  <td className="px-5 py-3.5 tabular text-[13px] text-muted-light">
                    {String(row.rank).padStart(2, "0")}
                  </td>
                  <td className="px-5 py-3.5">
                    <div className="text-[15px] font-bold text-ink">
                      {row.subcategory
                        ? formatSubcategoryLabel(row.subcategory)
                        : formatCategoryLabel(row.category)}
                    </div>
                    <div className="mt-1">
                      <span
                        className={[
                          "inline-block px-2.5 py-[2px]",
                          "text-[11px] rounded-full",
                          "bg-white/70 border border-white/60",
                          "text-[#5F6893] font-semibold",
                        ].join(" ")}
                      >
                        {formatCategoryLabel(row.category)}
                      </span>
                    </div>
                  </td>
                  <td className="px-5 py-3.5 text-right tabular text-[13px] text-ink-soft">
                    {formatNumber(row.postCount)}
                  </td>
                  <td className="px-5 py-3.5">
                    <SeverityBar value={row.avgSeverity} />
                  </td>
                  <td className="px-5 py-3.5 text-right">
                    <SentimentPill value={row.avgSentiment} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>

      <CategoryPostsModal
        category={selected?.category ?? null}
        subcategory={selected?.subcategory ?? null}
        onClose={() => setSelected(null)}
      />
    </>
  );
}