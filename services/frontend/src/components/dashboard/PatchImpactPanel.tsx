import { useEffect, useState } from "react";
import { Card, CardHeader } from "@/components/ui/Card";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/States";
import { usePatchImpact, usePatches } from "@/hooks/useDashboardData";
import type { PatchPeriodMetrics } from "@/types/api";
import {
  formatIsoDate,
  formatNumber,
  formatSentiment,
  formatSeverity,
  formatShortDate,
} from "@/lib/format";

type DeltaProps = {
  label: string;
  value: number;
  formatter: (value: number) => string;
  positiveIsGood: boolean;
  showPercent?: boolean;
};

function Delta({
  label,
  value,
  formatter,
  positiveIsGood,
  showPercent = false,
}: DeltaProps) {
  if (value === 0) {
    return <span className="text-[11px] ml-1.5 text-[#8A8984] dark:text-[#6A6A66]">±0</span>;
  }
  const isPositive = value > 0;
  const isGood = positiveIsGood ? isPositive : !isPositive;
  const color = isGood
    ? "text-[#047857] dark:text-[#6EE7B7]"
    : "text-[#B91C1C] dark:text-[#FCA5A5]";
  const arrow = isPositive ? "↑" : "↓";
  const display = showPercent
    ? `${formatter(Math.abs(value))}%`
    : formatter(Math.abs(value));

  return (
    <span className={["text-[11px] ml-1.5", color].join(" ")} aria-label={label}>
      {arrow} {display}
    </span>
  );
}

type PeriodCardProps = {
  title: string;
  start: string;
  end: string;
  metrics: PatchPeriodMetrics;
  compare?: PatchPeriodMetrics;
};

function PeriodCard({ title, start, end, metrics, compare }: PeriodCardProps) {
  const sentimentChange = compare ? metrics.avgSentiment - compare.avgSentiment : 0;
  const severityChange = compare ? metrics.avgSeverity - compare.avgSeverity : 0;
  const postsChangePercent =
    compare && compare.postCount > 0
      ? ((metrics.postCount - compare.postCount) / compare.postCount) * 100
      : 0;

  return (
    <div
      className={[
        "bg-page-light dark:bg-page-dark",
        "border-[0.5px] rounded-md px-3.5 py-3",
        "border-[rgba(0,0,0,0.05)] dark:border-[rgba(255,255,255,0.04)]",
      ].join(" ")}
    >
      <div className="flex items-baseline justify-between mb-2.5">
        <span className="text-xs font-medium">{title}</span>
        <span className="font-mono text-[11px] text-[#8A8984] dark:text-[#6A6A66]">
          {formatShortDate(start)} — {formatShortDate(end)}
        </span>
      </div>
      <div className="flex justify-between items-baseline py-1 text-xs">
        <span className="text-[#52524E] dark:text-[#9C9C98]">Posts</span>
        <span className="font-mono tabular font-medium">
          {formatNumber(metrics.postCount)}
          {compare ? (
            <Delta
              label="Post count change"
              value={postsChangePercent}
              formatter={(v) => v.toFixed(1)}
              positiveIsGood={false}
              showPercent
            />
          ) : null}
        </span>
      </div>
      <div className="flex justify-between items-baseline py-1 text-xs">
        <span className="text-[#52524E] dark:text-[#9C9C98]">Avg sentiment</span>
        <span className="font-mono tabular font-medium">
          {formatSentiment(metrics.avgSentiment)}
          {compare ? (
            <Delta
              label="Sentiment change"
              value={sentimentChange}
              formatter={(v) => v.toFixed(2)}
              positiveIsGood
            />
          ) : null}
        </span>
      </div>
      <div className="flex justify-between items-baseline py-1 text-xs">
        <span className="text-[#52524E] dark:text-[#9C9C98]">Avg severity</span>
        <span className="font-mono tabular font-medium">
          {formatSeverity(metrics.avgSeverity)}
          {compare ? (
            <Delta
              label="Severity change"
              value={severityChange}
              formatter={(v) => v.toFixed(2)}
              positiveIsGood={false}
            />
          ) : null}
        </span>
      </div>
    </div>
  );
}

export function PatchImpactPanel() {
  const patches = usePatches();
  const [selectedPatchId, setSelectedPatchId] = useState<string | null>(null);

  useEffect(() => {
    if (!selectedPatchId && patches.data && patches.data.length > 0) {
      setSelectedPatchId(patches.data[0].id);
    }
  }, [patches.data, selectedPatchId]);

  const impact = usePatchImpact(selectedPatchId);

  const sortedPatches = patches.data
    ? [...patches.data].sort(
        (a, b) =>
          new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime()
      )
    : [];

  const releaseDate = impact.data?.patch.releaseDate;
  const preStart = releaseDate
    ? new Date(new Date(releaseDate).getTime() - 7 * 86400000).toISOString()
    : "";
  const preEnd = releaseDate ?? "";
  const postStart = releaseDate ?? "";
  const postEnd = releaseDate
    ? new Date(new Date(releaseDate).getTime() + 7 * 86400000).toISOString()
    : "";

  const selectRight = (
    <select
      value={selectedPatchId ?? ""}
      onChange={(event) => setSelectedPatchId(event.target.value)}
      disabled={patches.isLoading || sortedPatches.length === 0}
      className={[
        "text-xs px-2.5 py-1.5 rounded-md",
        "bg-surface-light dark:bg-surface-dark",
        "text-[#111110] dark:text-[#F0F0EE]",
        "border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
        "focus:outline-none focus:ring-2 focus:ring-accent-light/30 dark:focus:ring-accent-dark/30",
        "disabled:opacity-60 disabled:cursor-not-allowed",
      ].join(" ")}
    >
      {sortedPatches.length === 0 ? (
        <option value="">No patches registered</option>
      ) : (
        sortedPatches.map((patch) => (
          <option key={patch.id} value={patch.id}>
            {patch.version} — {formatIsoDate(patch.releaseDate)}
          </option>
        ))
      )}
    </select>
  );

  return (
    <Card>
      <CardHeader
        title="Patch impact"
        subtitle="Seven days before vs seven days after release"
        right={selectRight}
      />

      {patches.isLoading ? (
        <div className="px-4 pb-4 pt-1">
          <Skeleton className="h-32" />
        </div>
      ) : patches.isError ? (
        <ErrorState
          message="Could not load patches."
          onRetry={() => patches.refetch()}
        />
      ) : sortedPatches.length === 0 ? (
        <EmptyState
          message="No patches registered yet."
          hint="Register a patch via POST /api/patches to see impact analysis."
        />
      ) : impact.isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 px-4 pb-4 pt-1.5">
          <Skeleton className="h-36" />
          <Skeleton className="h-36" />
        </div>
      ) : impact.isError ? (
        <ErrorState
          message="Could not load patch impact."
          onRetry={() => impact.refetch()}
        />
      ) : impact.data ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 px-4 pb-4 pt-1.5">
          <PeriodCard
            title="Before"
            start={preStart}
            end={preEnd}
            metrics={impact.data.prePatch}
          />
          <PeriodCard
            title="After"
            start={postStart}
            end={postEnd}
            metrics={impact.data.postPatch}
            compare={impact.data.prePatch}
          />
        </div>
      ) : null}
    </Card>
  );
}