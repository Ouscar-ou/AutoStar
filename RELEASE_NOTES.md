# Release Notes

## 0.3.6 Public Preview

- Makes workflow dry-run read-only: it no longer writes project/report files, updates execution records, or launches STAR-CCM+ and cloud postprocessing.
- Adds `workflow continue --to-iterations` for explicit absolute-target continuation without geometry import, domain creation, or remeshing.
- Prevents internal workflow child commands from repeatedly launching cloud export; a successful top-level workflow triggers at most one automatic image export.
- Separates prism-design y+ from result-acceptance y+ and makes both public y+ commands use one persisted report and one area-weighted assessment.
- Fixes STAR-CCM+ 18.04 scene compilation and marks successfully retried failures as resolved instead of retaining them as active report risks.
- Restores populated preflight derived values, clarifies inflow-diameter versus relative-chord Reynolds numbers, and reports residual plateaus with a mesh-repair recommendation.
- Unifies mesh-quality output so unavailable threshold counts are not reported as zero and STAR mesher/prism risk signals remain visible in the canonical gate.
- Keeps a risky 400-step pilot available for diagnosis while blocking longer continuation until the user explicitly confirms the mesh risk.
- Expands `results/results.json` with stable coefficients, sign conventions, stability, mesh/y+ gates, and recommended-use fields while preserving raw report values.
- Warns when wall-resolved prism-design y+ is unresolved or differs from the result-acceptance target.
- Expands regression coverage for dry-run immutability, safe continuation, derived preflight fields, resolved failures, version metadata, and public-only boundaries.

## 0.3.5 Public Preview

- Corrects STAR mesh-quality field normalization so measured cell quality, volume change, skewness angle, and face validity cannot be silently skipped.
- Makes the default 400-step smoke-test solve a real report-only pilot that writes pilot y+ diagnostics and pauses before any longer continuation.
- Records the completed STAR iteration count and compares it with the requested target before a continuation run.
- Removes the report-facing visibility-switch hint and keeps public report details fixed to the public view.
- Corrects Chinese headings and labels in generated workflow reports.

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
