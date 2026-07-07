from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT, check=True)


def main() -> int:
    if not HOME.exists():
        raise FileNotFoundError("Canonical enterprise homepage is missing: index.html")

    enterprise_home = HOME.read_text(encoding="utf-8")
    run("build_site.py")
    HOME.write_text(enterprise_home, encoding="utf-8")
    run("apply_enterprise_upgrade.py")
    print("Enterprise site build completed with the canonical homepage restored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
