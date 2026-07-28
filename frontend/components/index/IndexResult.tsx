import { CheckCircle2, CircleAlert } from "lucide-react";

interface IndexResultProps {
  success: boolean;
  message: string;
}

export default function IndexResult({
  success,
  message,
}: IndexResultProps) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <div className="flex items-center gap-3">
        {success ? (
          <CheckCircle2 className="h-8 w-8 text-green-600" />
        ) : (
          <CircleAlert className="h-8 w-8 text-red-600" />
        )}

        <h3 className="text-lg font-semibold">
          {success ? "Index Completed" : "Index Failed"}
        </h3>
      </div>

      <p className="mt-4 text-sm text-gray-600">
        {message}
      </p>

      <span
        className={`mt-4 inline-flex rounded-full px-3 py-1 text-sm font-medium ${
          success
            ? "bg-green-100 text-green-700"
            : "bg-red-100 text-red-700"
        }`}
      >
        {success ? "Completed" : "Failed"}
      </span>
    </div>
  );
}