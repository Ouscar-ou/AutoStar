# Examples

This AutoStar public preview package includes a minimal quick example and Codex chat prompts for STAR-CCM+ propeller workflow validation.

## Files

- `preview_quick_case.yaml`: editable quick mesh example.
- `codex_chat_test.zh.md`: Chinese copy-and-paste prompts for testing through Codex chat.
- `codex_chat_test.en.md`: English copy-and-paste prompts for testing through Codex chat.

## How to use

For chat-based testing, start with `codex_chat_test.zh.md` or `codex_chat_test.en.md`.

For manual YAML testing:

1. Copy `preview_quick_case.yaml` to your project directory as `case.yaml`.
2. Replace `geometry.stp` with your STEP/STP path.
3. Confirm D/L, velocity, flow direction, rpm, rotation vector, MRF axis/origin.
4. Run preflight before launching STAR-CCM+.

The package does not bundle a propeller STEP/STP file. Use your own geometry for real CFD workflow testing.

## Current Limit

Available mesh presets: `quick`, `coarse` only. Results are for workflow validation and screening, not final engineering reporting.
