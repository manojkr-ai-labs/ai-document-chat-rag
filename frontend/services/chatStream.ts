const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export async function streamChat(
  question: string,
  conversation_id: string | null,
  onChunk: (chunk: string) => void,
  signal?: AbortSignal,
): Promise<string | null> {

  const response = await fetch(
    `${API_URL}/chat/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        conversation_id,
      }),
      signal,
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to stream response: ${response.status}`
    );
  }

  if (!response.body) {
    throw new Error(
      "ReadableStream not supported"
    );
  }

  // Capture BEFORE consuming the stream
  const conversationId =
    response.headers.get("X-Conversation-ID");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { value, done } =
        await reader.read();

      if (done) {
          console.log("STREAM COMPLETE");
        break;
      }

      const chunk = decoder.decode(value, {
        stream: true,
      });
      console.log("STREAM CHUNK:", JSON.stringify(chunk));


      if (chunk) {
        onChunk(chunk);
        
      }
    }

    // Flush decoder
    const finalChunk = decoder.decode();

    if (finalChunk) {
      onChunk(finalChunk);
    }
  } finally {
    reader.releaseLock();
  }

  return conversationId;
}