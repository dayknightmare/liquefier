from src.utils.envs import settings
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def color_print(message, color: str = Colors.YELLOW):
    print(color + str(message) + Colors.ENDC)


def log_print(message):
    if not settings.debug:
        return

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{now_str}] -", str(message))


def log_color_print(message, color: str = Colors.YELLOW):
    if not settings.debug:
        return

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    print(color + f"[{now_str}] -", str(message) + Colors.ENDC)
