# AutoStar

English | [中文](README.md)

AutoStar is a conversational workflow for Siemens STAR-CCM+ propeller open-water CFD. The current preview provides the `quick` and `coarse` mesh presets for STEP/STP geometry checks, physical-direction confirmation, workflow validation, 400-step pilot screening, basic result interpretation, and cloud-image export.

> AutoStar does not include STAR-CCM+ software or a STAR-CCM+ license. Users need their own properly licensed and runnable Siemens STAR-CCM+ installation.

## Getting Started

- English installation guide: [`INSTALL.md`](INSTALL.md)
- Codex chat test: [`examples/codex_chat_test.en.md`](examples/codex_chat_test.en.md)
- 中文说明：[`README.md`](README.md)

Using Codex for installation is recommended. Before installation, Codex should ask where to place the skill, whether to create a local Python environment, and where CFD cases should be stored. It should not modify global Python, PATH, or the STAR-CCM+ installation directory by default.

```text
Install the AutoStar preview from https://github.com/Ouscar-ou/AutoStar.
Before installation, ask me for the skill folder, whether to create a local .venv, and the case workspace.
Do not modify global Python, PATH, or the STAR-CCM+ installation directory. Check the environment and STAR-CCM+ version after installation.
```

After installation, run these commands from the AutoStar folder:

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

`integrity-check` confirms that the installation is complete, while `version` checks Python and STAR-CCM+ discovery. When both checks pass, open a new Codex task or restart Codex, then use AutoStar through normal chat.

## Preview

The image below shows postprocessing from an open-water propeller case, including pressure clouds, y+ clouds, center-plane velocity/pressure, and mesh sections. It demonstrates the current reporting style and is not a formal engineering conclusion.

![Propeller CFD result clouds preview](docs/assets/result_clouds_preview.png)

## Current Capabilities

The current version can help users:

- Inspect STEP/STP files, units, bounding boxes, shaft alignment, and obvious geometry risks.
- Confirm shaft axis, flow direction, inlet/outlet sides, and rotation vector as separate physical inputs.
- Check the local STAR-CCM+ environment and produce a preflight assessment before calculation.
- Use `quick` or `coarse` meshes for workflow validation and preliminary CFD screening.
- Run a 400-step pilot after user confirmation and assess residuals, thrust, torque, stability, and y+.
- Continue to an explicitly confirmed total iteration target without repeating import, domain creation, or meshing.
- Produce `preflight_report.md`, `run_report.md`, and JSON diagnostics.
- Export four-view surface pressure/y+ images, center-plane pressure/velocity, mesh sections, and report contact sheets from solved cases.

AutoStar will continue to expand toward engineering applications. Higher-density engineering meshes, grid-independence assessment, batch operating-point analysis, automated design iteration, and deeper diagnostics and reporting will be introduced progressively after validation. Feature availability and intended use will follow each release note.

## Chat-Based Use

Users do not need to write a complete `case.yaml` before starting. Provide a STEP/STP path and the test objective. AutoStar first checks the environment and geometry, then asks for missing information one item at a time. If dimensions, directions, or operating conditions are unclear, it should explain and ask rather than guess and launch a run.

Copy this prompt to start a first case:

```text
Use AutoStar to check this propeller STEP file:
STEP=your STEP/STP file path
Goal=workflow validation/preliminary screening

First check my STAR-CCM+ environment and geometry. Then ask me, one item at a time, for the operating conditions, directions, mesh, and compute resources that still need confirmation.
Summarize the shaft axis, flow direction, inlet/outlet sides, and rotation vector and perform a consistency check. Do not start meshing or solving without my confirmation.
```

AutoStar normally asks for:

- Physical propeller diameter D and axial length L.
- Positive inflow-speed magnitude, actual flow direction, and inlet/outlet sides.
- Positive rpm magnitude and the angular-velocity vector defined by the right-hand rule.
- Water density, viscosity, and turbulence model.
- `quick` or `coarse` mesh, a 400-step pilot, and the parallel-core count.
- Case workspace, output location, and confirmation for the current run.

