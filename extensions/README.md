# Local Extensions / 本地扩展

Place independent scripts, adapters, external-tool wrappers, and integration code in this directory.

将独立脚本、适配器、外部工具封装和集成代码放在这里。

- AutoStar detects added files but does not execute them automatically.
- Review extension code and obtain explicit user approval before execution.
- Do not modify or replace `bin/starccm_engine.exe`, `starccm_cli.py`, or `public/engine_client.py`.
- Extensions cannot unlock unavailable mesh presets or bypass preflight and execution confirmation.
- Do not store private keys, tokens, confidential geometry, `.sim` files, or licensing material here.

新增文件后，`version` 应显示 `official core + user extensions`。
