# Runtime binaries

This directory contains the bundled runtime binary required by AutoStar public preview.

Expected file:

- `starccm_engine.exe`: single-layer Nuitka public-preview runtime engine with built-in cloud postprocessing and signed-manifest verification.

AutoStar public preview does not require separate AutoStar activation. Users still need their own valid Siemens STAR-CCM+ installation and license.

Do not place private keys, server credentials, signing keys, API tokens, or service credentials in this directory.

The release signing private key is never distributed. The package contains only `release_manifest.ed25519.sig`; the engine contains the corresponding public verification key and checks its own hash plus critical public files before running CFD commands.

Users should normally run the public wrapper `starccm_cli.py`. For release verification, direct commands `starccm_engine.exe integrity-check`, `starccm_engine.exe author`, and `starccm_engine.exe --ai-notice` are supported.
