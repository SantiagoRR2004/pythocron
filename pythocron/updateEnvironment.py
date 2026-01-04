import subprocess
import sys

if __name__ == "__main__":

    # Get outdated packages
    frozenPackages = subprocess.check_output(
        [sys.executable, "-m", "pip", "freeze"],
        text=True,
    )

    packages = [line.split("==")[0] for line in frozenPackages.splitlines() if line]

    if packages:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--force-reinstall",
                "--no-cache-dir",
                *packages,
            ]
        )
