"use client";

import Link from "next/link";
import { ReactNode } from "react";
import { usePathname } from "next/navigation";

interface SidebarItemProps {
  label: string;
  href: string;
  icon?: ReactNode;
  notificationCount?: number;
}

export default function SidebarItem({
  label,
  href,
  icon,
  notificationCount = 0,
}: SidebarItemProps) {
  const pathname = usePathname();
  const active = pathname === href;

  return (
    <Link
      href={href}
      className={`flex items-center justify-between px-4 py-1 transition-all
      ${
        active
          ? "bg-black text-white border-black shadow-md"
          : "bg-white border-gray-200 text-gray-700 hover:bg-gray-100 hover:-translate-y-[1px]"
      }`}
    >
      {/* Left side: icon + label */}
      <div className="flex items-center gap-3">
        {icon && <span className="text-xl">{icon}</span>}
        <span className="font-semibold tracking-wide">{label}</span>
      </div>

      {/* Right side: notification bubble */}
      {notificationCount > 0 && (
        <span className="text-xs px-2 py-0.5 rounded-full bg-black text-white">
          {notificationCount}
        </span>
      )}
    </Link>
  );
}
