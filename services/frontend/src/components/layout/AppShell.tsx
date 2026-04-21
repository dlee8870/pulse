import { ReactNode } from "react";
import { TopBar } from "./TopBar";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-page-light dark:bg-page-dark">
      <TopBar />
      <main className="max-w-[1200px] mx-auto px-5 py-6">{children}</main>
    </div>
  );
}