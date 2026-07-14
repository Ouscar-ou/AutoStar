# AutoStar

English | [中文](README.md)

AutoStar is a public-preview workflow package for STAR-CCM+ propeller open-water CFD. The current preview focuses on safe workflow validation and exposes only the `quick` / `coarse` mesh presets for STEP/CAD checks, direction checks, MRF/domain checks, 400-step pilot screening, and basic report interpretation.

> Important: this project does not include STAR-CCM+ itself, does not provide a STAR-CCM+ license, and does not bypass any commercial software licensing. Use your own properly licensed Siemens STAR-CCM+ installation.

## Installation Guide

Start here for first-time setup: [`INSTALL.md`](INSTALL.md)

For chat-based testing through Codex, see: [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md)

Recommended installation flow:

1. Choose the package source: GitHub URL, local release ZIP, or an already extracted/cloned local folder.
2. Put AutoStar in a local skill folder you choose, for example `C:/Users/<your-user-name>/.codex/skills/autostar`.
3. Do not modify global Python, Conda, PATH, or the STAR-CCM+ installation directory by default.
4. Run environment checks from the installation folder:

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

After verification passes, open a new Codex task/window, or restart Codex, so it can rescan `.codex/skills`. You can then use AutoStar through normal Codex chat.

If you ask Codex to install it for you, use wording like:

```text
Install the AutoStar preview from https://github.com/Ouscar-ou/AutoStar. Before installing, ask me where to place the skill, whether to create a local .venv, and where to put case outputs. Do not modify global Python, PATH, or the STAR-CCM+ installation directory. Run version after installation.
```

If network access or repository visibility is inconvenient, download the release ZIP first and give Codex the local ZIP path.

## Preview Images

The image below shows a postprocessing example from an open-water propeller case, including pressure clouds, y+ clouds, center-plane velocity/pressure, and mesh-section views. It demonstrates the report/postprocessing style of the current preview and is not a formal engineering conclusion.

![Propeller CFD result clouds preview](docs/assets/result_clouds_preview.png)

## What This Is

AutoStar provides a structured STAR-CCM+ propeller open-water CFD workflow. It helps make preprocessing, direction definitions, short-run stability checks, and basic reporting more repeatable.

The current preview includes:

- STEP/STP geometry checks.
- Propeller shaft axis, flow direction, rotation vector, and inlet/outlet-side confirmation.
- STAR-CCM+ environment checks and preflight.
- `quick` / `coarse` mesh workflow validation.
- 400-step pilot stability screening.
- y+, residual, thrust, torque, and basic report interpretation.
- Basic cloud/section image export from an existing `.sim` file.
- Codex chat-based test prompts: `examples/codex_chat_test.en.md`.

It is not a final engineering-decision tool and is not a publication-grade CFD generator. The current version is best used for workflow validation, education, direction checks, and initial CAD/mesh-risk screening.

## Current Scope

Available in the current preview:

- Mesh presets: `quick`, `coarse`.
- Workflow: environment check, STEP rough check, preflight, basic mesh/solver workflow, 400-step pilot.
- Postprocessing: pressure/y+ four-view surface images, center-plane pressure/velocity images, mesh-section images, and contact sheets from an existing `.sim` file.
- Reports: `preflight_report.md`, `run_report.md`, and JSON diagnostic files.

Not included in the current preview:

- High-density engineering mesh templates.
- Formal automatic grid-independence/GCI conclusions.
- Batch optimization, automatic design iteration, or advanced repair chains.
- Private STAR-CCM+ macro/template source code.
- Siemens STAR-CCM+ software or licensing.

## Core Integrity And Local Extensions

AutoStar `v0.3.2` uses a strict-core/open-extension integrity model. Do not modify core files. If any file below changes, AutoStar treats the official core as untrusted and stops formal commands with exit code `78`:

- `bin/starccm_engine.exe`
- `starccm_cli.py`
- `public/engine_client.py`
- `AI_USAGE_POLICY.md`
- `LICENSE`

README, INSTALL, examples, ordinary docs, and `SKILL.md` are advisory files. Local changes do not stop execution, but `integrity-check` reports warnings and the source label becomes `official core verified with local warnings`. Do not edit core files to add features, and do not present a locally modified package as an unchanged official Release.

