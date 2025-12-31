"use client";

import "./globals.css";
import Sidebar from "./components/Sidebar";// make sure you create this
import { usePathname } from "next/navigation";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Routes that should show sidebar and topbar
  const sidebarRoutes = ["/", "/intro"];
  const showSidebar = sidebarRoutes.some(
    route => pathname === route || pathname.startsWith(route + "/")
  );

  return (
    <html lang="en">
      <body className="bg-neutral-950 text-white min-h-screen">
        <div className="flex min-h-screen">
          {/* Sidebar */}
          {showSidebar && <Sidebar />}


            <div className="flex-1 flex flex-col">

              <main className="">{children}</main>
            </div>
        </div>
      </body>
    </html>
  );
}