# Installation Guide

[中文安装说明](INSTALL.zh.md) | English

This guide is for the AutoStar public preview.

AutoStar does not include Siemens STAR-CCM+ and does not provide a STAR-CCM+ license. You must use your own properly licensed local STAR-CCM+ installation.

## 1. Requirements

- Windows 10/11.
- Python 3.10+ available from PowerShell.
- Local Siemens STAR-CCM+ installation. This preview has been validated on STAR-CCM+ 18.04.008.
- A valid STAR-CCM+ license from Siemens or your organization.
- A STEP/STP propeller geometry and confirmed physical operating conditions.

## 2. Recommended Install With Codex

This is the recommended path for most Codex users, but Codex must ask before writing files or creating environments.

Before installation, confirm one package source and three local paths.

The package source can be one of:

1. GitHub repository URL: for example `https://github.com/Ouscar-ou/AutoStar`
2. Downloaded release ZIP: for example `C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.2-windows-x64.zip`
3. Already extracted or cloned local folder: for example `C:/Users/<your-user-name>/Downloads/AutoStar`

If Codex can access GitHub, putting the GitHub URL in the prompt is the easiest path. If network access, repository visibility, or authentication is unreliable, download the official release ZIP first and give Codex the local ZIP path. Do not paste GitHub tokens, passwords, or private credentials into the prompt.

The three local paths are:

1. Skill install folder: where AutoStar will be copied.
2. Local Python environment folder: optional, recommended as an isolated `.venv`.
3. Case workspace folder: where CFD cases and outputs will be created.

Recommended layout after confirmation:

```text
Skill install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Local Python environment folder:
C:/Users/<your-user-name>/Documents/autostar_env/.venv

Case workspace folder:
C:/Users/<your-user-name>/Documents/autostar_runs
```

Prompt Codex with wording like:

```text
Install the AutoStar preview from https://github.com/Ouscar-ou/AutoStar. Before installing, ask me where to place the skill, whether to create a local .venv, and where to put case outputs. Do not modify global Python, PATH, or the STAR-CCM+ installation directory. Run version after installation.
```

If you already downloaded the ZIP, use wording like:

```text
Install AutoStar from this local ZIP: C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.2-windows-x64.zip. Before installing, ask me where to place the skill, whether to create a local .venv, and where to put case outputs. Do not modify global Python, PATH, or the STAR-CCM+ installation directory. Verify SHA256SUMS.txt, then run integrity-check and version after installation.
```

If you approve a local `.venv`, create it in the selected folder:

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe C:/Users/<your-user-name>/.codex/skills/autostar/starccm_cli.py version
```

No package installation is normally required for this preview. Do not run `pip install`, do not upgrade pip, and do not modify PATH unless the user explicitly asks for it.

Important: Codex should not install Python, create a virtual environment, modify PATH, set `STARCCM_BAT`, set `STARCCM_EXE`, or change the STAR-CCM+ installation directory unless the user explicitly approves the action and target path.

## 3. Manual Install From ZIP

1. Download both `AutoStar-v0.3.2-windows-x64.zip` and `SHA256SUMS.txt` from the same official GitHub Release.
2. Before extracting or running anything, verify the ZIP hash in PowerShell:

```powershell
$downloadDir = "C:/Users/<your-user-name>/Downloads"
$zip = Join-Path $downloadDir "AutoStar-v0.3.2-windows-x64.zip"
$sums = Join-Path $downloadDir "SHA256SUMS.txt"
$expected = ((Get-Content -LiteralPath $sums -Raw).Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries))[0].ToLowerInvariant()
$actual = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "AutoStar ZIP SHA256 mismatch: $actual != $expected" }
"AutoStar ZIP SHA256 verified: $actual"
```

3. Extract the verified ZIP to a temporary folder.
4. Choose your install folder. Recommended:

```text
C:/Users/<your-user-name>/.codex/skills/autostar
```

5. Copy the extracted `AutoStar` package contents into that folder.
6. Optional but recommended: create a local Python `.venv` in a user-selected folder, not in global Python:

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
```

7. Open PowerShell in the AutoStar install folder and run:

```powershell
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py integrity-check
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py version
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./tests/verify_public_preview_package.py
```

If you want to continue with a chat-based Codex test case, open [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md) after installation verification passes.

Start by copying the post-install smoke-check prompt into Codex. If you have a STEP/STP file, continue with the quick preflight and 400-step pilot prompts.

You should see:

- `Edition: public`
- `Available mesh presets: quick, coarse`
- `OSK activation: not required for this preview edition`
- A STAR-CCM+ executable path and compatible version message.


