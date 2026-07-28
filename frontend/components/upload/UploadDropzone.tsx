"use client";

import { UploadCloud } from "lucide-react";

interface UploadDropzoneProps {
  file: File | null;
  onFileSelect: (file: File | null) => void;
}

export default function UploadDropzone({
  file,
  onFileSelect,
}: UploadDropzoneProps) {
  const handleFile = (selectedFile: File) => {
    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    const maxSize = 20 * 1024 * 1024;

    if (selectedFile.size > maxSize) {
      alert("File size must be less than 20 MB.");
      return;
    }

    onFileSelect(selectedFile);
  };

  const handleDrop = (
    e: React.DragEvent<HTMLDivElement>
  ) => {
    e.preventDefault();

    if (e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (e.target.files?.length) {
      handleFile(e.target.files[0]);
    }
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      className="rounded-xl border-2 border-dashed border-slate-300 bg-white p-10 text-center transition hover:border-blue-500"
    >
      <UploadCloud className="mx-auto h-16 w-16 text-blue-600" />

      <h2 className="mt-4 text-xl font-semibold">
        Drag & Drop PDF Here
      </h2>

      <p className="mt-2 text-sm text-gray-500">
        or click below to browse your files
      </p>

      <input
        type="file"
        accept=".pdf"
        onChange={handleChange}
        className="mt-6 block w-full text-sm"
      />

      {file && (
        <p className="mt-4 font-medium text-green-600">
          Selected: {file.name}
        </p>
      )}

      <p className="mt-4 text-xs text-gray-400">
        PDF only • Maximum file size: 20 MB
      </p>
    </div>
  );
}