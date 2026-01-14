import SidebarItem from "./SidebarItem";
import { Home, Settings, BookOpenCheck, User } from "lucide-react";

interface SidebarProps {
  className?: string;
}

export default function Sidebar({ className = "" }: SidebarProps) {
  return (
    <aside
      className={`flex flex-col w-64 border-r border-gray-200 bg-white p-6 ${className}`}
    >
      {/* Logo / Title - stays fixed */}
      <h2 className="text-xl font-bold font-mono tracking-tight mb-8 text-black flex-shrink-0">
        Resume Fill
      </h2>

      {/* Scrollable area: nav */}
      <nav className="flex-1 flex flex-col gap-1 overflow-auto">
        <SidebarItem label="Home" href="/dashboard" icon={<Home />} />
        <SidebarItem
          label="Job Recs"
          href="/job-recommendations"
          notificationCount={3}
          icon={<BookOpenCheck />}
        />
        <SidebarItem label="Settings" href="/settings" icon={<Settings />} />
      </nav>

      {/* Footer - pinned */}
      <div className="mt-auto border-t border-gray-200 pt-6 flex flex-col gap-3 flex-shrink-0">
        <SidebarItem label="Account" href="/profile" icon={<User />} />
      </div>
    </aside>
  );
}
