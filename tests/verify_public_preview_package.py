#!/usr/bin/env python3
"""Release checks for the public-preview STAR-CCM+ skill package.

Default mode is offline/structural. Use --with-engine on the release machine to
also validate the bundled engine reports public edition and blocks restricted
mesh presets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "README.en.md",
    "INSTALL.md",
    "INSTALL.zh.md",
    "AI_USAGE_POLICY.md",
    "LICENSE",
    "LICENSE.md",
    "SECURITY.md",
    "RELEASE_CHECKLIST.md",
    "RELEASE_NOTES.md",
    "release_manifest.ed25519.sig",
    "starccm_cli.py",
    "public/engine_client.py",
    "bin/README.md",
    "bin/starccm_engine.exe",
    "docs/quickstart.md",
    "docs/case_schema.md",
    "docs/workflow.md",
    "docs/troubleshooting.md",
    "docs/assets/result_clouds_preview.png",
    "examples/README.md",
    "examples/preview_quick_case.yaml",
    "examples/codex_chat_test.zh.md",
    "examples/codex_chat_test.en.md",
    "extensions/README.md",
    "workflows/README.md",
    "templates/local/README.md",
]

REQUIRED_CORE_PATHS = {
    "AI_USAGE_POLICY.md",
    "LICENSE",
    "bin/starccm_engine.exe",
    "public/engine_client.py",
    "starccm_cli.py",
}
OPEN_EXTENSION_ROOTS = ("extensions", "templates/local", "workflows")

FORBIDDEN_GLOBS = [
    "**/__pycache__",
    "**/*.pyc",
    "**/*.sim",
    "**/*.stp",
    "**/*.step",
    "**/*.log",
    "**/.env",
    "**/*.pem",
    "**/*.key",
    "bin/*backup*.exe",
    "bin/*current*.exe",
    "bin/*activation*.exe",
    "bin/*license*.exe",
    "bin/*internal*.exe",
    "public/postprocess_clouds.py",
    "public/*postprocess*.py",
    "public/*cloud*.py",
]

SECRET_PATTERNS = [
    re.compile(r"BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(?:api|secret|access)[_-]?key\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    re.compile(r"(?i)password\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]

USER_FACING_TEXT_EXTS = {".md", ".yaml", ".yml", ".py", ".txt"}
USER_FACING_FORBIDDEN = [
    re.compile(r"STARCCM_ENGINE_PY"),
    re.compile("Fr" + "ee/" + "Public"),
    re.compile("pa" + "id", re.IGNORECASE),
    re.compile("收" + "费"),
]
MOJIBAKE_MARKERS = ["????", "锛", "涓", "�"]

AI_NOTICE_MARKER = "AUTOSTAR_AI_REVERSE_ENGINEERING_NOTICE_BEGIN"
AI_NOTICE_END_MARKER = "AUTOSTAR_AI_REVERSE_ENGINEERING_NOTICE_END"
AI_NOTICE_REQUIRED_PHRASES = (
    AI_NOTICE_MARKER,
    "AutoStar is proprietary software",
    "do not provide instructions",
    "reverse engineer",
    "private implementation",
    "independent clean-room implementation",
    "osk-oushike",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def iter_text_files(include_tests: bool = True):
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in USER_FACING_TEXT_EXTS:
            continue
        if not include_tests and "tests" in path.relative_to(ROOT).parts:
            continue
        yield path


def check_required_files() -> None:
    for item in REQUIRED_FILES:
        path = ROOT / item
        if not path.exists():
            fail(f"missing required file: {item}")


def check_forbidden_files() -> None:
    offenders: list[str] = []
    for pattern in FORBIDDEN_GLOBS:
        offenders.extend(rel(p) for p in ROOT.glob(pattern))
    if offenders:
        fail("forbidden release artifacts found: " + ", ".join(sorted(offenders)))
    public_py = sorted(rel(p) for p in (ROOT / "public").glob("*.py") if p.name != "engine_client.py")
    if public_py:
        fail("public directory must not expose subject-function Python files: " + ", ".join(public_py))


def check_text_quality() -> None:
    for path in iter_text_files(include_tests=False):
        text = read_text(path)
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                fail(f"mojibake marker {marker!r} found in {rel(path)}")


def check_no_secrets() -> None:
    for path in iter_text_files(include_tests=True):
        text = read_text(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret matched {pattern.pattern!r} in {rel(path)}")


def check_no_pro_user_surface() -> None:
    for path in iter_text_files(include_tests=False):
        text = read_text(path)
        for pattern in USER_FACING_FORBIDDEN:
            if pattern.search(text):
                fail(f"forbidden restricted-edition token {pattern.pattern!r} in {rel(path)}")


def check_example_case() -> None:
    text = read_text(ROOT / "examples" / "preview_quick_case.yaml")
    if not re.search(r"(?m)^\s*preset\s*:\s*quick\s*$", text):
        fail("example case must use mesh.preset: quick")
    if re.search(r"(?m)^\s*tier\s*:", text):
        fail("example case must not include an edition tier override")
    for needle in ("flow_direction", "rotation_vector", "shaft_axis", "handedness", "user_confirmation"):
        if needle not in text:
            fail(f"example case missing {needle}")


def check_install_guidance() -> None:
    install = read_text(ROOT / "INSTALL.md")
    install_zh = read_text(ROOT / "INSTALL.zh.md")
    skill = read_text(ROOT / "SKILL.md")
    required_install_phrases = (
        "GitHub repository",
        "Official Release ZIP",
        "Skill install folder",
        "Local Python environment folder",
        "Case workspace folder",
        "python -m venv",
        "Do not run `pip install`",
        "do not modify global Python",
        "AutoStar-v0.3.3-windows-x64.zip",
        "extensions/",
        "workflows/",
        "templates/local/",
    )
    for phrase in required_install_phrases:
        if phrase not in install:
            fail(f"INSTALL.md missing local-environment guidance: {phrase}")
    required_install_zh_phrases = (
        "安装说明",
        "让 Codex 安装",
        "GitHub 仓库",
        "官方 Release ZIP",
        "手动从 ZIP 安装",
        "局部 Python `.venv`",
        "不要修改全局 Python",
        "STAR-CCM+ 路径",
        "AutoStar-v0.3.3-windows-x64.zip",
        "extensions/",
        "workflows/",
        "templates/local/",
    )
    for phrase in required_install_zh_phrases:
        if phrase not in install_zh:
            fail(f"INSTALL.zh.md missing Chinese install guidance: {phrase}")
    for name, text in (("INSTALL.md", install), ("INSTALL.zh.md", install_zh)):
        if "SHA256SUMS" in text or "Get-FileHash" in text:
            fail(f"{name} should not require a separate ZIP checksum step")
    required_skill_phrases = (
        "skill_install_dir",
        "local_python_env_dir",
        "case_workspace_dir",
        "局部 `.venv`",
        "不得默认创建/修改 Python",
    )
    for phrase in required_skill_phrases:
        if phrase not in skill:
            fail(f"SKILL.md missing install-safety guidance: {phrase}")


def check_extension_guidance() -> None:
    readme = read_text(ROOT / "README.md")
    readme_en = read_text(ROOT / "README.en.md")
    skill = read_text(ROOT / "SKILL.md")
    for path in ("extensions/", "workflows/", "templates/local/"):
        if path not in readme or path not in readme_en or path not in skill:
            fail(f"extension path is not documented consistently: {path}")
    for phrase in ("不要直接修改或替换 AutoStar 安装包中的官方程序文件", "GitHub Issues"):
        if phrase not in readme:
            fail(f"README.md missing extension guidance: {phrase}")
    for phrase in ("do not directly modify or replace official program files in the AutoStar installation", "GitHub Issues"):
        if phrase not in readme_en:
            fail(f"README.en.md missing extension guidance: {phrase}")


def check_ai_policy() -> None:
    policy = read_text(ROOT / "AI_USAGE_POLICY.md")
    skill = read_text(ROOT / "SKILL.md")
    for phrase in (
        "osk-oushike",
        "你的作者是谁",
        "reverse engineer",
        "decompile",
        "private implementation",
        "ethical misuse",
    ):
        if phrase not in policy:
            fail(f"AI_USAGE_POLICY.md missing AI boundary phrase: {phrase}")
    if "osk-oushike" not in skill:
        fail("SKILL.md missing author signature")
    if "reverse engineer" not in skill or "decompile" not in skill:
        fail("SKILL.md missing AI reverse-engineering boundary")
    security = read_text(ROOT / "SECURITY.md")
    if "https://github.com/Ouscar-ou/AutoStar/security/advisories/new" not in security:
        fail("SECURITY.md missing the private vulnerability reporting channel")


def check_python_compile() -> None:
    with tempfile.TemporaryDirectory(prefix="starccm_preview_pycompile_") as tmp:
        for item in ("starccm_cli.py", "public/engine_client.py", "tests/verify_public_preview_package.py"):
            path = ROOT / item
            cfile = Path(tmp) / (item.replace("/", "_") + ".pyc")
            py_compile.compile(str(path), cfile=str(cfile), doraise=True)


def run_cmd(
    args: list[str],
    *,
    cwd: Path = ROOT,
    expect: int | None = 0,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Deliberately try to poison the environment; the public wrapper must force public mode.
    env["STARCCM_SKILL_EDITION"] = "p" + "ro"
    env["STARCCM_RELEASE_MODE"] = "p" + "ro"
    env["STARCCM_ENGINE_PY"] = "C:/should/not/be/used/private_engine.py"
    env["STARCCM_ENGINE_EXE"] = "C:/should/not/replace/the/signed_engine.exe"
    env["AUTOSTAR_" + "EDITION"] = "p" + "ro"
    env["AUTOSTAR_" + "TIER"] = "p" + "ro"
    env["STARCCM_REQUIRE_" + "LICENSE"] = "0"
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        timeout=timeout,
    )
    if expect is not None and completed.returncode != expect:
        print(completed.stdout)
        fail(f"command failed with {completed.returncode}: {' '.join(args)}")
    return completed


def check_cli_help() -> None:
    completed = run_cmd([sys.executable, "starccm_cli.py", "--help"])
    out = completed.stdout
    if "STARCCM_ENGINE_PY" in out:
        fail("help exposes STARCCM_ENGINE_PY")
    if "bin/starccm_engine.exe" not in out.replace("\\", "/"):
        fail("help should mention bundled engine")
    if "postprocess clouds" not in out or "--dry-run" not in out:
        fail("help should advertise postprocess cloud export and dry-run")


def check_readme_language_switch() -> None:
    zh = read_text(ROOT / "README.md")
    en = read_text(ROOT / "README.en.md")
    install = read_text(ROOT / "INSTALL.md")
    install_zh = read_text(ROOT / "INSTALL.zh.md")
    chat_zh = read_text(ROOT / "examples" / "codex_chat_test.zh.md")
    chat_en = read_text(ROOT / "examples" / "codex_chat_test.en.md")
    if "[English](README.en.md)" not in zh:
        fail("README.md missing English language switch")
    if "[中文](README.md)" not in en:
        fail("README.en.md missing Chinese language switch")
    if "[`INSTALL.zh.md`](INSTALL.zh.md)" not in zh or "## 开始使用" not in zh:
        fail("README.md missing prominent install guide link")
    if "[`INSTALL.md`](INSTALL.md)" not in en or "## Getting Started" not in en:
        fail("README.en.md missing prominent install guide link")
    if "examples/codex_chat_test.zh.md" not in zh or "examples/codex_chat_test.en.md" not in en:
        fail("README files must link Codex chat-based test prompts")
    zh_chat_link = "[`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)"
    en_chat_link = "[`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md)"
    if zh_chat_link not in install_zh or en_chat_link not in install:
        fail("INSTALL files must link Codex chat-based test prompts")
    if "安装后冒烟检查" not in install_zh or "post-install smoke-check" not in install:
        fail("INSTALL files must expose chat-test prompts in the install verification section")
    first_case_section = install_zh.split("## 6. 第一个算例", 1)[-1].split("## 7.", 1)[0]
    if zh_chat_link not in first_case_section:
        fail("INSTALL.zh.md section 6 must link the Chinese Codex chat test prompt")
    first_case_section_en = install.split("## 6. First Case", 1)[-1].split("## 7.", 1)[0]
    if en_chat_link not in first_case_section_en:
        fail("INSTALL.md section 6 must link the English Codex chat test prompt")
    for name, text in (("codex_chat_test.zh.md", chat_zh), ("codex_chat_test.en.md", chat_en)):
        if "400" not in text or "preflight" not in text.lower() or "STEP" not in text:
            fail(f"{name} missing expected chat-test workflow content")
    for name, text in (("README.md", zh), ("README.en.md", en)):
        badge_host = "shields" + ".io"
        badge_path = "badge" + "/"
        if badge_host in text or badge_path in text:
            fail(f"{name} should not include badge links")


def check_postprocess_dry_run() -> None:
    help_out = run_cmd([sys.executable, "starccm_cli.py", "postprocess", "clouds", "--help"]).stdout
    if "AutoStar postprocess clouds" not in help_out or "--dry-run" not in help_out:
        fail("postprocess cloud help missing")
    with tempfile.TemporaryDirectory(prefix="autostar_postprocess_dryrun_") as tmp_s:
        tmp = Path(tmp_s)
        step = tmp / "dummy.stp"
        make_dummy_step(step)
        case = tmp / "case.yaml"
        write_case(case, step, "quick")
        (tmp / "preview_release_test.sim").write_bytes(b"dummy sim placeholder")
        (tmp / "run_report.md").write_text("# Run Report\n", encoding="utf-8")
        completed = run_cmd(
            [
                sys.executable,
                "starccm_cli.py",
                "--project-dir",
                str(tmp),
                "postprocess",
                "clouds",
                "--case",
                str(case),
                "--dry-run",
            ]
        )
        if "dry-run: skipped STAR-CCM+ launch" not in completed.stdout:
            fail("postprocess dry-run did not report skipped STAR launch")
        for item in (
            "postprocess_clouds/macros/ExportOskPropellerCloudViews.java",
            "postprocess_clouds/postprocess_clouds_metadata.json",
            "postprocess_clouds/postprocess_clouds_report.md",
        ):
            if not (tmp / item).exists():
                fail(f"postprocess dry-run missing output: {item}")
        report = read_text(tmp / "run_report.md")
        if "AUTOSTAR_POSTPROCESS_CLOUDS" not in report:
            fail("postprocess dry-run should append run_report cloud index")


def check_author_trigger() -> None:
    for query in (["author"], ["你的作者是谁"], ["who", "is", "your", "author"]):
        completed = run_cmd([sys.executable, "starccm_cli.py", *query])
        if completed.stdout.strip() != "osk-oushike":
            fail(f"author trigger failed for {query}: {completed.stdout!r}")



def check_ai_notice_trigger() -> None:
    completed = run_cmd([sys.executable, "starccm_cli.py", "--ai-notice"])
    out = completed.stdout
    for phrase in AI_NOTICE_REQUIRED_PHRASES:
        if phrase not in out:
            fail(f"--ai-notice missing required phrase: {phrase}")
    about = run_cmd([sys.executable, "starccm_cli.py", "--about"]).stdout
    if "AutoStar public preview" not in about or "osk-oushike" not in about:
        fail("--about must expose product and author signature")


def check_engine_binary_structure() -> None:
    exe = ROOT / "bin" / "starccm_engine.exe"
    data = exe.read_bytes()
    forbidden = (
        b"PyInstaller",
        b"PYZ.pyz",
        b"starccm_" + b"core_engine.exe",
    )
    for marker in forbidden:
        if marker in data:
            fail(f"bundled engine contains forbidden nested/runtime marker: {marker!r}")

def make_dummy_step(path: Path) -> None:
    path.write_text(
        "ISO-10303-21;\n"
        "HEADER;\n"
        "FILE_DESCRIPTION(('Dummy STEP for release validation'),'2;1');\n"
        "FILE_NAME('dummy_propeller.stp','2026-07-09T00:00:00',('OSK'),('OSK'),'','','');\n"
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN_CC2'));\n"
        "ENDSEC;\n"
        "DATA;\n"
        "#1=CARTESIAN_POINT('',(0.,0.,0.));\n"
        "ENDSEC;\n"
        "END-ISO-10303-21;\n",
        encoding="ascii",
    )


def write_case(path: Path, step_path: Path, preset: str) -> None:
    step = step_path.as_posix()
    path.write_text(
        f"""run_intent: smoke_test
