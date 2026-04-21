import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/theme/useTheme";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
      className={[
        "w-8 h-8 rounded-md inline-flex items-center justify-center",
        "border-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
        "bg-surface-light dark:bg-surface-dark",
        "text-[#52524E] dark:text-[#9C9C98]",
        "hover:bg-hover-light dark:hover:bg-hover-dark",
        "transition-colors outline-none",
        "focus:ring-2 focus:ring-accent-light/30 dark:focus:ring-accent-dark/30",
      ].join(" ")}
    >
      {isDark ? <Sun size={14} /> : <Moon size={14} />}
    </button>
  );
}