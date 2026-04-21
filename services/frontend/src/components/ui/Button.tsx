import { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  children: ReactNode;
};

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    "bg-accent-light dark:bg-accent-dark text-white hover:opacity-90 disabled:opacity-60",
  secondary:
    "bg-surface-light dark:bg-surface-dark text-[#111110] dark:text-[#F0F0EE] border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)] hover:bg-hover-light dark:hover:bg-hover-dark",
  ghost:
    "text-[#52524E] dark:text-[#9C9C98] hover:bg-hover-light dark:hover:bg-hover-dark",
};

export function Button({
  variant = "primary",
  className = "",
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={[
        "h-9 px-4 rounded-md text-sm font-medium",
        "transition-colors outline-none",
        "focus:ring-2 focus:ring-accent-light/30 dark:focus:ring-accent-dark/30",
        "disabled:cursor-not-allowed",
        variantClasses[variant],
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </button>
  );
}