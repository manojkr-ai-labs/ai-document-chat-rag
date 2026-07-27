import { Database } from "lucide-react";
import DashboardCard from "./DashboardCard";

interface StatsCardProps {
  documents: number;
  chunks: number;
}

export default function StatsCard({
  documents,
  chunks,
}: StatsCardProps) {
  return (
    <DashboardCard
      title="Statistics"
      description="Indexed document overview"
      icon={<Database className="h-6 w-6" />}
    >
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-500">
            Documents
          </p>

          <p className="text-2xl font-bold">
            {documents}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Chunks
          </p>

          <p className="text-2xl font-bold">
            {chunks}
          </p>
        </div>
      </div>
    </DashboardCard>
  );
}