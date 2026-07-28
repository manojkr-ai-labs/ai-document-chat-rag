export interface UploadResponse {
  success: boolean;
  message: string;
  task_id: string;
}

export interface UploadStatus {
  status: string;
  progress: number;
}

export interface UploadStatusResponse {
  success: boolean;
  message: string;
  data: UploadStatus;
}

export interface UploadRequest {
  file: File;
}