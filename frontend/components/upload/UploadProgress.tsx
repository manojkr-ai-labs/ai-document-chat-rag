"use client";

interface UploadProgressProps {
  status: string;
}

export default function UploadProgress({
  status,
}: UploadProgressProps) {
  const completed = status === "completed";

  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <h3 className="text-lg font-semibold">
        Upload Progress
      </h3>

      <p className="mt-2 text-sm text-gray-500">
        Status: {status}
      </p>

      <div className="mt-4 h-3 w-full rounded-full bg-slate-200">
        <div
          className={`h-3 rounded-full transition-all duration-300 ${
            completed ? "bg-green-600" : "bg-blue-600"
          }`}
          style={{
            width: completed ? "100%" : "50%",
          }}
        />
      </div>

      <p className="mt-4 text-sm text-gray-500">
        {completed
          ? "Document indexed successfully!"
          : "Processing document..."}
      </p>
    </div>
  );
}