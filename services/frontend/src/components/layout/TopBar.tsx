import { LogOut } from "lucide-react";
import { Logo } from "@/components/ui/Logo";
import { ThemeToggle } from "./ThemeToggle";
import { useAuth } from "@/auth/useAuth";

export function TopBar() {
  const { user, logout } = useAuth();

  const initials = user
    ? user.username.slice(0, 2).toUpperCase()
    : "PA";

  return (
    <header
      className={[
        "flex items-center justify-between",
        "px-5 py-3.5",
        "bg-surface-light dark:bg-surface-dark",
        "border-b-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
      ].join(" ")}
    >
      <div className="flex items-center gap-2.5">
        <Logo />
        <span className="text-sm font-medium tracking-tightish">Pulse</span>
        <span
          className={[
            "ml-2 pl-3 text-xs",
            "text-[#8A8984] dark:text-[#6A6A66]",
            "border-l-[0.5px] border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
          ].join(" ")}
        >
          EA FC · production
        </span>
      </div>

      <div className="flex items-center gap-3.5">
        <span className="inline-flex items-center gap-1.5 text-xs text-[#52524E] dark:text-[#9C9C98]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
          Live
        </span>

        <ThemeToggle />

        <div
          className={[
            "inline-flex items-center gap-2",
            "pr-3 pl-1 py-0.5",
            "border-[0.5px] rounded-full",
            "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
            "text-xs",
          ].join(" ")}
        >
          <span
            className={[
              "w-6 h-6 rounded-full flex items-center justify-center",
              "bg-accent-light dark:bg-accent-dark text-white",
              "text-[11px] font-medium",
            ].join(" ")}
          >
            {initials}
          </span>
          <span className="text-[#111110] dark:text-[#F0F0EE]">
            {user?.username ?? "user"}
          </span>
        </div>

        <button
          type="button"
          onClick={logout}
          aria-label="Sign out"
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
          <LogOut size={14} />
        </button>
      </div>
    </header>
  );
}