import { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  className?: string;
};

export function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={[
        "bg-surface-light dark:bg-surface-dark",
        "border-[0.5px] rounded-card",
        "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
        "overflow-hidden",
        className,
      ].join(" ")}
    >
      {children}
    </div>
  );
}

type CardHeaderProps = {
  title: string;
  subtitle?: string;
  right?: ReactNode;
};

export function CardHeader({ title, subtitle, right }: CardHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-3 px-4 pt-3.5 pb-2.5">
      <div>
        <p className="text-sm font-medium tracking-tightish m-0">{title}</p>
        {subtitle ? (
          <p className="text-xs text-[#52524E] dark:text-[#9C9C98] mt-0.5">
            {subtitle}
          </p>
        ) : null}
      </div>
      {right}
    </div>
  );
}