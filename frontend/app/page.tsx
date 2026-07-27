import DashboardLayout from "@/components/layout/DashboardLayout";
import StatusCard from "@/components/dashboard/StatusCard";
import StatsCard from "@/components/dashboard/StatsCard";

export default function Home() {
  return (
    <DashboardLayout>
      <div className="grid grid-cols-2 gap-6">
        <StatusCard healthy={true} />
        <StatsCard
          documents={1243}
          chunks={8542}
        />
      </div>
    </DashboardLayout>
  );
}