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
        "bg-surface-light",
        "border border-white/50 rounded-container",
        "shadow-[0_2px_16px_rgba(80,90,180,0.06)]",
        "px-5 py-4",
      ].join(" ")}
    >
      <p className="text-[13px] text-muted-light m-0 mb-2">{label}</p>
      <p
        className={[
          "tabular text-4xl font-bold m-0 tracking-tightest",
          valueClassName,
        ].join(" ")}
      >
        {value}
      </p>
      {sub ? (
        <p className="text-[12px] text-muted-light mt-2">{sub}</p>
      ) : null}
    </div>
  );
}

function TileSkeleton() {
  return (
    <div
      className={[
        "bg-surface-light",
        "border border-white/50 rounded-container",
        "px-5 py-4",
      ].join(" ")}
    >
      <Skeleton className="h-3.5 w-24 mb-3" />
      <Skeleton className="h-9 w-16 mb-3" />
      <Skeleton className="h-3 w-28" />
    </div>
  );
}

export function OverviewStrip() {
  const trends = useTrendsOverview();
  const issues = useIssuesSummary();

  const isLoading = trends.isLoading || issues.isLoading;

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5 mb-5">
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

  const sentimentColor = avgSentiment < -0.3 ? "text-[#C4494C]" : avgSentiment > 0.3 ? "text-[#0E8F62]" : "";
  const criticalColor = criticalIssues > 0 ? "text-[#C4494C]" : "";

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
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5 mb-5">
      <Tile
        label="Total posts"
        value={formatNumber(totalPosts)}
        sub="EA SPORTS FC 26 Steam reviews"
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