After these checks pass, the file-level installation is complete. Open a new Codex task/window, or restart Codex, so Codex can rescan the `.codex/skills` directory. Then you can ask Codex to `use AutoStar/autostar for a propeller CFD workflow check`, and Codex should load this skill.

Make sure the install folder layout is:

```text
C:/Users/<your-user-name>/.codex/skills/autostar/SKILL.md
```

Do not accidentally create a nested layout like:

```text
C:/Users/<your-user-name>/.codex/skills/autostar/AutoStar/SKILL.md
```
## 4. First-Run Environment Check

Before creating or running any CFD case, always run from the selected AutoStar folder:

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

`integrity-check` must report `AutoStar integrity: verified`. If the signature, executable, or a critical skill file has changed, AutoStar stops; reinstall from the official release instead of bypassing the check.

For local development, do not edit the required core files. Put custom scripts in `extensions/`, workflow definitions in `workflows/`, and local templates in `templates/local/`. Added extension files change the source label to `official core + user extensions` but do not stop normal execution. The release-package verification script remains intentionally strict and may report a package mismatch after local extensions are added.

If you are on the release/test machine and want to validate the bundled engine too:

```powershell
python ./tests/verify_public_preview_package.py --with-engine
```

Do not start meshing or solving until STAR-CCM+ is detected correctly.

If you want to test AutoStar entirely through Codex chat, open [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md).

It contains copy-and-paste prompts for post-install smoke check, quick preflight with your own STEP, and a confirmed 400-step pilot.

## 5. STAR-CCM+ Path

AutoStar tries to locate STAR-CCM+ automatically. If STAR-CCM+ is not found, first confirm where STAR-CCM+ is installed, then set one of these variables only for the current PowerShell session:

```powershell
$env:STARCCM_BAT="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
```

or:

```powershell
$env:STARCCM_EXE="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
```

Then rerun:

```powershell
python ./starccm_cli.py version
```

Do not write these variables permanently unless you understand the impact and want that behavior.

## 6. First Case

If you prefer to run the first case through Codex chat, open [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md) first.

That file provides English copy-and-paste prompts for the post-install smoke check, quick preflight with your own STEP/STP file, and the confirmed 400-step pilot. The command-based flow below is useful when you want to inspect the case file and run steps manually.

Copy the example case:

```powershell
mkdir C:/runs/case1
copy ./examples/preview_quick_case.yaml C:/runs/case1/case.yaml
```

Edit `C:/runs/case1/case.yaml` and confirm:

- STEP/STP path.
- Diameter `D` and axial length `L`.
- Flow direction and inlet/outlet side.
- Rotation-vector direction and rpm.
- Mesh preset: `quick` or `coarse` only.

Then run preflight:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow preflight --case C:/runs/case1/case.yaml
```

Only after preflight is acceptable and the user confirms this run, start the workflow:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow run --case C:/runs/case1/case.yaml
```

## 7. Upgrade

1. Close running STAR-CCM+ jobs that use this package.
2. Back up your case folders if needed; normal case workspaces should already be outside the skill installation.
3. Confirm the old install folder, then archive the entire folder instead of deleting it.
4. Pay special attention to user-created files under `extensions/`, `workflows/`, and `templates/local/`.
5. Verify the new Release ZIP against its `SHA256SUMS.txt`, then install the new official package into a clean folder.
6. Copy only your user-created extension/workflow/template files from the archive into the corresponding new directories. Do not overwrite the new official `README.md` files or any required core file.
7. Run `python ./starccm_cli.py integrity-check` and `python ./starccm_cli.py version`.
8. An unchanged installation reports `official core verified`; an installation with restored extensions reports `official core + user extensions`.
9. Keep the archived old installation until the new version and extensions have been verified.

## 8. Uninstall

Delete the selected install folder, for example:

```text
C:/Users/<your-user-name>/.codex/skills/autostar
```

This does not remove STAR-CCM+ or your case folders.

## 9. Troubleshooting

- Python not found: first decide whether to install Python or use an existing Python. Prefer a local `.venv`; do not modify global PATH unless explicitly approved.
- STAR-CCM+ not found: confirm the STAR-CCM+ install path, then set `STARCCM_BAT` or `STARCCM_EXE` for the current session.
- STAR license failure: check your Siemens STAR-CCM+ license; this preview does not provide a STAR license.
- Antivirus blocks `starccm_engine.exe`: restore or allow the official release folder, then verify the SHA256 manifest.
- Preflight says only quick/coarse are available: this is expected in the current preview.
- Axis or direction is unclear: do not run; confirm `shaft_axis`, `flow_direction`, and `rotation_vector` separately.

See `docs/troubleshooting.md` for more details.
