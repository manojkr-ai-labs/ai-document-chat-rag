interface StreamingMessageProps {
  content: string;
}

export default function StreamingMessage({
  content,
}: StreamingMessageProps) {
  return (
    <div className="whitespace-pre-wrap break-words leading-7 text-sm">
      {content}
      <span className="ml-1 inline-block animate-pulse font-bold select-none">
        ▌
      </span>
    </div>
  );
}