import { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  className?: string;
};

export function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={[
        "bg-surface-light",
        "border border-white/50 rounded-container",
        "shadow-[0_2px_16px_rgba(80,90,180,0.06)]",
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
    <div className="flex items-start justify-between gap-3 px-5 pt-4 pb-3">
      <div>
        <p className="text-[17px] font-bold tracking-tightish m-0">{title}</p>
        {subtitle ? (
          <p className="text-[13px] text-muted-light mt-1">{subtitle}</p>
        ) : null}
      </div>
      {right}
    </div>
  );
}