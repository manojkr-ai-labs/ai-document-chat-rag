import {api} from "./api";

import type {
  UploadResponse,
  UploadStatusResponse,
} from "@/types/upload";

export async function uploadPdf(file: File) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post<UploadResponse>(
    "/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function getUploadStatus(taskId: string) {
  const response = await api.get<UploadStatusResponse>(
    `/tasks/${taskId}`
  );

  return response.data;
}