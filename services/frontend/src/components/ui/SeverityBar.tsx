import { severityColor } from "@/lib/tone";
import { formatSeverity } from "@/lib/format";

type SeverityBarProps = {
  value: number;
};

export function SeverityBar({ value }: SeverityBarProps) {
  const clamped = Math.max(0, Math.min(1, value));
  const color = severityColor(clamped);

  return (
    <div className="flex items-center gap-2.5 min-w-[120px]">
      <div className="flex-1 h-[7px] rounded-full bg-white/70 overflow-hidden">
        <div
          className="h-full rounded-full"
          style={{ width: `${Math.round(clamped * 100)}%`, background: color }}
        />
      </div>
      <span className="font-mono tabular text-[12px] text-ink-soft min-w-[32px] text-right">
        {formatSeverity(clamped)}
      </span>
    </div>
  );
}