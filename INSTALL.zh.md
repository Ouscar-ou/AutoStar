# 安装说明

[English installation guide](INSTALL.md) | 中文

本文档用于 AutoStar 公开预览版安装。

AutoStar 不包含 Siemens STAR-CCM+ 软件本体，不提供 STAR-CCM+ 授权，也不会绕过任何商业软件授权。你必须使用自己或所在机构合法授权的本机 STAR-CCM+。

## 1. 环境要求

- Windows 10/11。
- PowerShell 中可用的 Python 3.10+。
- 本机已安装 Siemens STAR-CCM+；当前预览版已在 STAR-CCM+ 18.04.008 上验证。
- 来自 Siemens 或所在机构的有效 STAR-CCM+ license。
- STEP/STP 螺旋桨几何文件，以及已确认的物理工况。

## 2. 推荐：使用 Codex 安装

这是多数 Codex 用户推荐的方式，但 Codex 在写入文件或创建环境前必须先询问你。

安装前先确认一个安装来源和三个路径。

安装来源可以三选一：

1. GitHub 仓库地址：例如 `https://github.com/Ouscar-ou/AutoStar`
2. 已下载的 release ZIP：例如 `C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.2-windows-x64.zip`
3. 已解压或已 clone 的本地文件夹：例如 `C:/Users/<your-user-name>/Downloads/AutoStar`

如果 Codex 所在环境可以访问 GitHub，直接把 GitHub URL 写进 prompt 最方便。如果网络、权限或仓库可见性不稳定，建议你先手动下载官方 release ZIP，再把本地 ZIP 路径交给 Codex。不要把 GitHub token、账号密码或私有凭据直接粘贴到 prompt 里。

三个路径是：

1. Skill install folder：AutoStar skill 要复制到哪里。
2. Local Python environment folder：是否创建局部 Python `.venv`，推荐创建但必须由你确认位置。
3. Case workspace folder：后续 CFD 算例和输出放在哪里。

推荐布局：

```text
Skill install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Local Python environment folder:
C:/Users/<your-user-name>/Documents/autostar_env/.venv

Case workspace folder:
C:/Users/<your-user-name>/Documents/autostar_runs
```

你可以这样让 Codex 安装：

```text
请从 https://github.com/Ouscar-ou/AutoStar 安装 AutoStar 初步版本。安装前先问我 skill 放在哪里、是否创建局部 .venv、算例输出放在哪里；不要修改全局 Python、PATH 或 STAR-CCM+ 安装目录。安装后运行 version 检查环境。
```

如果你已经下载了 ZIP，也可以这样说：

```text
请从这个本地 ZIP 安装 AutoStar：C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.2-windows-x64.zip。安装前先问我 skill 放在哪里、是否创建局部 .venv、算例输出放在哪里；不要修改全局 Python、PATH 或 STAR-CCM+ 安装目录。先核对 SHA256SUMS.txt，安装后再运行 integrity-check 和 version。
```

如果你同意创建局部 `.venv`，在你确认的文件夹中执行：

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe C:/Users/<your-user-name>/.codex/skills/autostar/starccm_cli.py version
```

当前预览版通常不需要安装额外 Python 包。除非你明确要求，否则不要运行 `pip install`、不要升级 pip、不要修改全局 PATH。

重要：除非你明确同意具体动作和目标路径，否则 Codex 不应安装 Python、不应创建虚拟环境、不应修改 PATH、不应设置 `STARCCM_BAT` 或 `STARCCM_EXE`，也不应修改 STAR-CCM+ 安装目录。

## 3. 手动从 ZIP 安装

1. 从同一个官方 GitHub Release 下载 `AutoStar-v0.3.2-windows-x64.zip` 和 `SHA256SUMS.txt`。
2. 解压或运行任何文件前，先在 PowerShell 中核对 ZIP 哈希：

```powershell
$downloadDir = "C:/Users/<your-user-name>/Downloads"
$zip = Join-Path $downloadDir "AutoStar-v0.3.2-windows-x64.zip"
$sums = Join-Path $downloadDir "SHA256SUMS.txt"
$expected = ((Get-Content -LiteralPath $sums -Raw).Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries))[0].ToLowerInvariant()
$actual = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "AutoStar ZIP SHA256 mismatch: $actual != $expected" }
"AutoStar ZIP SHA256 verified: $actual"
```

3. 把校验通过的 ZIP 解压到临时文件夹。
4. 选择安装文件夹。推荐：

```text
C:/Users/<your-user-name>/.codex/skills/autostar
```

5. 把解压后的 `AutoStar` 包内容复制到该文件夹。
6. 可选但推荐：在你指定的位置创建局部 Python `.venv`，不要放进全局 Python：

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
```

7. 在 AutoStar 安装文件夹中打开 PowerShell，运行：

```powershell
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py integrity-check
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py version
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./tests/verify_public_preview_package.py
```

