# Local Workflows / 本地工作流

Place user-owned Markdown, YAML, or JSON workflow definitions and agent instructions in this directory.

将用户自己的 Markdown、YAML、JSON 工作流定义和 agent 操作说明放在这里。

- Keep case outputs in a separate workspace, not inside the AutoStar installation.
- Reference only documented public CLI commands.
- A workflow must not request hidden mesh presets, preflight bypasses, or automatic execution without confirmation.
- AutoStar does not automatically trust or execute local workflow files.

Suggested names include `geometry_check.md`, `pilot_screening.yaml`, and `report_export.json`.
