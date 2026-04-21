import { useMemo } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { OverviewStrip } from "@/components/dashboard/OverviewStrip";
import { TopIssuesTable } from "@/components/dashboard/TopIssuesTable";
import { CategoryBreakdown } from "@/components/dashboard/CategoryBreakdown";
import { PatchImpactPanel } from "@/components/dashboard/PatchImpactPanel";
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
        <h1 className="text-lg font-medium tracking-tightish m-0">Overview</h1>
        {lastUpdated ? (
          <span className="text-[11px] text-[#8A8984] dark:text-[#6A6A66]">
            Updated {relativeTime(lastUpdated)}
          </span>
        ) : null}
      </div>
      <p className="text-[13px] text-[#52524E] dark:text-[#9C9C98] mb-5 m-0">
        Community feedback signals from r/EAFC and r/FIFA, classified and ranked.
      </p>

      <OverviewStrip />

      <div className="grid grid-cols-1 lg:grid-cols-[1.45fr_1fr] gap-3 mb-3">
        <TopIssuesTable />
        <CategoryBreakdown />
      </div>

      <PatchImpactPanel />
    </AppShell>
  );
}