如果你想继续用 Codex 对话方式跑通测试案例，安装验证通过后打开 [`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)。

先复制其中“安装后冒烟检查”给 Codex；如果你已有 STEP/STP 文件，再继续复制“quick 预检”和“400-step pilot”的提示词。

正常情况下你应看到：

- `Edition: public`
- `Available mesh presets: quick, coarse`
- `OSK activation: not required for this preview edition`
- STAR-CCM+ 可执行路径和兼容版本提示。

看到这些输出后，文件层面的安装已经完成。接下来新开一个 Codex 任务/窗口，或重启 Codex，让 Codex 重新扫描 `.codex/skills` 目录。之后你就可以在 Codex 里直接说“使用 AutoStar/使用 autostar 做螺旋桨 CFD 流程检查”，Codex 会读取该 skill 并按安装好的工作流执行。

注意安装目录层级应为：

```text
C:/Users/<your-user-name>/.codex/skills/autostar/SKILL.md
```

不要变成：

```text
C:/Users/<your-user-name>/.codex/skills/autostar/AutoStar/SKILL.md
```
## 4. 首次运行检查

创建或运行任何 CFD 算例前，都应先在 AutoStar 安装文件夹运行：

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

`integrity-check` 必须显示 `AutoStar integrity: verified`。如果签名、EXE 或关键 skill 文件被修改，AutoStar 会停止执行；请重新下载官方 release，不要绕过检查。

如果要进行本地扩展，不要修改强制核心文件。自定义脚本放入 `extensions/`，工作流定义放入 `workflows/`，本地模板放入 `templates/local/`。加入扩展后来源标记会变为 `official core + user extensions`，但普通运行不会停止；发布包验证脚本仍会严格检查官方包是否原样，因此可能按预期报告 package mismatch。

如果你在发布/测试机器上，希望连同 bundled engine 一起验证：

```powershell
python ./tests/verify_public_preview_package.py --with-engine
```

只有 STAR-CCM+ 被正确识别后，才继续网格或求解。

如果你希望完全通过 Codex 对话方式测试，请打开 [`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)。

该文件包含三段可复制给 Codex 的提示词：安装冒烟检查、使用你自己的 STEP 运行 quick preflight、以及确认后继续 400-step pilot。

## 5. STAR-CCM+ 路径

AutoStar 会尝试自动寻找 STAR-CCM+。如果未识别到，请先确认 STAR-CCM+ 的安装位置，然后只在当前 PowerShell 会话中设置以下变量之一：

```powershell
$env:STARCCM_BAT="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
```

或：

```powershell
$env:STARCCM_EXE="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
```

然后重新运行：

```powershell
python ./starccm_cli.py version
```

除非你理解影响并且确实需要，否则不要永久写入这些环境变量。

## 6. 第一个算例

如果你希望直接用 Codex 对话方式完成第一个算例测试，请优先打开 [`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)。

该文件提供可直接复制给 Codex 的中文提示词入口，包括安装后冒烟检查、使用你自己的 STEP/STP 做 quick preflight，以及在确认后继续 400-step pilot。下面的命令式流程适合你想手动检查 case 文件和运行步骤时使用。

复制示例 case：

```powershell
mkdir C:/runs/case1
copy ./examples/preview_quick_case.yaml C:/runs/case1/case.yaml
```

编辑 `C:/runs/case1/case.yaml`，确认：

- STEP/STP 文件路径。
- 螺旋桨直径 `D` 和轴向长度 `L`。
- 来流方向和入口/出口侧。
- 旋转矢量方向和转速 rpm。
- 网格密度只能使用 `quick` 或 `coarse`。

然后运行 preflight：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow preflight --case C:/runs/case1/case.yaml
```

只有在 preflight 可接受、且用户确认本次运行后，才启动 workflow：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow run --case C:/runs/case1/case.yaml
```

## 7. 升级

1. 关闭正在使用该包的 STAR-CCM+ 任务。
2. 如有需要，备份 case 文件夹；正常情况下 case workspace 应位于 skill 安装目录之外。
3. 确认旧安装文件夹，然后归档整个旧目录，不要直接删除。
4. 特别检查并保留 `extensions/`、`workflows/`、`templates/local/` 中的用户自建文件。
5. 使用 `SHA256SUMS.txt` 校验新 Release ZIP，再把新的官方包安装到干净目录。
6. 只把归档中的用户自建扩展、工作流和模板复制到新包对应目录；不要覆盖新版官方 `README.md` 或任何强制核心文件。
7. 运行 `python ./starccm_cli.py integrity-check` 和 `python ./starccm_cli.py version`。
8. 未添加扩展时应显示 `official core verified`；恢复扩展后应显示 `official core + user extensions`。
9. 新版本和扩展验证完成前，保留旧安装归档。

## 8. 卸载

删除你选择的安装文件夹，例如：

```text
C:/Users/<your-user-name>/.codex/skills/autostar
```

这不会删除 STAR-CCM+，也不会删除你的 case 文件夹。

## 9. 常见问题

- Python 未找到：先决定使用现有 Python 还是安装 Python。优先使用局部 `.venv`；除非明确同意，不要修改全局 PATH。
- STAR-CCM+ 未找到：确认 STAR-CCM+ 安装路径，然后只在当前会话设置 `STARCCM_BAT` 或 `STARCCM_EXE`。
- STAR license 失败：检查你的 Siemens STAR-CCM+ license；本预览版不提供 STAR 授权。
- 杀毒软件拦截 `starccm_engine.exe`：恢复或允许官方 release 文件夹，然后核对 SHA256 manifest。
- preflight 提示只开放 quick/coarse：这是当前预览版本的预期行为。
- 轴向或方向语义不清：不要运行；先分别确认 `shaft_axis`、`flow_direction` 和 `rotation_vector`。

更多说明见 `docs/troubleshooting.md`。
