import SidebarItem from "./SidebarItem";

import {Home, Settings, BookOpenCheck, Book } from "lucide-react";
export default function Sidebar() {
  return (
    <aside className="h-screen w-64 border-r border-gray-200 bg-white p-6 flex flex-col">
      <h2 className="text-xl font-bold font-mono tracking-tight mb-8 text-black">
        Resume Fill
      </h2>

      <nav className="flex flex-col gap-1">
        <SidebarItem label="Home" href="/dashboard"  icon ={<Home/>}/>
        <SidebarItem label="Job Recs" href="/dashboard/applications" notificationCount={3} icon={<BookOpenCheck/>}/>
        <SidebarItem label="Settings" href="/dashboard/settings"  icon = {<Settings/>}/>
      </nav>

      <div className="mt-auto text-gray-500 text-sm border-t border-gray-200 pt-6">
        © 2025 — Job Hunt Smart 🚀
      </div>
    </aside>
  );
}
