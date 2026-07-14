"""Public engine client for the STAR-CCM+ skill wrapper.

This module intentionally contains only process-launching glue for the bundled
public-preview engine.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def _wrapper_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_engine_command() -> list[str]:
    """Resolve the bundled public-preview engine command."""
    bin_dir = _wrapper_root() / "bin"
    bundled = bin_dir / "starccm_engine.exe"
    if bundled.exists():
        return [str(bundled)]

    raise RuntimeError("Bundled signed engine not found: bin/starccm_engine.exe")


def _engine_env() -> dict[str, str]:
    env = os.environ.copy()
    env["STARCCM_SKILL_EDITION"] = "public"
    env["STARCCM_RELEASE_MODE"] = "public"
    env.pop("STARCCM_" + "ENGINE_PY", None)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    root = _wrapper_root()
    env.setdefault("OSK_SKILL_ROOT", str(root))
    return env


def run_engine(args: list[str]) -> int:
    cmd = [*resolve_engine_command(), *args]
    env = _engine_env()
    completed = subprocess.run(cmd, env=env)
    return int(completed.returncode)


def run_engine_captured(args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [*resolve_engine_command(), *args]
    return subprocess.run(
        cmd,
        env=_engine_env(),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