If a parameter is unknown, answer: "Unknown; estimate it from the STEP file first and identify the risk." AutoStar keeps estimated values distinct from confirmed inputs and does not treat a bounding-box dimension as final physical truth.

## What Users Receive

A standard preview run normally produces:

1. Environment and STAR-CCM+ version checks.
2. STEP/STP geometry and direction-risk notes.
3. A confirmed operating-condition summary and preflight report.
4. Mesh-generation status and 400-step pilot results.
5. Plain-language interpretation of residuals, thrust, torque, stability, and y+.
6. A usability level, known risks, and recommended next actions.
7. Pressure, y+, section, and mesh images when a solved case is available.

After each run, AutoStar lists direct links to the reports, JSON diagnostics, simulation file, and generated postprocessing images. If meshing, convergence, or cloud export has a problem, it still links the diagnostics that were produced and identifies the failed stage and next action.

The 400-step pilot is primarily a direction, mesh, and obvious-divergence screen. AutoStar reports mesh generation separately from the mesh-quality gate and does not treat `mesh_success=true` as a quality pass; clear mesh risks should be repaired first. After the user confirms a higher total, AutoStar uses the dedicated continuation path to run only the missing iterations and refresh results. `--dry-run` first provides a read-only plan without writing project files or launching STAR-CCM+.

## Direction Inputs

A propeller case needs these inputs separately; a single ambiguous `axis=X` is not enough:

- `shaft_axis`: the geometric shaft axis, such as X, Y, or Z.
- `flow_direction`: the actual water-flow direction, such as `-X`.
- `inlet_side` / `outlet_side`: which axial sides contain the inlet and outlet.
- `rotation_vector`: angular-velocity vector direction by the right-hand rule, such as `+X`.
- `velocity` / `rpm`: positive magnitudes only; directions are stated separately.

AutoStar checks these inputs for consistency and uses them to arrange the inlet/outlet sides of the domain, MRF region, and local refinements.

## Requirements

- Windows 10/11.
- Python 3.10+.
- A locally installed and runnable Siemens STAR-CCM+ installation.
- A valid Siemens STAR-CCM+ license supplied by the user or organization.
- STEP/STP propeller geometry and confirmable operating conditions.

The current validated environment is Windows, Python 3.13, and STAR-CCM+ `18.04.008-R8`. Start with STAR-CCM+ `18.04+` in the same family or a newer release. Major STAR-CCM+ versions may differ in Java APIs, field-function names, or scene export, so run `version` before first use.

## Local Extensions

For easier upgrades and support, do not directly modify or replace official program files in the AutoStar installation. Put custom content in the designated folders:

- `extensions/`: independent scripts, adapters, and external-tool integrations.
- `workflows/`: local workflow instructions and definitions.
- `templates/local/`: local case, input, and report templates.

Back up these three folders before upgrading and restore custom content to the corresponding folders after installing the new version. Feature requests, compatibility issues, and reproducible defects can be reported through GitHub Issues.

## Intended Use

Current `quick` / `coarse` results are intended for workflow validation, education, demonstrations, and preliminary screening. They should not be treated directly as formal engineering certification, class approval, or publication-ready final CFD. Users remain responsible for assessing mesh density, convergence, physical models, and experimental agreement before relying on results.

See [`LICENSE`](LICENSE) and [`LICENSE.md`](LICENSE.md) for the complete terms.

STAR-CCM+ is a Siemens commercial software product and trademark. AutoStar is not an official Siemens product, does not include STAR-CCM+ software or licensing, and does not replace Siemens licensing requirements.

## Feedback

Use [GitHub Issues](https://github.com/Ouscar-ou/AutoStar/issues) for general feedback. Include the STAR-CCM+ and Windows versions, `version` output, sanitized operating conditions, relevant reports, and key error logs when possible.

Submit security concerns privately through [GitHub Private Vulnerability Reporting](https://github.com/Ouscar-ou/AutoStar/security/advisories/new).
