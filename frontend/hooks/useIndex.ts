"use client";

import { useMutation } from "@tanstack/react-query";

import { indexDocuments } from "@/services/index";

import type { IndexResponse } from "@/types/index";

export function useIndex() {
  return useMutation<
    IndexResponse,
    Error,
    void
  >({
    mutationFn: indexDocuments,

    onSuccess: (data) => {
      console.log("Index completed:", data);
    },

    onError: (error) => {
      console.error("Index failed:", error);
    },
  });
}