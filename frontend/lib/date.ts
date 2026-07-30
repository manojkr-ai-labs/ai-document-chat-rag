export function formatMessageTime(
    value: Date | string
) {
    return new Date(value).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    });
}