import SidebarItem from "./SidebarItem";
import { Home, Settings, BookOpenCheck, User } from "lucide-react";

interface SidebarProps {
  className?: string;
}

export default function Sidebar({ className = "" }: SidebarProps) {
  return (
    <aside className={`h-screen w-64 border-r border-gray-200 bg-white p-6 flex flex-col ${className}`}>
      <h2 className="text-xl font-bold font-mono tracking-tight mb-8 text-black">
        Resume Fill
      </h2>

      <nav className="flex flex-col gap-1">
        <SidebarItem label="Home" href="/dashboard" icon={<Home />} />
        <SidebarItem
          label="Job Recs"
          href="/dashboard/applications"
          notificationCount={3}
          icon={<BookOpenCheck />}
        />
        <SidebarItem label="Settings" href="/settings" icon={<Settings />} />
      </nav>

      {/* Footer */}
      <div className="mt-auto border-t border-gray-200 pt-6 flex flex-col gap-3">
        <SidebarItem label="Account" href="/profile" icon={<User />} />
      </div>
    </aside>
  );
}
