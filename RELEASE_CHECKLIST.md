# AutoStar Release Checklist

Before publishing:

- [ ] `python starccm_cli.py version` reports the public edition and `quick, coarse` mesh presets.
- [ ] `python starccm_cli.py integrity-check` passes on the final package.
- [ ] Documented wrapper and runtime commands respond correctly.
- [ ] Example quick and coarse preflight tests pass or produce expected warnings.
- [ ] Cloud-postprocessing dry-run and report export tests pass.
- [ ] `python tests/verify_public_preview_package.py --with-engine` passes.
- [ ] Repository and package secret scans report no sensitive development material.
- [ ] The package contains no CFD run outputs, STEP/STP geometry, `.sim` files, logs, caches, or backup executables.
- [ ] README, INSTALL, LICENSE, SECURITY, docs, examples, and local-extension folders are present.
- [ ] Chinese and English installation links and Codex chat-test links work.
- [ ] Installation instructions require user confirmation before creating environments or changing paths.
- [ ] Local-extension upgrade instructions cover `extensions/`, `workflows/`, and `templates/local/`.
- [ ] Release metadata and package verification files are refreshed.
- [ ] PE product/file metadata reports AutoStar, OSK, and the intended release version.
- [ ] The final ZIP installs cleanly and passes `integrity-check` from a fresh extraction.
- [ ] The Git tag and GitHub Release point to the tested commit.
- [ ] Repository visibility and private security-reporting settings are correct.
