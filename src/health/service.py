from src.health.ollama import check_ollama
from src.health.chroma import check_chroma
from src.health.disk import check_disk


def check_health():
    return {
        "healthy": True,
        "checks": {
            "ollama": check_ollama(),
            "chroma": check_chroma(),
            "disk": check_disk(),
        },
    }