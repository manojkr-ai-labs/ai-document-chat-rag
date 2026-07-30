import { useRef } from "react";

export default function useAutoResizeTextarea() {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

 const resizeTextarea = () => {
  const textarea = textareaRef.current;

  if (!textarea) return;

  textarea.style.height = "0px";
  textarea.style.height = `${Math.min(
    textarea.scrollHeight,
    192
  )}px`;

  textarea.style.overflowY =
    textarea.scrollHeight > 192 ? "auto" : "hidden";
};

  const resetTextarea = () => {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "auto";
  };

  return {
    textareaRef,
    resizeTextarea,
    resetTextarea,
  };
}