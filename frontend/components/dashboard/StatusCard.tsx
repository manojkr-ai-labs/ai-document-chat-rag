import { HeartPulse } from "lucide-react";
import DashboardCard from "./DashboardCard";

interface StatusCardProps {
  healthy: boolean;
}

export default function StatusCard({
  healthy,
}: StatusCardProps) {
  return (
    <DashboardCard
      title="System Health"
      description="Current backend status"
      icon={<HeartPulse className="h-6 w-6" />}
    >
      <div className="space-y-2">
        <p className="text-sm text-gray-600">
          Backend
        </p>

        <span
          className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${
            healthy
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {healthy ? "Healthy" : "Offline"}
        </span>
      </div>
    </DashboardCard>
  );
}