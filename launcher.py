from __future__ import annotations

import os
from pathlib import Path
import sys


def main() -> None:
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_path = bundle_root / "app.py"
    if not app_path.is_file():
        raise FileNotFoundError(f"Arquivo da aplicação não encontrado: {app_path}")

    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", "127.0.0.1")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "false")
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    sys.argv = ["streamlit", "run", str(app_path)]

    from streamlit.web.cli import main as streamlit_main

    streamlit_main()


if __name__ == "__main__":
    main()
