# AutoStar Release Validation

Validation date: 2026-07-14
Package: `autostar`
Edition: `public`
Version: `0.3.3-public-preview`

## Validation Summary

The release package passed the automated public-package and bundled-runtime checks on the release machine.

```powershell
python .\tests\verify_public_preview_package.py
python .\tests\verify_public_preview_package.py --with-engine
```

Validated areas:

- Required package files and documentation are present.
- The package exposes the public edition with `quick` and `coarse` mesh presets.
- Example quick/coarse preflight cases complete with expected pass or warning outcomes.
- Installation, first-case, direction-confirmation, and local-extension guidance are present in Chinese and English.
- Python entry points compile and the bundled runtime responds to documented commands.
- Cloud postprocessing supports dry-run validation and report-image export.
- Public-package boundary, installation completeness, and modified-package behavior tests pass.
- Executable product metadata identifies AutoStar, OSK, and version `0.3.3.0`.
- A fresh extraction of the generated Release ZIP passes the installation and runtime checks.

## Package Scope

The published package contains the AutoStar public-preview runtime, wrappers, documentation, examples, tests, and designated local-extension folders. CFD case files, STEP/STP geometry, `.sim` files, logs, and local development outputs are not part of the Release package.

Publish only the tested repository package or generated Release ZIP.
