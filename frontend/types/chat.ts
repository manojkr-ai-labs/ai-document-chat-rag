export interface Citation {
  source: string;
  page: string;
} 

export interface ChatData {
  answer: string;
  citations: Citation[];
} 
export interface ChatRequest {
  question: string;
  conversation_id?: string;
}

export interface ChatAnswer {
  answer: string;
}

// export interface ChatResponse {
//   success: boolean;
//   message: string;
//   data: ChatAnswer;
// }
export interface ChatResponse {
  success: boolean;
  message: string;
  data: {
    conversation_id: string;
    title?: string;
    answer: string;
    citations: Citation[];
  };
}
export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  citations?: Citation[];
}