import { formatMessageTime } from "@/lib/date";

interface MessageTimestampProps {
  timestamp?: string | Date;
}

export default function MessageTimestamp({
  timestamp,
}: MessageTimestampProps) {
  if (!timestamp) return null;

  const date =
    timestamp instanceof Date
      ? timestamp
      : new Date(timestamp);

  return (
    <div className="mt-2 text-xs text-slate-400">
      {formatMessageTime(timestamp)}
    </div>
  );
}