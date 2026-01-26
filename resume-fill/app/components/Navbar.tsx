"use client";

import { Bell, User, Puzzle } from "lucide-react"; // Puzzle icon for extension
import Link from "next/link";

export default function Navbar() {
  return (
    <header className="w-full bg-stone-100 px-6 py-4 flex justify-between items-center flex-shrink-0 shadow-sm border-b border-gray-200">
      {/* Left: App Title */}
      <div className="flex items-center gap-3">
        <h1 className="text-2xl font-bold tracking-tight text-black">Resume Fill</h1>
      </div>

      {/* Right: Notifications + Profile + Extension */}
      <div className="flex items-center gap-4">
        {/* Notification */}
        <button className="relative p-2 rounded-full hover:bg-gray-100 transition">
          <Bell className="text-gray-600" />
          <span className="absolute -top-1 -right-1 text-xs w-4 h-4 bg-red-500 text-white rounded-full flex items-center justify-center">
            3
          </span>
        </button>

        {/* Profile */}
        <Link
          href="/profile"
          className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition"
        >
          <User className="text-gray-600" />
          <span className="text-gray-800 font-medium">Archit</span>
        </Link>

        {/* Minimal White Extension Button */}
        <a
          href="https://your-extension-link.com" // replace with your extension link
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center p-2 rounded-full hover:bg-gray-200 transition"
          title="Open Extension"
        >
          <Puzzle className="text-gray-600" />
          <span>Extension</span>
        </a>
      </div>
    </header>
  );
}
