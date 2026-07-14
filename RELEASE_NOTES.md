# Release Notes

## 0.3.2-public-preview

- Initial public-preview release for STAR-CCM+ open-water propeller CFD workflow validation.
- Limits public mesh presets to `quick` and `coarse`.
- Provides STEP/STP checks, explicit direction semantics, preflight, 400-step pilot diagnostics, reports, and compiled cloud postprocessing.
- Uses a single public-only Nuitka executable with no nested private engine or exposed postprocess Python module.
- Compiles author queries, Chinese author queries, AI notice handling, and Ed25519 manifest verification into executable control flow.
- Enforces required hashes for the engine, public wrappers, AI policy, and `LICENSE`.
- Treats README, INSTALL, examples, ordinary docs, and `SKILL.md` changes as visible warnings rather than runtime failures.
- Supports user-owned additions under `extensions/`, `workflows/`, and `templates/local/` without automatic execution.
- Adds SHA256-before-extraction installation instructions and extension-preserving upgrades.
- Provides GitHub Private Vulnerability Reporting as the private security channel.
- Includes restricted-preset, environment-spoofing, core-tamper, advisory-warning, extension, package-integrity, and executable-metadata tests.
