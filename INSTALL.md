# AutoStar Installation Guide

English | [中文安装说明](INSTALL.zh.md)

This guide installs the AutoStar preview. AutoStar does not include Siemens STAR-CCM+ software or licensing. Before use, confirm that a properly licensed STAR-CCM+ installation runs on the local machine.

## 1. Requirements

- Windows 10/11.
- Python 3.10+ available from PowerShell.
- A local Siemens STAR-CCM+ installation; the current version has been validated with STAR-CCM+ `18.04.008-R8`.
- A separate workspace for CFD cases and outputs.

## 2. Recommended: Install With Codex

Before installation, choose the package source and confirm three local paths.

The package source can be:

1. GitHub repository: `https://github.com/Ouscar-ou/AutoStar`
2. Official Release ZIP, for example `C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.3-windows-x64.zip`
3. An extracted or cloned local folder.

The user should confirm:

1. Skill install folder: where AutoStar will be installed.
2. Local Python environment folder: whether to create a local `.venv` and where.
3. Case workspace folder: where CFD cases and outputs will be stored.

Recommended layout:

```text
Skill install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Local Python environment folder:
C:/Users/<your-user-name>/Documents/autostar_env/.venv

Case workspace folder:
C:/Users/<your-user-name>/Documents/autostar_runs
```

Give Codex this prompt:

```text
Install the AutoStar preview from https://github.com/Ouscar-ou/AutoStar.
Before installation, ask me for the skill folder, whether to create a local .venv, and the CFD case workspace.
Prefer local environments and do not modify global Python, Conda, PATH, or the STAR-CCM+ installation directory.
After installation, run integrity-check and version and explain the results.
```

If the ZIP is already downloaded, replace the first line with:

```text
Install AutoStar from this local ZIP: C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.3-windows-x64.zip.
```

The current preview normally requires no additional Python packages. Do not run `pip install`, upgrade pip, modify global PATH, or change the STAR-CCM+ installation directory without user approval.

## 3. Manual ZIP Installation

1. Download `AutoStar-v0.3.3-windows-x64.zip` from the official GitHub Release.
2. Extract the ZIP to a temporary folder.
3. Copy the package contents to the user-approved skill folder, for example:

```text
C:/Users/<your-user-name>/.codex/skills/autostar
```

4. Confirm the directory layout:

```text
C:/Users/<your-user-name>/.codex/skills/autostar/SKILL.md
```

Do not create an extra nested `AutoStar/AutoStar/` directory.

5. Optionally create a local Python environment in a user-approved location:

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
```

6. Run checks from the AutoStar installation folder:

```powershell
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py integrity-check
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py version
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./tests/verify_public_preview_package.py
```

If no `.venv` was created, replace the executable prefix with `python`.

## 4. Post-Installation Check

A normal installation should report:

- A successful installation-completeness check.
- `Edition: public`.
- `Available mesh presets: quick, coarse`.
- The detected STAR-CCM+ path and version.

If STAR-CCM+ is not found, confirm the path as described in section 5 before meshing or solving.

After the checks pass, open a new Codex task or restart Codex so it rescans `.codex/skills`. You can then say: "Use AutoStar to check my propeller STEP file."

## 5. STAR-CCM+ Path

AutoStar attempts to locate STAR-CCM+ automatically. If discovery fails, confirm the real installation path and set a launcher path for the current PowerShell session:

```powershell
$env:STARCCM_BAT="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
python ./starccm_cli.py version
```

`STARCCM_EXE` may also point to a usable local STAR-CCM+ launcher. Prefer a temporary current-session setting first; the user decides whether any system-level environment setting is appropriate.

## 6. First Case

Chat-based test entry: [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md)

Open that file and give Codex the post-install smoke-check prompt. After it passes, use the quick-preflight and 400-step-pilot prompts with your own STEP/STP file.

You can also begin with:

```text
Use AutoStar to check this propeller STEP file:
STEP=your STEP/STP file path
Goal=workflow validation

Check the environment and geometry first. Then ask me, one item at a time, for dimensions, operating conditions, flow direction, inlet/outlet sides, rotation vector, mesh, and core count.
Summarize and cross-check all direction inputs. Do not start meshing or solving without my confirmation.
```

AutoStar first checks the environment and geometry, then asks for diameter D, axial length L, speed, flow direction, rpm, rotation vector, fluid properties, mesh, and core count. Preflight and the 400-step pilot begin only after the user confirms the complete setup.

`quick` is the lowest-cost workflow check. `coarse` provides a somewhat denser preliminary screen. A 400-step run is intended to identify obvious direction, mesh, and divergence risks, not to serve directly as a final engineering result.

## 7. Local Extensions And Upgrades

Do not directly modify or replace official program files in the installation. Put custom content in:

- `extensions/`: independent scripts, adapters, and tool integrations.
- `workflows/`: local workflow instructions and definitions.
- `templates/local/`: local case, input, and report templates.

Recommended upgrade process:

1. Back up custom content under `extensions/`, `workflows/`, and `templates/local/`.
2. Install the new version in a temporary folder and complete the installation checks.
3. Replace the previous official installation files with the new version.
4. Restore custom content to the corresponding extension folders.
5. Run `integrity-check` and `version` again.

Keep CFD cases and results in a separate case workspace, not in the skill installation folder.

## 8. Troubleshooting

- `python` is unavailable: confirm the local Python path or ask Codex to create a local `.venv` in a user-approved folder.
- STAR-CCM+ is not found: confirm the launcher path and apply the current-session setting from section 5.
- Directory layout is wrong: make sure `SKILL.md` is directly under `.../.codex/skills/autostar/`.
- Codex does not detect the skill: open a new task or restart Codex, then recheck the installation folder.
- Security software blocks the EXE: confirm that the file came from the official GitHub Release, then follow the local security policy.
- STEP/STP import fails: check units, body integrity, and shaft alignment in CAD or STAR-CCM+.

For a complete chat-based test, see [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md).
