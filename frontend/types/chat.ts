export interface ChatRequest {
  question: string;
}

export interface ChatAnswer {
  answer: string;
}

export interface ChatResponse {
  success: boolean;
  message: string;
  data: ChatAnswer;
}