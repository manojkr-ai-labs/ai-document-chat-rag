"use client";
import { ReactNode } from "react";
import { Button } from "@/components/ui/button";

interface QuickActionProps {
  title: string;
  description: string;
  icon: ReactNode;
  buttonText: string;
  onClick?: () => void;
}

export default function QuickAction({
  title,
  description,
  icon,
  buttonText,
  onClick,
}: QuickActionProps) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm transition-all hover:-translate-y-1 hover:shadow-lg">
      <div className="mb-4 text-blue-600">
        {icon}
      </div>

      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm text-gray-500">
        {description}
      </p>

      <Button
        className="mt-6 w-full"
        onClick={onClick}
      >
        {buttonText}
      </Button>
    </div>
  );
}