All custom extensions must be placed in one of these directories. Do not scatter extension scripts in the AutoStar root, `bin/`, or `public/`:

- `extensions/`: independent scripts, adapters, external-tool wrappers, and integration code.
- `workflows/`: local Markdown/YAML/JSON workflow definitions and agent instructions.
- `templates/local/`: local case, input, and report templates; never store private keys, tokens, confidential geometry, or STAR-CCM+ licensing material here.

New files under these roots are outside mandatory official-core hashing. AutoStar continues to run and reports `official core + user extensions`. AutoStar does not automatically execute user scripts; the user or agent must review them and obtain explicit execution approval. Extensions cannot unlock unavailable meshes, replace the engine, bypass preflight, or remove the quick/coarse boundary.

Use these commands for normal runtime verification:

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
```

`tests/verify_public_preview_package.py` verifies that an official Release is byte-for-byte complete. After adding user extensions, this strict package test intentionally reports a package mismatch; that does not mean the official core has failed.

Feedback for maintainers may cover installation and compatibility, direction semantics, STEP import, preflight, quick/coarse mesh behavior, solver stability, reports and cloud images, extension-interface requests, and reproducible documentation defects. Include `version` and `integrity-check` output, STAR-CCM+/Windows versions, a sanitized case, relevant logs, and minimal reproduction steps. Never publish private STEP files, `.sim` files, license material, tokens, or confidential project data.

## Requirements

- Windows 10/11.
- Python 3.10+.
- A locally installed and runnable Siemens STAR-CCM+ installation.
- A valid Siemens STAR-CCM+ license, provided by the user or organization.
- STEP/STP propeller geometry.
- Confirmed physical conditions: diameter D, axial length L, inflow speed, rpm, flow direction, rotation vector, fluid properties, and related inputs.

## STAR-CCM+ Version

Current local validation environment:

- STAR-CCM+ `18.04.008-R8`
- Windows
- Python 3.13 local runtime

STAR-CCM+ `18.04+` or newer versions are recommended for testing. Different major STAR-CCM+ versions may differ in Java APIs, macro interfaces, field-function names, or scene export behavior. Always start with:

```powershell
python ./starccm_cli.py version
```

If you use another STAR-CCM+ version, verify the STAR-CCM+ path and version in the `version` output. For compatibility issues, include the `version` output, STAR-CCM+ version, and error log in your issue.

## Installation Philosophy

To avoid disturbing the user's local environment, AutoStar recommends local environments, local run folders, and explicit path confirmation.

Before installation or configuration, confirm:

1. `skill_install_dir`: the skill installation folder.
2. `local_python_env_dir`: optional local Python `.venv` folder.
3. `case_workspace_dir`: CFD case and output workspace.

Recommended layout:

```text
Skill install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Local Python environment folder:
C:/Users/<your-user-name>/Documents/autostar_env/.venv

Case workspace folder:
C:/Users/<your-user-name>/Documents/autostar_runs
```

By default, do not:

- Modify global Python or Conda.
- Modify system PATH.
- Write permanent environment variables.
- Modify the STAR-CCM+ installation directory.
- Run `pip install` or upgrade pip unless explicitly needed and confirmed.

See `INSTALL.md` for detailed installation steps.

## Quick Start

Run inside the skill folder:

```powershell
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

If using a local `.venv`:

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py version
```

Copy the example case:

```powershell
mkdir C:/runs/case1
copy ./examples/preview_quick_case.yaml C:/runs/case1/case.yaml
```

Run preflight:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow preflight --case C:/runs/case1/case.yaml
```

