# Release Notes

## 0.3.4 Public Preview

- Fixes automatic `run_report.md` generation for public-preview projects.
- Renames the internal imported-CAD-body count so it is no longer presented as a blade count, while preserving domain-creation behavior and migrating older project states.
- Removes fixed cell-count expectations; `quick` and `coarse` remain relative workflow-validation presets whose resulting counts depend on geometry and meshing.
- Adds a compiled-engine regression test covering report generation from an existing solved-project state.

## 0.3.3 Public Preview

- Simplifies ZIP installation by removing the separate `SHA256SUMS.txt` user step.
- Keeps signed-manifest and bundled-runtime integrity verification after extraction.
- Improves Chinese and English user-facing setup, interaction, and extension guidance.
- Aligns the public package with protected-branch, protected-tag, and least-privilege release practices.
- Rebuilds the public-only runtime with AutoStar `0.3.3.0` product metadata.

## 0.3.2 Public Preview

- Introduces the AutoStar public preview for STAR-CCM+ open-water propeller CFD workflow validation.
- Provides `quick` and `coarse` mesh presets for preliminary workflow checks.
- Adds STEP/STP geometry review, explicit direction inputs, preflight, and 400-step pilot diagnostics.
- Reports residuals, thrust, torque, stability, y+, and result usability in structured Markdown and JSON outputs.
- Exports four-view propeller pressure/y+ images, center-plane pressure/velocity, mesh sections, and contact sheets from solved cases.
- Includes Chinese and English installation guides and Codex chat-based test prompts.
- Provides dedicated folders for user extensions, local workflows, and local templates.
- Adds release-package verification and installation-completeness checks.

Future releases will progressively introduce additional engineering mesh, grid-assessment, batch-analysis, automated-iteration, diagnostic, and reporting capabilities after validation.
