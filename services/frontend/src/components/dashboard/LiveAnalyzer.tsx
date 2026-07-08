import { useEffect, useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Sparkles } from "lucide-react";
import { Card, CardHeader } from "@/components/ui/Card";
import { SentimentPill } from "@/components/ui/SentimentPill";
import { SeverityBar } from "@/components/ui/SeverityBar";
import { analyzeText } from "@/api/processing";
import {
  formatCategoryLabel,
  formatSubcategoryLabel,
} from "@/lib/format";

const MIN_LENGTH = 10;
const MAX_LENGTH = 5000;
const SLOW_THRESHOLD_MS = 6000;

export function LiveAnalyzer() {
  const [text, setText] = useState("");
  const [slow, setSlow] = useState(false);
  const slowTimer = useRef<number | null>(null);

  const mutation = useMutation({
    mutationFn: analyzeText,
    onSettled: () => {
      if (slowTimer.current) {
        window.clearTimeout(slowTimer.current);
        slowTimer.current = null;
      }
      setSlow(false);
    },
  });

  useEffect(() => {
    return () => {
      if (slowTimer.current) {
        window.clearTimeout(slowTimer.current);
      }
    };
  }, []);

  const trimmed = text.trim();
  const tooShort = trimmed.length > 0 && trimmed.length < MIN_LENGTH;
  const canSubmit = trimmed.length >= MIN_LENGTH && !mutation.isPending;

  function handleSubmit() {
    if (!canSubmit) {
      return;
    }
    setSlow(false);
    slowTimer.current = window.setTimeout(
      () => setSlow(true),
      SLOW_THRESHOLD_MS
    );
    mutation.mutate(trimmed);
  }

  const result = mutation.data;

  return (
    <Card>
      <CardHeader
        title="Live analyzer"
        subtitle="Type a complaint or review and watch the real NLP pipeline classify it. Nothing you type is stored."
      />

      <div className="px-5 pb-5">
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
              event.preventDefault();
              handleSubmit();
            }
          }}
          maxLength={MAX_LENGTH}
          rows={3}
          placeholder="e.g. the defending is broken and the game keeps crashing after every match"
          className={[
            "w-full resize-none rounded-xl px-4 py-3",
            "text-[14px] leading-relaxed",
            "bg-white/70",
            "border border-white/60",
            "text-ink placeholder:text-faint-light",
            "outline-none focus:ring-2 focus:ring-accent-light/40",
          ].join(" ")}
        />

        <div className="mt-2.5 flex items-center justify-between gap-3">
          <span className="text-[12px] text-muted-light">
            {tooShort
              ? `At least ${MIN_LENGTH} characters`
              : `${trimmed.length}/${MAX_LENGTH}`}
          </span>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={!canSubmit}
            className={[
              "inline-flex items-center gap-1.5",
              "text-[14px] font-semibold px-4 py-2 rounded-xl",
              "transition-opacity outline-none",
              "focus:ring-2 focus:ring-accent-light/40",
              canSubmit
                ? "bg-accent-light text-white hover:opacity-90 cursor-pointer"
                : "bg-white/60 text-faint-light cursor-not-allowed",
            ].join(" ")}
          >
            <Sparkles size={14} />
            {mutation.isPending ? "Analyzing" : "Analyze"}
          </button>
        </div>

        {mutation.isPending ? (
          <p className="mt-3 text-[13px] text-muted-light m-0">
            {slow
              ? "Waking up the NLP model. A cold start can take a minute, every run after this is fast."
              : "Running the pipeline on your text."}
          </p>
        ) : null}

        {mutation.isError ? (
          <p className="mt-3 text-[13px] text-[#C4494C] m-0">
            Analysis failed. The model may still be starting, try again in a
            moment.
          </p>
        ) : null}

        {result && !mutation.isPending ? (
          <div
            className={[
              "mt-3.5 rounded-[14px] px-4 py-3.5",
              "border border-white/60",
              "bg-white/60",
            ].join(" ")}
          >
            <div className="flex flex-wrap items-center gap-2.5">
              <span
                className={[
                  "inline-block px-2.5 py-[2px]",
                  "text-[11px] rounded-full",
                  "bg-white/80 border border-white/70",
                  "text-[#5F6893] font-semibold",
                ].join(" ")}
              >
                {formatCategoryLabel(result.category)}
              </span>
              {result.subcategory ? (
                <span className="text-[14px] font-bold text-ink">
                  {formatSubcategoryLabel(result.subcategory)}
                </span>
              ) : null}
            </div>

            <div className="mt-3 flex flex-wrap items-center gap-5">
              <div className="flex items-center gap-2">
                <span className="text-[12px] text-muted-light">Sentiment</span>
                <SentimentPill value={result.sentiment_score} />
              </div>
              <div className="flex items-center gap-2 min-w-[160px]">
                <span className="text-[12px] text-muted-light">Severity</span>
                <div className="flex-1">
                  <SeverityBar value={result.severity_score} />
                </div>
              </div>
            </div>

            {result.keywords.length > 0 ? (
              <div className="mt-3 flex flex-wrap gap-2">
                {result.keywords.map((keyword) => (
                  <span
                    key={keyword}
                    className={[
                      "inline-block px-2.5 py-[2px]",
                      "text-[11px] rounded-full",
                      "bg-white/80 border border-white/70",
                      "text-muted-light",
                    ].join(" ")}
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}
      </div>
    </Card>
  );
}