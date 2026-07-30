import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from "lucide-react";

interface MessageActionsProps {
  onCopy: () => void;
  onRegenerate: () => void;
  onLike: () => void;
  onDislike: () => void;
}

export default function MessageActions({
  onCopy,
  onRegenerate,
  onLike,
  onDislike,
}: MessageActionsProps) {
  return (
    <div   
     className="mt-3
    flex
    items-center
    gap-2
    justify-end
    opacity-0
    transition-all
    duration-200
    group-hover:opacity-100
   
  "
  
  >
      <button
        onClick={onCopy}
        className=" rounded-md
    p-2
    text-slate-500
    transition-colors
    hover:bg-slate-100
    hover:text-slate-900"
      >
        <Copy size={16} />
      </button>

      <button
        onClick={onRegenerate}
        className=" rounded-md
    p-2
    text-slate-500
    transition-colors
    hover:bg-slate-100
    hover:text-slate-900"
      >
        <RotateCcw size={16} />
      </button>

      <button
        onClick={onLike}
        className=" rounded-md
    p-2
    text-slate-500
    transition-colors
    hover:bg-slate-100
    hover:text-slate-900"
      >
        <ThumbsUp size={16} />
      </button>

      <button
        onClick={onDislike}
        className=" rounded-md
    p-2
    text-slate-500
    transition-colors
    hover:bg-slate-100
    hover:text-slate-900"
      >
        <ThumbsDown size={16} />
      </button>
    </div>
  );
}