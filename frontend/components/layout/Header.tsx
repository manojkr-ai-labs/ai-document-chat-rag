import { Bot, Bell, UserCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Header() {
  return (
    <header className="flex items-center justify-between border-b bg-white px-6 py-4 shadow-sm">
      <div className="flex items-center gap-3">
        <Bot className="h-8 w-8 text-blue-600" />

        <div>
          <h1 className="text-xl font-bold">
            AI Document Chat
          </h1>

          <p className="text-sm text-gray-500">
            Enterprise RAG Assistant
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
          ● Online
        </span>

        <Button variant="ghost" size="icon">
          <Bell className="h-5 w-5" />
        </Button>

        <Button variant="ghost" size="icon">
          <UserCircle className="h-7 w-7" />
        </Button>
      </div>
    </header>
  );
}