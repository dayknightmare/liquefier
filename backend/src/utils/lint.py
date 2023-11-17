from src.utils.pretty_print import Colors, color_print
from src.utils.envs import settings
import subprocess


def run_lint():
    if not settings.debug:
        return

    subprocess.Popen(
        ["black", "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).wait()

    p = subprocess.Popen(
        ["ruff", "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while p.poll() is None:
        assert p.stdout is not None

        line = p.stdout.readline().decode()
        color_print(line, Colors.RED)
