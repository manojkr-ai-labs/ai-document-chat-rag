"use client";

import { useQuery } from "@tanstack/react-query";

import { getTaskStatus } from "@/services/upload";

import type { UploadStatusResponse } from "@/types/upload";

export function useTaskStatus(taskId: string | null) {
  return useQuery<UploadStatusResponse, Error>({
    queryKey: ["task-status", taskId],

    queryFn: () => getTaskStatus(taskId!),

    enabled: !!taskId,

    refetchInterval: (query) => {
      if (query.state.data?.data.status === "completed") {
        return false;
      }

      return 2000;
    },
  });
}