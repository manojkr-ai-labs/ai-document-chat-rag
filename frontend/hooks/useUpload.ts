"use client";

import { useMutation } from "@tanstack/react-query";

import { uploadPdf } from "@/services/upload";

export function useUpload() {
  return useMutation({
    mutationFn: uploadPdf,

    onSuccess: (data) => {
      console.log("Upload successful:", data);
    },

    onError: (error) => {
      console.error("Upload failed:", error);
    },
  });
}