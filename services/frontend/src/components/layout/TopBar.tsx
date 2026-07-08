import { LogOut } from "lucide-react";
import { Logo } from "@/components/ui/Logo";
import { useAuth } from "@/auth/useAuth";

export function TopBar() {
  const { user, logout } = useAuth();

  const initials = user ? user.username.slice(0, 2).toUpperCase() : "PA";

  return (
    <header
      className={[
        "flex items-center justify-between",
        "px-5 py-3.5",
        "bg-white/30 backdrop-blur-sm",
        "border-b border-white/40",
      ].join(" ")}
    >
      <div className="flex items-center gap-2.5">
        <Logo />
        <span className="text-sm font-bold tracking-tightish">Pulse</span>
        <span className="ml-2 pl-3 text-xs text-muted-light border-l border-white/50">
          EA FC · production
        </span>
      </div>

      <div className="flex items-center gap-3.5">
        <span className="inline-flex items-center gap-1.5 text-xs text-muted-light">
          <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
          Live
        </span>

        <div
          className={[
            "inline-flex items-center gap-2",
            "pr-3 pl-1 py-0.5",
            "border border-white/50 rounded-full bg-white/30",
            "text-xs",
          ].join(" ")}
        >
          <span
            className={[
              "w-6 h-6 rounded-full flex items-center justify-center",
              "bg-accent-light text-white",
              "text-[11px] font-semibold",
            ].join(" ")}
          >
            {initials}
          </span>
          <span className="text-ink">{user?.username ?? "user"}</span>
        </div>

        <button
          type="button"
          onClick={logout}
          aria-label="Sign out"
          className={[
            "w-8 h-8 rounded-lg inline-flex items-center justify-center",
            "border border-white/50 bg-white/30",
            "text-muted-light",
            "hover:bg-white/60",
            "transition-colors outline-none",
            "focus:ring-2 focus:ring-accent-light/30",
          ].join(" ")}
        >
          <LogOut size={14} />
        </button>
      </div>
    </header>
  );
}