Only start the workflow after preflight is acceptable, direction semantics are clear, and the user confirms the run:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow run --case C:/runs/case1/case.yaml
```

## Input Template

Confirm these inputs before preflight:

```text
STEP=your STEP/STP file path
run_intent=screening
mesh=quick or coarse
D=propeller diameter, e.g. 250 mm
L=axial propeller length, e.g. 53 mm
velocity=positive inflow speed magnitude, e.g. 3.0 m/s
rpm=positive rotation speed magnitude, e.g. 900 rpm
fluid=Water
density=998.2 kg/m3
dynamic viscosity=0.001003 Pa*s
turbulence=K-Omega-SST
shaft_axis=X/Y/Z
flow_direction=actual water-flow direction, e.g. -X
inlet_side=inlet side, e.g. +X
outlet_side=outlet side, e.g. -X
rotation_vector=angular-velocity vector direction, e.g. +X
origin=[0,0,0]
prism_mode=wall_resolved
pilot=400 steps
```

See `docs/case_schema.md` for the YAML schema.

## Workflow

1. Run `version` to confirm Python, STAR-CCM+ path, and available mesh presets.
2. Check that the STEP/STP file exists and inspect units, bbox, and obvious geometry risks.
3. Confirm the input template: D/L, speed, rpm, fluid, shaft axis, flow direction, and rotation vector.
4. Run `workflow preflight`.
5. Generate surface/no-prism and prism mesh.
6. Run a 400-step pilot.
7. Review `run_report.md`, residuals, thrust/torque, and y+ diagnostics.
8. Export postprocess cloud images if a `.sim` file is available.

## Direction Convention

Do not use a single ambiguous `axis=X` to describe every direction. Confirm these separately:

- `shaft_axis`: which geometric axis the propeller shaft follows, X/Y/Z.
- `flow_direction`: the actual water-flow direction.
- `rotation_vector`: angular-velocity vector direction by the right-hand rule.
- `velocity`: positive speed magnitude only.
- `rpm`: positive rotation-speed magnitude only.

Example:

```yaml
domain:
  shaft_axis: X
  hub_axis: +X

operating_condition:
  velocity: 3.0 m/s
  flow_direction: -X
  rpm: 900 rpm
  rotation_vector: +X
```

## Postprocess Output

After `workflow run` or `results extract/analyze` succeeds, AutoStar attempts to export report-facing cloud images automatically. You can also export from an existing solved `.sim` manually:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml
```

To verify command routing, case parsing, and macro generation without launching STAR-CCM+:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml --dry-run
```

Outputs are written to `postprocess_clouds/figures`, with a report at `postprocess_clouds/postprocess_clouds_report.md`. If `run_report.md` exists, a cloud-image index is appended. Current postprocessing outputs include:

- Four-view propeller surface pressure images.
- Four-view propeller surface y+ images.
- Combined pressure/y+ contact sheet.
- Center-plane pressure/velocity images.
- Mesh-section images.
- Complete contact sheet.

## Verification

Run before publishing or after installation:

```powershell
python ./tests/verify_public_preview_package.py
python ./tests/verify_public_preview_package.py --with-engine
```

The second command calls the bundled engine and requires STAR-CCM+ to be discoverable on the local machine.

## Usage Boundaries

This repository is intended for evaluation, demonstration, education, and workflow validation. To protect author rights, please follow these boundaries:

- Do not sell, rent, resell, or redistribute this project, modified copies, or lightly repackaged versions as a competing product.
- `quick` / `coarse` outputs are intended for preliminary validation and education. They are not recommended for formal engineering certification, class approval, or publication-ready CFD conclusions. Users are responsible for any engineering, business, or publication decisions made from preliminary outputs.
- Public demos, courses, videos, or articles should cite this repository or OSK.

See `LICENSE` / `LICENSE.md` for complete terms.

## License

This package uses a custom Public Preview License, not MIT. MIT-style licenses are intentionally permissive; this preview package keeps narrower usage boundaries for author-rights protection and workflow validation.

Full terms: `LICENSE` / `LICENSE.md`.

## Siemens / STAR-CCM+ Notice

STAR-CCM+ is a Siemens commercial software product and trademark. This project is not an official Siemens product, does not include STAR-CCM+ software, does not provide a STAR-CCM+ license, and does not provide cracking, license bypassing, or license replacement services. Users must ensure that their STAR-CCM+ installation and usage comply with Siemens license terms.

## Support

When opening an issue, include:

- Output from `python ./starccm_cli.py version`.
- STAR-CCM+ version.
- Windows version.
- `case.yaml`, with private paths or sensitive geometry names removed if needed.
- `preflight_report.md` or `run_report.md`.
- Relevant log snippets, screenshots, or error messages.

Do not publicly upload confidential STEP/STP, `.sim`, or complete project files.

For vulnerabilities, private-key exposure, credential leaks, or unintended access paths, do not open a public issue. Use [GitHub Private Vulnerability Reporting](https://github.com/Ouscar-ou/AutoStar/security/advisories/new).
