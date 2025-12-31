"use client";

import "./globals.css";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import { usePathname } from "next/navigation";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Routes that show sidebar/navbar
  const dashboardRoutes = ["/", "/intro", "/dashboard", "/profile", "/settings"];
  const showSidebar = dashboardRoutes.some(
    route => pathname === route || pathname.startsWith(route + "/")
  );

  return (
    <html lang="en">
      <body className="bg-gray-50 text-black">
        <div className="flex h-screen">
          {/* Sidebar */}
          {showSidebar && <Sidebar />}

          {/* Main content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Navbar */}
            {showSidebar && <Navbar />}

            {/* Main scrollable area */}
            <main className="flex-1 overflow-auto p-6">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
