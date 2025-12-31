"use client";

import { Bell, User } from "lucide-react";
import Link from "next/link";

export default function Navbar() {
  return (
    <header className="w-full bg-white border-b border-gray-200 shadow-sm px-6 py-4 flex justify-between items-center">
      {/* Left side: logo / title */}
      <div className="flex items-center gap-3">
        <h1 className="text-2xl font-bold tracking-tight text-black">Resume Fill</h1>
      </div>

      {/* Right side: notifications + profile */}
      <div className="flex items-center gap-4">
        {/* Notification Icon */}
        <button className="relative p-2 rounded-full hover:bg-gray-100 transition">
          <Bell className="text-gray-600" />
          <span className="absolute -top-1 -right-1 text-xs w-4 h-4 bg-red-500 text-white rounded-full flex items-center justify-center">
            3
          </span>
        </button>

        {/* Profile / Account Link */}
        <Link href="/profile" className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition">
          <User className="text-gray-600" />
          <span className="text-gray-800 font-medium">Archit</span>
        </Link>
      </div>
    </header>
  );
}
