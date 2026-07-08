import { useEffect, useState } from "react";
import { Card, CardHeader } from "@/components/ui/Card";
import { EmptyState, ErrorState, Skeleton } from "@/components/ui/States";
import { usePatchImpact, usePatches } from "@/hooks/useDashboardData";
import type { PatchPeriodMetrics } from "@/types/api";
import {
  formatNumber,
  formatSentiment,
  formatSeverity,
} from "@/lib/format";

function formatDateOnly(value: string): string {
  const datePart = value.slice(0, 10);
  const [year, month, day] = datePart.split("-").map(Number);
  if (!year || !month || !day) {
    return value;
  }
  return new Date(year, month - 1, day).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: undefined,
  });
}

function formatDateWithYear(value: string): string {
  const datePart = value.slice(0, 10);
  const [year, month, day] = datePart.split("-").map(Number);
  if (!year || !month || !day) {
    return value;
  }
  return new Date(year, month - 1, day).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function shiftDate(value: string, days: number): string {
  const datePart = value.slice(0, 10);
  const [year, month, day] = datePart.split("-").map(Number);
  const shifted = new Date(year, month - 1, day + days);
  const mm = String(shifted.getMonth() + 1).padStart(2, "0");
  const dd = String(shifted.getDate()).padStart(2, "0");
  return `${shifted.getFullYear()}-${mm}-${dd}`;
}

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
    return <span className="text-[12px] ml-1.5 text-faint-light">±0</span>;
  }
  const isPositive = value > 0;
  const isGood = positiveIsGood ? isPositive : !isPositive;
  const color = isGood ? "text-[#0E8F62]" : "text-[#C4494C]";
  const arrow = isPositive ? "↑" : "↓";
  const display = showPercent
    ? `${formatter(Math.abs(value))}%`
    : formatter(Math.abs(value));

  return (
    <span
      className={["text-[12px] ml-1.5 font-semibold", color].join(" ")}
      aria-label={label}
    >
      {arrow} {display}
    </span>
  );
}

type PeriodBlockProps = {
  title: string;
  start: string;
  end: string;
  metrics: PatchPeriodMetrics;
  compare?: PatchPeriodMetrics;
};

function PeriodBlock({ title, start, end, metrics, compare }: PeriodBlockProps) {
  const sentimentChange = compare
    ? metrics.avgSentiment - compare.avgSentiment
    : 0;
  const severityChange = compare
    ? metrics.avgSeverity - compare.avgSeverity
    : 0;
  const postsChangePercent =
    compare && compare.postCount > 0
      ? ((metrics.postCount - compare.postCount) / compare.postCount) * 100
      : 0;

  return (
    <div className="py-1">
      <div className="flex items-baseline justify-between mb-2">
        <span className="text-[15px] font-bold text-ink">{title}</span>
        <span className="text-[12px] text-muted-light">
          {formatDateOnly(start)} — {formatDateOnly(end)}
        </span>
      </div>
      <div className="flex justify-between items-baseline py-1.5 text-[13px]">
        <span className="text-muted-light">Posts</span>
        <span className="tabular font-semibold text-ink">
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
      <div className="flex justify-between items-baseline py-1.5 text-[13px]">
        <span className="text-muted-light">Avg sentiment</span>
        <span className="tabular font-semibold text-ink">
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
      <div className="flex justify-between items-baseline py-1.5 text-[13px]">
        <span className="text-muted-light">Avg severity</span>
        <span className="tabular font-semibold text-ink">
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

  const sortedPatches = patches.data
    ? [...patches.data].sort(
        (a, b) =>
          new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime()
      )
    : [];

  useEffect(() => {
    if (!selectedPatchId && sortedPatches.length > 0) {
      setSelectedPatchId(sortedPatches[0].id);
    }
  }, [sortedPatches, selectedPatchId]);

  const impact = usePatchImpact(selectedPatchId);

  const releaseDate = impact.data?.patch.releaseDate ?? "";
  const preStart = releaseDate ? shiftDate(releaseDate, -7) : "";
  const preEnd = releaseDate;
  const postStart = releaseDate;
  const postEnd = releaseDate ? shiftDate(releaseDate, 7) : "";

  const selectRight = (
    <select
      value={selectedPatchId ?? ""}
      onChange={(event) => setSelectedPatchId(event.target.value)}
      disabled={patches.isLoading || sortedPatches.length === 0}
      className={[
        "text-[13px] px-3 py-2 rounded-lg",
        "bg-white/70",
        "text-ink font-semibold",
        "border border-white/60",
        "focus:outline-none focus:ring-2 focus:ring-accent-light/30",
        "disabled:opacity-60 disabled:cursor-not-allowed",
      ].join(" ")}
    >
      {sortedPatches.length === 0 ? (
        <option value="">No patches registered</option>
      ) : (
        sortedPatches.map((patch) => (
          <option key={patch.id} value={patch.id}>
            {patch.version} — {formatDateWithYear(patch.releaseDate)}
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
        <div className="px-5 pb-5 pt-1">
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
        <div className="px-5 pb-5 pt-1 space-y-3">
          <Skeleton className="h-28" />
          <Skeleton className="h-28" />
        </div>
      ) : impact.isError ? (
        <ErrorState
          message="Could not load patch impact."
          onRetry={() => impact.refetch()}
        />
      ) : impact.data ? (
        <div className="px-5 pb-5 pt-1">
          <PeriodBlock
            title="Before"
            start={preStart}
            end={preEnd}
            metrics={impact.data.prePatch}
          />
          <div className="border-t border-white/60 my-2.5" />
          <PeriodBlock
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