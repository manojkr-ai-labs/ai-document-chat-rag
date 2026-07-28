"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

import { useUpload } from "@/hooks/useUpload";

import UploadDropzone from "./UploadDropzone";
import UploadProgress from "./UploadProgress";
import UploadResult from "./UploadResult";

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);

  const uploadMutation = useUpload();

  const handleUpload = () => {
    if (!file) return;

    uploadMutation.mutate(file);
  };

  return (
    <div className="space-y-6">
      <UploadDropzone
        file={file}
        onFileSelect={setFile}
      />

      <Button
        className="w-full"
        onClick={handleUpload}
        disabled={!file || uploadMutation.isPending}
      >
        {uploadMutation.isPending
          ? "Uploading..."
          : "Upload PDF"}
      </Button>

      {uploadMutation.isPending && (
        <UploadProgress progress={50} />
      )}

      {uploadMutation.isSuccess && (
        <UploadResult
          success={true}
          message={uploadMutation.data.message}
        />
      )}

      {uploadMutation.isError && (
        <UploadResult
          success={false}
          message={
            uploadMutation.error?.message ??
            "Upload failed. Please try again."
          }
        />
      )}
    </div>
  );
}