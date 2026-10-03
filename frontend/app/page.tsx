import StatusCard from "@/components/dashboard/StatusCard";
import StatsCard from "@/components/dashboard/StatsCard";
import QuickActions from "@/components/dashboard/QuickActions";

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="grid gap-6 md:grid-cols-2">
        <StatusCard healthy={true} />
        <StatsCard documents={1243} chunks={8542} />
      </div>

      <QuickActions />
    </div>
  );
}