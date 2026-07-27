import { ReactNode } from "react";

interface DashboardCardProps {
  title: string;
  description?: string;
  icon?: ReactNode;
  children?: ReactNode;
}

export default function DashboardCard({
  title,
  description,
  icon,
  children,
}: DashboardCardProps) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm transition hover:shadow-md">
      <div className="mb-4 flex items-center gap-3">
        <div className="text-blue-600">
          {icon}
        </div>

        <div>
          <h2 className="text-lg font-semibold">
            {title}
          </h2>

          {description && (
            <p className="text-sm text-gray-500">
              {description}
            </p>
          )}
        </div>
      </div>

      <div>
        {children}
      </div>
    </div>
  );
}