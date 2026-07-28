 
export interface UploadResponse {
  success: boolean;
  message: string;
  data: {
    task_id: string;
    status: string;
    filename: string;
  };
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