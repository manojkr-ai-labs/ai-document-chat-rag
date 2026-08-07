const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function streamChat(
  question: string,
  conversation_id: string | null,
  onChunk: (chunk: string) => void,
  signal?: AbortSignal
) {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
       question,
       conversation_id,
    }),
    signal
  });

  if (!response.ok) {
    throw new Error("Failed to stream response");
  }

  if (!response.body) {
    throw new Error("ReadableStream not supported");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value, {
      stream: true,
    });

    onChunk(chunk);
  }
}