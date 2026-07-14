# AutoStar 安装说明

[English installation guide](INSTALL.md) | 中文

本文档用于安装 AutoStar 初步版本。AutoStar 不包含 Siemens STAR-CCM+ 软件或授权，使用前请确认本机 STAR-CCM+ 可以正常启动并具有有效授权。

## 1. 环境要求

- Windows 10/11。
- PowerShell 中可用的 Python 3.10+。
- 本机已安装 Siemens STAR-CCM+；当前版本已在 STAR-CCM+ `18.04.008-R8` 上验证。
- 一个用于存放 CFD 算例和输出的独立工作目录。

## 2. 推荐：让 Codex 安装

安装前先确定安装来源和三个本地路径。

安装来源可以是：

1. GitHub 仓库：`https://github.com/Ouscar-ou/AutoStar`
2. 官方 Release ZIP：例如 `C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.2-windows-x64.zip`
3. 已解压或已 clone 的本地文件夹。

需要用户确认的三个路径是：

1. Skill install folder：AutoStar skill 的安装位置。
2. Local Python environment folder：是否创建局部 Python `.venv`，以及创建位置。
3. Case workspace folder：后续 CFD 算例和结果的保存位置。

推荐布局：

```text
Skill install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Local Python environment folder:
C:/Users/<your-user-name>/Documents/autostar_env/.venv

Case workspace folder:
C:/Users/<your-user-name>/Documents/autostar_runs
```

可以直接把下面的提示词交给 Codex：

```text
请从 https://github.com/Ouscar-ou/AutoStar 安装 AutoStar 初步版本。
安装前先询问我 skill 安装目录、是否创建局部 .venv，以及 CFD 算例输出目录。
优先使用局部环境，不要修改全局 Python、Conda、PATH 或 STAR-CCM+ 安装目录。
安装完成后运行 integrity-check 和 version，并用中文说明检查结果。
```

如果已经下载 ZIP，可以把第一行改为：

```text
请从这个本地 ZIP 安装 AutoStar：C:/Users/<your-user-name>/Downloads/AutoStar-v0.3.2-windows-x64.zip。
```

当前版本通常不需要额外 Python 包。除非用户明确同意，不要运行 `pip install`、升级 pip、修改全局 PATH，或改动 STAR-CCM+ 安装目录。

## 3. 手动从 ZIP 安装

1. 从官方 GitHub Release 下载 `AutoStar-v0.3.2-windows-x64.zip`。
2. 将 ZIP 解压到临时文件夹。
3. 将包内容复制到用户确认的 skill 目录，例如：

```text
C:/Users/<your-user-name>/.codex/skills/autostar
```

4. 确认安装目录层级正确：

```text
C:/Users/<your-user-name>/.codex/skills/autostar/SKILL.md
```

不要多嵌套一层 `AutoStar/AutoStar/`。

5. 可选：在用户指定的位置创建局部 Python 环境：

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
```

6. 在 AutoStar 安装目录中运行检查：

```powershell
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py integrity-check
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py version
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./tests/verify_public_preview_package.py
```

如果没有创建 `.venv`，将命令前半部分替换为 `python`。

## 4. 安装完成后的检查

正常情况下应看到：

- 安装完整性检查通过。
- `Edition: public`。
- `Available mesh presets: quick, coarse`。
- 本机 STAR-CCM+ 路径与版本信息。

如果 STAR-CCM+ 未被识别，先按第 5 节确认路径，不要直接开始网格或求解。

检查通过后，新开一个 Codex 任务或重启 Codex，让 Codex 重新扫描 `.codex/skills`。之后可以直接说“使用 AutoStar 检查我的螺旋桨 STEP”。

## 5. STAR-CCM+ 路径

AutoStar 会尝试自动查找 STAR-CCM+。如果未识别到，请先确认实际安装位置，再只为当前 PowerShell 会话设置一个启动路径：

```powershell
$env:STARCCM_BAT="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
python ./starccm_cli.py version
```

也可以使用 `STARCCM_EXE` 指向本机可用的 STAR-CCM+ 启动程序。建议先使用当前会话的临时设置；是否写入系统环境由用户自行决定。

## 6. 第一个算例

对话式测试入口：[`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)

打开该文件并复制“安装后冒烟检查”提示词给 Codex。检查通过后，再使用“quick 预检”和“400-step pilot”提示词测试自己的 STEP/STP 文件。

也可以直接从下面这段话开始：

```text
使用 AutoStar 检查这个螺旋桨 STEP：
STEP=你的 STEP/STP 文件路径
目标=流程验证

请先检查环境和几何，再用中文逐项询问我需要确认的尺寸、工况、来流方向、入口/出口、旋转矢量、网格和核数。
汇总并闭环检查所有方向信息；未经我确认，不要开始网格或求解。
```

AutoStar 会先完成环境与几何检查，再询问螺旋桨直径 D、轴向长度 L、速度、流向、转速、旋转矢量、流体参数、网格和核数。用户确认完整工况后，才进入 preflight 和 400-step pilot。

`quick` 适合最低成本的流程验证，`coarse` 适合稍密的初步筛查。400 步用于发现明显方向、网格和发散风险，不应直接作为正式工程最终结果。

## 7. 本地扩展与升级

请不要直接修改或替换安装包中的官方程序文件。自定义内容应放入：

- `extensions/`：独立脚本、适配器和工具集成。
- `workflows/`：自定义工作流说明与定义。
- `templates/local/`：本地 case、输入和报告模板。

升级建议：

1. 备份 `extensions/`、`workflows/` 和 `templates/local/` 中的自定义内容。
2. 将新版本安装到新的临时目录并完成安装检查。
3. 用新版本替换旧的官方安装文件。
4. 将自定义内容恢复到对应的扩展目录。
5. 再次运行 `integrity-check` 和 `version`。

CFD 算例和结果应保存在独立的 case workspace 中，不要放在 skill 安装目录内。

## 8. 常见问题

- `python` 不可用：先确认本机 Python 安装位置，或让 Codex 在用户确认的目录创建局部 `.venv`。
- STAR-CCM+ 未识别：确认启动文件路径后，按第 5 节在当前会话设置路径。
- 安装目录层级错误：确保 `SKILL.md` 直接位于 `.../.codex/skills/autostar/`。
- Codex 没有识别 skill：新开任务或重启 Codex，再确认安装目录。
- EXE 被安全软件拦截：确认文件来自官方 GitHub Release 后，按本机安全策略处理。
- STEP/STP 导入失败：先在 CAD 或 STAR-CCM+ 中确认单位、实体完整性和轴线方向。

更完整的对话测试见 [`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)。
