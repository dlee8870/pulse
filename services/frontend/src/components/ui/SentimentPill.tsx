import { sentimentTone } from "@/lib/tone";
import { formatSentiment } from "@/lib/format";
import { useTheme } from "@/theme/useTheme";

type SentimentPillProps = {
  value: number;
};

export function SentimentPill({ value }: SentimentPillProps) {
  const { theme } = useTheme();
  const tone = sentimentTone(value, theme === "dark");

  return (
    <span
      className="inline-block px-[7px] py-[2px] rounded font-mono tabular text-[11px]"
      style={{ background: tone.bg, color: tone.fg }}
    >
      {formatSentiment(value)}
    </span>
  );
}