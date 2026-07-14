# AutoStar Release Validation

Validation date: 2026-07-13
Package: `autostar`
Edition: `public`
Version: `0.3.2-public-preview`

## Local Validation Results

All checks passed on the release machine.

Commands run from this package root:

```powershell
python .\tests\verify_public_preview_package.py
python .\tests\verify_public_preview_package.py --with-engine
```

Validated behavior:

- Required release files are present.
- No `__pycache__`, `.pyc`, `.sim`, `.stp`, `.step`, logs, backup runtime exe, private-key files, or dotenv files are included.
- Public wrapper forces `Edition: public` even if the shell contains other mode environment variables.
- `version` exposes exactly `quick, coarse` as available mesh presets.
- `version` reports `OSK activation: not required for this preview edition`.
- `version` reports signed-manifest integrity as `verified`.
- An unchanged package reports `Source: official core verified`.
- Public-preview package does not include separate activation helpers, private runtime helpers, or internal-only binaries.
- Example quick and coarse preflights pass or warn.
- Environment and case-level edition spoofing cannot unlock unavailable mesh presets.
- Every restricted higher-density preset probe is blocked at preflight with `Use one of: quick, coarse`.
- Direct EXE author queries, Chinese author queries, and `--ai-notice` work without the Python wrapper.
- Direct EXE help does not expose activation, batch optimization, GCI, macro-preview, REPL, custom-density controls, or the preflight bypass.
- Required-core and executable-byte tampering stop execution with exit code 78.
- Advisory documentation changes continue with visible local warnings.
- Files under `extensions/`, `workflows/`, and `templates/local/` continue with `official core + user extensions`.
- Files added outside approved extension roots continue with an unmanaged-file warning.
- Strict official-package verification rejects packages containing local extensions.
- PE metadata identifies AutoStar, OSK, and version `0.3.2.0`.
- Python files compile successfully without writing bytecode into the package.
- SHA256 release manifest matches the package contents.

## Payload Audit

The bundled `bin/starccm_engine.exe` was rebuilt from a generated public-only source tree and compiled directly as one Nuitka onefile executable.

Payload audit results:

- No PyInstaller wrapper, nested core executable, Python `PYZ` archive, bundled docs, or bundled examples are present.
- Cloud postprocessing, Pillow contact-sheet support, authorship handling, and AI notice handling are compiled into the same Nuitka executable.
- No exact restricted high-density template identifiers, activation-helper identifiers, device-binding fields, or private signing material were found in the generated public source or final executable.
- The AI notice is part of executable control flow rather than an appended removable overlay.
- The Ed25519 release manifest is signed by a DPAPI-protected private key stored outside the repository; only the public verifier is compiled into the engine.
- Manifest v2 classifies exactly five files as required core and all other official files as advisory.

Current release hashes:

- `bin/starccm_engine.exe` SHA256: `9115A03D97B7DE673AF8FB8526BC96517D4234E014E6654118CE3CD4B35506B6`
- Final zip SHA256 should be computed after packaging because embedding the zip hash inside the zip would change the zip hash itself.

## Publish Note

Publish this package or the generated zip only. Do not publish the parent release-kit folder because it may contain local development artifacts.
