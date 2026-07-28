import {api} from "./api";

import type { IndexResponse } from "@/types/index";

export async function indexDocuments() {
  const response = await api.post<IndexResponse>("/index");

  return response.data;
}