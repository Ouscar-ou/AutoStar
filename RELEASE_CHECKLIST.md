# AutoStar Release Checklist

Before publishing:

- [ ] `python starccm_cli.py version` shows `Edition: public`.
- [ ] Available mesh presets are exactly `quick, coarse`.
- [ ] Version output says `OSK activation: not required for this preview edition`.
- [ ] Version output says `Integrity: verified` and `Source: official core verified`.
- [ ] Direct EXE `author`, Chinese author query, `--ai-notice`, and `integrity-check` pass.
- [ ] Direct EXE help contains no activation, optimization, GCI, macro-preview, or REPL commands.
- [ ] `examples/preview_quick_case.yaml` uses `mesh.preset: quick`.
- [ ] No separate activation helper, private runtime helper, or internal-only binary is included.
- [ ] No `__pycache__`, `.pyc`, backup exe, test run output, `.sim`, or `.stp` files are included.
- [ ] No private keys, API tokens, service credentials, or server credentials are included.
- [ ] `python tests/verify_public_preview_package.py --with-engine` passes, including spoofed-edition, core tamper, advisory warning, extension, and strict-package tests.
- [ ] Required integrity policy covers exactly the engine, two public wrappers, AI policy, and `LICENSE`.
- [ ] `extensions/`, `workflows/`, and `templates/local/` additions do not stop normal runtime integrity checks.
- [ ] `release_manifest.sha256.json` has been regenerated and `release_manifest.ed25519.sig` verifies.
- [ ] PE product/file metadata reports AutoStar `0.3.2.0` and company OSK.
- [ ] Final ZIP and external `SHA256SUMS.txt` have been generated and independently checked.
- [ ] Git tag `v0.3.2` and the GitHub Release point to the tested commit.
- [ ] Repository visibility is Public and GitHub Private Vulnerability Reporting is enabled.
- [ ] README, INSTALL, LICENSE, SECURITY, docs, and examples are present.
- [ ] Installation docs tell agents to ask the user for the target install folder before copying files or changing environment settings.
