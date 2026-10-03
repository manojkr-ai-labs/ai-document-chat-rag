"use client";

import {
  LayoutDashboard,
  Upload,
  Database,
  MessageSquare,
  HeartPulse,
  Settings,
} from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

const menuItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    href: "/",
  },
  {
    title: "Upload",
    icon: Upload,
    href: "/upload",
  },
  {
    title: "Documents",
    icon: Database,
    href: "/documents",
  },
  {
    title: "Chat",
    icon: MessageSquare,
    href: "/chat",
  },
  {
    title: "Health",
    icon: HeartPulse,
    href: "/health",
  },
];

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-64 flex-col border-r bg-slate-900 text-white">
      {/* Header */}
      <div className="border-b p-6">
        <h2 className="text-2xl font-bold">
          🤖 AI Document Chat
        </h2>

        <p className="mt-2 text-sm text-slate-400">
          Enterprise RAG
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-2 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <Link
              key={item.title}
              href={item.href}
              className="block"
            >
              <Button
                variant="ghost"
                className="w-full justify-start text-white hover:bg-slate-800"
              >
                <Icon className="mr-2 h-5 w-5" />
                {item.title}
              </Button>
            </Link>
          );
        })}
      </nav>

      {/* Settings */}
      <div className="border-t p-4">
        <Button
          variant="ghost"
          className="w-full justify-start text-slate-400 hover:bg-slate-800"
        >
          <Settings className="mr-2 h-5 w-5" />
          Settings
        </Button>
      </div>
    </aside>
  );
}