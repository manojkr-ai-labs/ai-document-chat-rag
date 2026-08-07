import { api } from "./api";

export async function getConversations() {
  const response = await api.get("/conversations");
  return response.data;
}

export async function createConversation(title = "New Chat") {
  const response = await api.post("/conversations", {
    title,
  });

  return response.data;
}

export async function renameConversation(
  id: string,
  title: string
) {
  const response = await api.patch(
    `/conversations/${id}`,
    {
      title,
    }
  );

  return response.data;
}

export async function getConversation(id: string) {
  const response = await api.get(
    `/conversations/${id}`
  );

  return response.data;
}

export async function deleteConversation(id: string) {
  const response = await api.delete(
    `/conversations/${id}`
  );

  return response.data;
}