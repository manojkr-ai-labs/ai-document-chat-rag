"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

import  UploadDropzone  from "./UploadDropzone";
import  UploadProgress  from "./UploadProgress";
import UploadResult  from "./UploadResult";

import { useUpload } from "@/hooks/useUpload";
import { useTaskStatus } from "@/hooks/useTaskStatus";

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);

  const uploadMutation = useUpload();

  const { data: taskStatus } = useTaskStatus(taskId);

  const handleUpload = async () => {
    if (!file) return;

    try {
      const response = await uploadMutation.mutateAsync(file);

      setTaskId(response.data.task_id);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div className="space-y-6">
      <UploadDropzone
        file={file}
        onFileSelect={setFile}
      />

      <Button
        className="w-full"
        disabled={!file || uploadMutation.isPending}
        onClick={handleUpload}
      >
        {uploadMutation.isPending
          ? "Uploading..."
          : "Upload PDF"}
      </Button>

      {taskId && (
        <UploadProgress
          status={taskStatus?.data.status ?? "processing"}
        />
      )}

      {uploadMutation.isSuccess && (
        <UploadResult
          success={true}
          message={
            taskStatus?.data.status === "completed"
              ? "Document indexed successfully."
              : "Upload started successfully."
          }
        />
      )}

      {uploadMutation.isError && (
        <UploadResult
          success={false}
          message={
            uploadMutation.error?.message ??
            "Upload failed."
          }
        />
      )}
    </div>
  );
}