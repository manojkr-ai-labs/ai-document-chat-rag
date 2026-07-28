"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

import UploadDropzone from "./UploadDropzone";
import UploadProgress from "./UploadProgress";
import UploadResult from "./UploadResult";

export default function UploadForm() {
  const [file, setFile] = useState<File | null>(null);

  const [progress, setProgress] = useState(0);

  const [success, setSuccess] = useState(false);

  const [message, setMessage] = useState("");

  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF.");
      setSuccess(false);
      return;
    }

    setUploading(true);

    setProgress(0);

    const timer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(timer);

          setUploading(false);

          setSuccess(true);

          setMessage(`${file.name} uploaded successfully.`);

          return 100;
        }

        return prev + 10;
      });
    }, 200);
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
        disabled={uploading}
      >
        {uploading ? "Uploading..." : "Upload PDF"}
      </Button>

      {uploading && (
        <UploadProgress progress={progress} />
      )}

      {message && (
        <UploadResult
          success={success}
          message={message}
        />
      )}
    </div>
  );
}