"""AutoStar public CLI wrapper.

The wrapper is intentionally thin: it forwards user-facing CLI commands to the
bundled, signed-manifest-verified engine binary.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Prefer UTF-8 output even on Windows consoles using a legacy code page.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Keep installed preview folders clean: users commonly run `version` before
# release verification, so the wrapper must not create public/__pycache__.
sys.dont_write_bytecode = True

# Public-preview release must stay in public mode even if the caller has
# development environment variables in their shell.
os.environ["STARCCM_SKILL_EDITION"] = "public"
os.environ["STARCCM_RELEASE_MODE"] = "public"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from public.engine_client import run_engine  # noqa: E402

HELP = """AutoStar public wrapper

Usage:
  python starccm_cli.py [ENGINE_ARGS...]

Examples:
  python starccm_cli.py version
  python starccm_cli.py --project-dir C:\\runs\\case1 workflow preflight --case case.yaml
  python starccm_cli.py --project-dir C:\\runs\\case1 workflow run --case case.yaml
  python starccm_cli.py --project-dir C:\\runs\\case1 postprocess clouds --case case.yaml
  python starccm_cli.py --project-dir C:\\runs\\case1 postprocess clouds --case case.yaml --dry-run
  python starccm_cli.py --project-dir C:\\runs\\case1 workflow run --case case.yaml --postprocess-clouds
  python starccm_cli.py --ai-notice
  python starccm_cli.py --about

Engine resolution:
  bin/starccm_engine.exe next to this wrapper (signed package engine only)
"""
def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print(HELP)
        return 0
    try:
        return run_engine(argv)
    except Exception as exc:
        print(f"Engine unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
