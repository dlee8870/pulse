import { ReactNode } from "react";
import { useIssuesSummary, useTrendsOverview } from "@/hooks/useDashboardData";
import { Skeleton } from "@/components/ui/States";
import { formatNumber, formatSentiment } from "@/lib/format";
import type { Issue } from "@/types/api";

type TileProps = {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  valueClassName?: string;
};

function Tile({ label, value, sub, valueClassName = "" }: TileProps) {
  return (
    <div
      className={[
        "bg-surface-light dark:bg-surface-dark",
        "border-[0.5px] rounded-card",
        "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
        "px-4 py-3.5",
      ].join(" ")}
    >
      <p className="text-xs text-[#52524E] dark:text-[#9C9C98] m-0 mb-1.5">
        {label}
      </p>
      <p
        className={[
          "font-mono tabular text-2xl font-medium m-0 tracking-tightest",
          valueClassName,
        ].join(" ")}
      >
        {value}
      </p>
      {sub ? (
        <p className="text-[11px] text-[#8A8984] dark:text-[#6A6A66] mt-1.5">
          {sub}
        </p>
      ) : null}
    </div>
  );
}

function TileSkeleton() {
  return (
    <div
      className={[
        "bg-surface-light dark:bg-surface-dark",
        "border-[0.5px] rounded-card",
        "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
        "px-4 py-3.5",
      ].join(" ")}
    >
      <Skeleton className="h-3 w-20 mb-2" />
      <Skeleton className="h-7 w-16 mb-2" />
      <Skeleton className="h-2.5 w-24" />
    </div>
  );
}

export function OverviewStrip() {
  const trends = useTrendsOverview();
  const issues = useIssuesSummary();

  const isLoading = trends.isLoading || issues.isLoading;

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5 mb-4">
        <TileSkeleton />
        <TileSkeleton />
        <TileSkeleton />
        <TileSkeleton />
      </div>
    );
  }

  const totalPosts = trends.data?.totalProcessed ?? 0;
  const avgSentiment = trends.data?.avgSentiment ?? 0;
  const allIssues: Issue[] = issues.data?.items ?? [];
  const openIssues: Issue[] = allIssues.filter(
    (issue: Issue) => issue.status !== "closed" && issue.status !== "resolved"
  );
  const byStatus: Record<string, number> = openIssues.reduce(
    (acc: Record<string, number>, issue: Issue) => {
      acc[issue.status] = (acc[issue.status] ?? 0) + 1;
      return acc;
    },
    {} as Record<string, number>
  );
  const criticalIssues: number = openIssues.filter(
    (issue: Issue) => issue.severity === "critical"
  ).length;

  const sentimentColor =
    avgSentiment < -0.3
      ? "text-[#DC2626] dark:text-[#F87171]"
      : avgSentiment > 0.3
      ? "text-[#047857] dark:text-[#6EE7B7]"
      : "";

  const criticalColor =
    criticalIssues > 0 ? "text-[#DC2626] dark:text-[#F87171]" : "";

  const statusParts: string[] = [];
  if (byStatus.open) {
    statusParts.push(`${byStatus.open} open`);
  }
  if (byStatus.investigating) {
    statusParts.push(`${byStatus.investigating} investigating`);
  }
  if (byStatus.acknowledged) {
    statusParts.push(`${byStatus.acknowledged} acknowledged`);
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5 mb-4">
      <Tile
        label="Total posts"
        value={formatNumber(totalPosts)}
        sub="Across r/EAFC and r/FIFA"
      />
      <Tile
        label="Average sentiment"
        value={formatSentiment(avgSentiment)}
        valueClassName={sentimentColor}
        sub={
          avgSentiment < 0
            ? "Negative leaning"
            : avgSentiment > 0
            ? "Positive leaning"
            : "Neutral"
        }
      />
      <Tile
        label="Open issues"
        value={formatNumber(openIssues.length)}
        sub={statusParts.length > 0 ? statusParts.join(" · ") : "None active"}
      />
      <Tile
        label="Critical issues"
        value={formatNumber(criticalIssues)}
        valueClassName={criticalColor}
        sub="Severity above 0.85"
      />
    </div>
  );
}