interface UploadProgressProps {
  progress: number;
}

export default function UploadProgress({
  progress,
}: UploadProgressProps) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <h3 className="text-lg font-semibold">
        Upload Progress
      </h3>

      <p className="mt-2 text-sm text-gray-500">
        {progress}%
      </p>

      <div className="mt-4 h-3 w-full rounded-full bg-slate-200">
        <div
          className="h-3 rounded-full bg-blue-600 transition-all duration-300"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      <p className="mt-4 text-sm text-gray-500">
        {progress === 100
          ? "Upload completed successfully!"
          : "Uploading document..."}
      </p>
    </div>
  );
}