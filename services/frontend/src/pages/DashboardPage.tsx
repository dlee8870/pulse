import { useMemo } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { OverviewStrip } from "@/components/dashboard/OverviewStrip";
import { TopIssuesTable } from "@/components/dashboard/TopIssuesTable";
import { CategoryBreakdown } from "@/components/dashboard/CategoryBreakdown";
import { PatchImpactPanel } from "@/components/dashboard/PatchImpactPanel";
import { LiveAnalyzer } from "@/components/dashboard/LiveAnalyzer";
import { useTrendsOverview } from "@/hooks/useDashboardData";
import { relativeTime } from "@/lib/format";

export function DashboardPage() {
  const { dataUpdatedAt, isFetched } = useTrendsOverview();

  const lastUpdated = useMemo(() => {
    if (!isFetched || !dataUpdatedAt) {
      return null;
    }
    return new Date(dataUpdatedAt).toISOString();
  }, [dataUpdatedAt, isFetched]);

  return (
    <AppShell>
      <div className="mb-1 flex items-baseline gap-2.5">
        <h1 className="text-[26px] font-bold tracking-tightish m-0">
          Overview
        </h1>
        {lastUpdated ? (
          <span className="text-[12px] text-muted-light">
            Updated {relativeTime(lastUpdated)}
          </span>
        ) : null}
      </div>
      <p className="text-[14px] text-muted-light mb-6 m-0">
        EA SPORTS FC 26 player reviews from Steam, classified and ranked.
      </p>

      <OverviewStrip />

      <div className="grid grid-cols-1 lg:grid-cols-[1.45fr_1fr] gap-3.5">
        <TopIssuesTable />
        <div className="flex flex-col gap-3.5">
          <CategoryBreakdown />
          <PatchImpactPanel />
        </div>
      </div>

      <div className="mt-3.5">
        <LiveAnalyzer />
      </div>
    </AppShell>
  );
}