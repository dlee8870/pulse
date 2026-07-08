import { sentimentTone } from "@/lib/tone";
import { formatSentiment } from "@/lib/format";

type SentimentPillProps = {
  value: number;
};

export function SentimentPill({ value }: SentimentPillProps) {
  const tone = sentimentTone(value);

  return (
    <span
      className="inline-block px-2 py-[3px] rounded-md font-mono tabular text-[11px] font-semibold"
      style={{ background: tone.bg, color: tone.fg }}
    >
      {formatSentiment(value)}
    </span>
  );
}