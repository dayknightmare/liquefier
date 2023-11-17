import subprocess
import shutil


path = "config/hooks/pre-commit"
dest = ".git/hooks"

shutil.copy2(path, dest)

subprocess.Popen(
    ["chmod", "+x", f"{dest}/pre-commit"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
).wait()
