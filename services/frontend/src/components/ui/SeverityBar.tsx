import { severityColor } from "@/lib/tone";
import { formatSeverity } from "@/lib/format";

type SeverityBarProps = {
  value: number;
};

export function SeverityBar({ value }: SeverityBarProps) {
  const clamped = Math.max(0, Math.min(1, value));
  const color = severityColor(clamped);

  return (
    <div className="flex items-center gap-2 min-w-[120px]">
      <div className="flex-1 h-[5px] rounded-[3px] bg-track-light dark:bg-track-dark overflow-hidden">
        <div
          className="h-full rounded-[3px]"
          style={{ width: `${Math.round(clamped * 100)}%`, background: color }}
        />
      </div>
      <span className="font-mono tabular text-[11px] text-[#52524E] dark:text-[#9C9C98] min-w-[30px] text-right">
        {formatSeverity(clamped)}
      </span>
    </div>
  );
}