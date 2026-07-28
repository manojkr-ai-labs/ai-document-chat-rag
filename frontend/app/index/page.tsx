"use client";

import { useIndex } from "@/hooks/useIndex";

import IndexButton from "@/components/index/IndexButton";
import IndexResult from "@/components/index/IndexResult";

export default function IndexPage() {
  const indexMutation = useIndex();

  const handleIndex = () => {
    indexMutation.mutate();
  };

  return (
    <div className="mx-auto max-w-3xl space-y-8 p-8">
      <div>
        <h1 className="text-3xl font-bold">
          Index Documents
        </h1>

        <p className="mt-2 text-gray-500">
          Build the vector database from uploaded PDF
          documents.
        </p>
      </div>

      <IndexButton
        onIndex={handleIndex}
        isLoading={indexMutation.isPending}
      />

      {indexMutation.isSuccess && (
        <IndexResult
          success={true}
          message={indexMutation.data.message}
        />
      )}

      {indexMutation.isError && (
        <IndexResult
          success={false}
          message={
            indexMutation.error?.message ??
            "Failed to index documents."
          }
        />
      )}
    </div>
  );
}