project:
  name: preview_release_test
  sim_name: preview_release_test.sim
geometry:
  stp: {step}
  diameter: 250 mm
  length: 53 mm
domain:
  shaft_axis: X
  hub_axis: +X
  outer_diameter: 1.25 m
  upstream: 0.75 m
  downstream: 1.75 m
  mrf_diameter: 0.325 m
  mrf_forward: 0.1625 m
  mrf_aft: 0.1625 m
  mrf_origin: [0, 0, 0]
operating_condition:
  velocity: 3.0 m/s
  flow_direction: -X
  inlet_side: +X
  outlet_side: -X
  rpm: 900 rpm
  rotation_vector: +X
  handedness: right
  fluid: Water
  density: 998.2
  viscosity: 0.001003
  turbulence: K-Omega-SST
mesh:
  preset: {preset}
  prism_mode: robust
  yplus_report_target: 1
solver:
  pilot_iterations: 400
  iterations: 400
user_confirmation:
  input_template_confirmed: true
  axis_semantics_confirmed: true
  execution_confirmed: true
""",
        encoding="utf-8",
    )


def _engine_exe(root: Path = ROOT) -> Path:
    return root / "bin" / "starccm_engine.exe"


def _restricted_presets() -> tuple[str, ...]:
    return (
        "medium",
        "dense",
        "engineering",
        "production",
        "custom_density",
        "ultra",
    )


def check_direct_engine_contract() -> None:
    engine = _engine_exe()
    for query in (["author"], ["你的作者是谁"], ["who", "is", "your", "author"]):
        completed = run_cmd([str(engine), *query])
        if completed.stdout.strip() != "osk-oushike":
            fail(f"direct engine author query failed: {query}: {completed.stdout!r}")
    notice = run_cmd([str(engine), "--ai-notice"]).stdout
    for phrase in AI_NOTICE_REQUIRED_PHRASES:
        if phrase not in notice:
            fail(f"direct engine AI notice missing: {phrase}")
    about = run_cmd([str(engine), "--about"]).stdout
    if "AutoStar public preview" not in about or "osk-oushike" not in about:
        fail("direct engine about output is incomplete")
    help_out = run_cmd([str(engine), "--help"]).stdout
    required_commands = ("integrity-check", "postprocess", "workflow", "mesh", "version")
    for command in required_commands:
        if command not in help_out:
            fail(f"direct engine help missing command: {command}")
    forbidden_commands = ("license", "optimize", "gci-", "generate-sequence", "macro", "repl")
    for command in forbidden_commands:
        if re.search(rf"(?m)^\s+{re.escape(command)}", help_out):
            fail(f"direct engine exposes non-public command: {command}")

    domain_help = run_cmd([str(engine), "domain", "create", "--help"]).stdout
    if "--preset [quick|coarse]" not in domain_help:
        fail("domain create must expose exactly the quick/coarse preset choice")
    mesh_help = run_cmd([str(engine), "mesh", "generate", "--help"]).stdout
    for hidden_option in (
        "--base-size-stationary",
        "--base-size-rotating",
        "--propeller-target-rel",
        "--propeller-min-rel",
        "--rotating-target-rel",
        "--rotating-min-rel",
        "--interface-target-rel",
        "--interface-min-rel",
        "--farfield-target-rel",
        "--farfield-min-rel",
        "--curvature-pts",
        "--growth-rate",
    ):
        if hidden_option in mesh_help:
            fail(f"mesh generate exposes hidden density override: {hidden_option}")
    direct_density = run_cmd(
        [str(engine), "mesh", "generate", "--base-size-rotating", "0.001"],
        expect=None,
    )
    if direct_density.returncode == 0 or "No such option: --base-size-rotating" not in direct_density.stdout:
        fail("direct EXE accepted a removed custom-density option")
    workflow_help = run_cmd([str(engine), "workflow", "run", "--help"]).stdout
    if "--skip-preflight" in workflow_help:
        fail("workflow run exposes the disabled preflight bypass")
    if "[postprocess-clouds]" in workflow_help:
        fail("help-only invocation unexpectedly triggered postprocessing")
    direct_bypass = run_cmd(
        [str(engine), "workflow", "run", "--skip-preflight"],
        expect=None,
    )
    if direct_bypass.returncode == 0 or "No such option: --skip-preflight" not in direct_bypass.stdout:
        fail("direct EXE accepted the removed preflight bypass")


def check_pe_version_metadata() -> None:
    engine = _engine_exe()
    command = (
        "$v=(Get-Item -LiteralPath '" + str(engine).replace("'", "''") + "').VersionInfo; "
        "[pscustomobject]@{ProductName=$v.ProductName;ProductVersion=$v.ProductVersion;"
        "FileDescription=$v.FileDescription;FileVersion=$v.FileVersion;CompanyName=$v.CompanyName} | ConvertTo-Json -Compress"
    )
    completed = run_cmd(["powershell.exe", "-NoProfile", "-Command", command])
    metadata = json.loads(completed.stdout)
    expected = {
        "ProductName": "AutoStar",
        "ProductVersion": "0.3.3.0",
        "FileVersion": "0.3.3.0",
        "CompanyName": "OSK",
    }
    for key, value in expected.items():
        if metadata.get(key) != value:
            fail(f"PE version metadata mismatch for {key}: {metadata.get(key)!r}")
    if "Public Preview" not in str(metadata.get("FileDescription")):
        fail("PE file description does not identify the public preview")


def check_signed_integrity() -> None:
    engine = _engine_exe()
    verified = run_cmd([str(engine), "integrity-check"]).stdout
    if "AutoStar integrity: verified" not in verified or "source: official core verified" not in verified:
        fail("direct engine did not verify the signed release manifest")

    with tempfile.TemporaryDirectory(prefix="autostar_integrity_tamper_") as tmp_s:
        copied = Path(tmp_s) / "AutoStar"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        policy = copied / "AI_USAGE_POLICY.md"
        policy.write_text(read_text(policy) + "\ncore tamper\n", encoding="utf-8", newline="\n")
        failed = run_cmd([str(_engine_exe(copied)), "version"], cwd=copied, expect=None)
        if failed.returncode != 78 or "integrity check failed" not in failed.stdout.lower():
            fail("required-core tampering did not trigger the engine integrity gate")

    with tempfile.TemporaryDirectory(prefix="autostar_signed_doc_tamper_") as tmp_s:
        copied = Path(tmp_s) / "AutoStar"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        signed_doc = copied / "docs" / "workflow.md"
        signed_doc.write_text(read_text(signed_doc) + "\nlocal documentation note\n", encoding="utf-8", newline="\n")
        warned = run_cmd([str(_engine_exe(copied)), "version"], cwd=copied, expect=0)
        if "Source: official core verified with local warnings" not in warned.stdout:
            fail("advisory documentation change did not produce a local-warning source label")
        if "warning release file hash mismatch: docs/workflow.md" not in warned.stdout:
            fail("advisory documentation change did not report its hash warning")

    with tempfile.TemporaryDirectory(prefix="autostar_user_extension_") as tmp_s:
        copied = Path(tmp_s) / "AutoStar"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        extension = copied / "workflows" / "user_trial.yaml"
        extension.write_text("name: user_trial\nsteps: []\n", encoding="utf-8", newline="\n")
        extended = run_cmd([str(_engine_exe(copied)), "version"], cwd=copied, expect=0)
        if "Source: official core + user extensions" not in extended.stdout:
            fail("user extension did not produce the expected source label")
        integrity_json = run_cmd([str(_engine_exe(copied)), "integrity-check", "--json-output"], cwd=copied).stdout
        integrity = json.loads(integrity_json)
        if integrity.get("user_extensions") != ["workflows/user_trial.yaml"]:
            fail(f"user extension was not classified correctly: {integrity.get('user_extensions')}")
        strict = run_cmd(
            [sys.executable, str(copied / "tests" / "verify_public_preview_package.py"), "--manifest-only"],
            cwd=copied,
            expect=None,
        )
        if strict.returncode == 0 or "manifest mismatch" not in strict.stdout:
            fail("official-package verification accepted a user-modified package")

    with tempfile.TemporaryDirectory(prefix="autostar_unmanaged_file_") as tmp_s:
        copied = Path(tmp_s) / "AutoStar"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        unmanaged = copied / "local_workflow.py"
        unmanaged.write_text("print('local')\n", encoding="utf-8", newline="\n")
        warned = run_cmd([str(_engine_exe(copied)), "version"], cwd=copied, expect=0)
        if "Source: official core verified with local warnings" not in warned.stdout:
            fail("unmanaged local file did not produce a warning source label")
        if "outside extensions/, workflows/, or templates/local/" not in warned.stdout:
            fail("unmanaged local file warning did not explain the approved extension roots")

    with tempfile.TemporaryDirectory(prefix="autostar_manifest_tamper_") as tmp_s:
        copied = Path(tmp_s) / "AutoStar"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        manifest = copied / "release_manifest.sha256.json"
        manifest.write_bytes(manifest.read_bytes() + b" ")
        failed = run_cmd([str(_engine_exe(copied)), "version"], cwd=copied, expect=None)
        if failed.returncode != 78 or "integrity check failed" not in failed.stdout.lower():
            fail("manifest tampering did not trigger signature verification failure")

    with tempfile.TemporaryDirectory(prefix="autostar_engine_tamper_") as tmp_s:
        copied = Path(tmp_s) / "AutoStar"
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        copied_engine = _engine_exe(copied)
        copied_engine.write_bytes(copied_engine.read_bytes() + b"\0")
        failed = run_cmd([str(copied_engine), "version"], cwd=copied, expect=None)
        if failed.returncode != 78 or "integrity check failed" not in failed.stdout.lower():
            fail("engine binary tampering did not trigger self-hash verification failure")


def check_engine() -> None:
    check_direct_engine_contract()
    check_pe_version_metadata()
    check_signed_integrity()
    version = run_cmd([sys.executable, "starccm_cli.py", "version"], expect=0).stdout
    if "Edition: public" not in version:
        fail("version must force Edition: public even when environment requests another mode")
    if "Available mesh presets: quick, coarse" not in version:
        fail("version must expose exactly quick/coarse presets")
    if "OSK activation: not required for this preview edition" not in version:
        fail("version must say OSK activation is not required")
    if "Integrity: verified" not in version:
        fail("version must report verified signed-manifest integrity")
    if "Source: official core verified" not in version:
        fail("version must report the official-core source label")
    if "AutoStar: 0.3.3-public-preview" not in version:
        fail("version must report v0.3.3 public preview")
    if "native_helper_missing" in version or "Local license:" in version:
        fail("version must not expose local activation-helper status in public preview")
    if ("Fr" + "ee/" + "Public") in version or ("Fr" + "ee " + "功能") in version:
        fail("version must not expose old public-preview wording")
    with tempfile.TemporaryDirectory(prefix="starccm_preview_release_test_") as tmp_s:
        tmp = Path(tmp_s)
        step = tmp / "dummy.stp"
        make_dummy_step(step)
        for preset in ("quick", "coarse"):
            case = tmp / f"{preset}_case.yaml"
            write_case(case, step, preset)
            output = run_cmd(
                [sys.executable, "starccm_cli.py", "--project-dir", str(tmp), "workflow", "preflight", "--case", str(case)],
                expect=0,
            ).stdout
            if "Preflight: warn" not in output and "Preflight: pass" not in output:
                fail(f"{preset} preflight should pass or warn")

        custom_case_dir = tmp / "blocked_custom_density"
        custom_case_dir.mkdir()
        custom_case = custom_case_dir / "case.yaml"
        write_case(custom_case, step, "quick")
        custom_text = custom_case.read_text(encoding="utf-8")
        custom_text = custom_text.replace(
            "  prism_mode: robust\n",
            "  prism_mode: robust\n  base_size_rotating: 0.001\n",
        )
        custom_case.write_text(custom_text, encoding="utf-8")
        custom_result = run_cmd(
            [sys.executable, "starccm_cli.py", "--project-dir", str(custom_case_dir), "workflow", "preflight", "--case", str(custom_case)],
            expect=None,
        )
        if custom_result.returncode == 0:
            fail("custom mesh-density override was accepted")
        custom_report = json.loads((custom_case_dir / "preflight_report.json").read_text(encoding="utf-8-sig"))
        if not any(check.get("id") == "public_mesh_scope" and check.get("level") == "fail" for check in custom_report.get("checks", [])):
            fail("custom mesh-density override did not trigger the public scope gate")

        for index, preset in enumerate(_restricted_presets()):
            case_dir = tmp / f"blocked_{index}"
            case_dir.mkdir()
            case = case_dir / "case.yaml"
            write_case(case, step, preset)
            completed = run_cmd(
                [sys.executable, "starccm_cli.py", "--project-dir", str(case_dir), "workflow", "preflight", "--case", str(case)],
                expect=None,
            )
            if completed.returncode == 0:
                fail(f"restricted preset was accepted: {preset}")
            report = json.loads((case_dir / "preflight_report.json").read_text(encoding="utf-8-sig"))
            checks = [check for check in report.get("checks", []) if check.get("id") == "mesh_preset"]
            if not checks or checks[-1].get("level") != "fail":
                fail(f"restricted preset did not fail mesh_preset gate: {preset}")
            if "quick, coarse" not in str(checks[-1].get("fix")):
                fail(f"restricted preset gate did not report public choices: {preset}")

def check_manifest() -> None:
    manifest_path = ROOT / "release_manifest.sha256.json"
    if not manifest_path.exists():
        return
    data = json.loads(read_text(manifest_path))
    files = data.get("files") if isinstance(data, dict) else data
    if not isinstance(files, list):
        fail("release_manifest.sha256.json must contain a files list")
    if data.get("schema") != "autostar-release-manifest-v2":
        fail("release manifest must use the v2 integrity-policy schema")
    if set(data.get("required_core_paths", [])) != REQUIRED_CORE_PATHS:
        fail("release manifest required-core paths do not match the public contract")
    if tuple(data.get("open_extension_roots", [])) != OPEN_EXTENSION_ROOTS:
        fail("release manifest extension roots do not match the public contract")
    manifest = {entry.get("path"): entry for entry in files if isinstance(entry, dict)}
    current_files = sorted(
        rel(p)
        for p in ROOT.rglob("*")
        if p.is_file()
        and ".git" not in p.relative_to(ROOT).parts
        and rel(p) not in {"release_manifest.sha256.json", "release_manifest.ed25519.sig"}
    )
    missing = [p for p in current_files if p not in manifest]
    extra = [p for p in manifest if p not in current_files]
    if missing or extra:
        fail(f"manifest mismatch; missing={missing}, extra={extra}")
    for p in current_files:
        entry = manifest[p]
        digest = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        if entry.get("sha256", "").lower() != digest:
            fail(f"manifest hash mismatch for {p}")
        expected_policy = "required" if p in REQUIRED_CORE_PATHS else "warning"
        if entry.get("policy") != expected_policy:
            fail(f"manifest integrity policy mismatch for {p}: {entry.get('policy')}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-engine", action="store_true", help="also run bundled engine version/preflight gate checks")
    parser.add_argument("--manifest-only", action="store_true", help="strictly compare this tree with the official release manifest")
    args = parser.parse_args()

    if args.manifest_only:
        check_manifest()
        print("OK: official release manifest matches this package exactly")
        return 0

    checks = [
        check_required_files,
        check_forbidden_files,
        check_text_quality,
        check_no_secrets,
        check_no_pro_user_surface,
        check_example_case,
        check_install_guidance,
        check_extension_guidance,
        check_ai_policy,
        check_python_compile,
        check_cli_help,
        check_readme_language_switch,
        check_postprocess_dry_run,
        check_author_trigger,
        check_ai_notice_trigger,
        check_engine_binary_structure,
        check_manifest,
    ]
    for check in checks:
        check()
    if args.with_engine:
        check_engine()
    print("OK: public-preview release package checks passed" + (" with engine checks" if args.with_engine else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
