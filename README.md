# AutoStar

[English](README.en.md) | 中文

AutoStar 是一个面向 STAR-CCM+ 螺旋桨开放水 CFD 的公开预览工作流包。当前预览版本重点用于安全的流程验证，只开放 `quick` / `coarse` 两档网格，用于 STEP/CAD 检查、方向检查、MRF/外域检查、400-step pilot 初筛和基础报告解读。

> 重要说明：本项目不包含 STAR-CCM+ 软件本体，不提供 STAR-CCM+ 授权，也不绕过任何商业软件授权。请使用你本人或所在机构合法授权的 Siemens STAR-CCM+ 正版软件。

## 安装指南

第一次使用请先看这里：[`INSTALL.zh.md`](INSTALL.zh.md)

想用 Codex 对话方式跑通测试，请看：[`examples/codex_chat_test.zh.md`](examples/codex_chat_test.zh.md)

推荐安装方式：

1. 先确定安装来源：GitHub URL、本地 release ZIP，或已解压/已 clone 的本地文件夹。
2. 把 AutoStar 放到你确认的本地 skill 文件夹，例如 `C:/Users/<your-user-name>/.codex/skills/autostar`。
3. 不要默认修改全局 Python、Conda、PATH 或 STAR-CCM+ 安装目录。
4. 在安装目录运行环境检查：

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

验证通过后，新开一个 Codex 任务/窗口，或重启 Codex，让它重新扫描 `.codex/skills`。之后即可在 Codex 里对话使用 AutoStar。

如果你让 Codex 帮你安装，可以直接说：

```text
请从 https://github.com/Ouscar-ou/AutoStar 安装 AutoStar 初步版本。安装前先问我 skill 放在哪里、是否创建局部 .venv、算例输出放在哪里；不要修改全局 Python、PATH 或 STAR-CCM+ 安装目录。安装后运行 version 检查环境。
```

如果网络或权限不方便，也可以先下载 release ZIP，再把本地 ZIP 路径给 Codex。

## 效果预览

下面是一个开放水螺旋桨算例的后处理示例，展示压力云图、y+ 云图、中心剖面速度/压力和网格截面。图片仅用于展示当前预览版本的报告/后处理风格，不代表正式工程结论。

![Propeller CFD result clouds preview](docs/assets/result_clouds_preview.png)

## 这是什么

AutoStar 提供一个结构化的 STAR-CCM+ 螺旋桨开放水 CFD 工作流，帮助用户把容易出错的前处理、方向定义、短步数稳定性检查和基础报告整理成可复用流程。

当前预览版覆盖：

- STEP/STP 几何文件检查。
- 螺旋桨轴向、来流方向、旋转矢量、入口/出口语义确认。
- STAR-CCM+ 环境检查与 preflight。
- `quick` / `coarse` 网格流程验证。
- 400-step pilot 稳定性初筛。
- y+、残差、推力、扭矩和基础报告解读。
- 已有 `.sim` 的基础云图/截面图导出。
- 面向 Codex 对话使用的测试提示词：`examples/codex_chat_test.zh.md`。

它不是正式工程最终结论工具，也不是论文级 CFD 自动生成器。当前版本更适合流程验证、教学演示、方向检查、CAD/网格风险初筛。

## 当前能力

当前版本开放：

- 网格密度：`quick`、`coarse`。
- 工况流程：环境检查、STEP 粗检、preflight、mesh/solver 基础流程、400-step pilot。
- 后处理：从已有 `.sim` 导出压力/y+ 四视角、中心剖面压力/速度、网格截面和联系图。
- 报告：`preflight_report.md`、`run_report.md`、JSON 诊断文件。

当前版本不包含：

- 高密度工程网格模板。
- 正式网格无关性/GCI 自动结论。
- 批量优化、自动设计迭代或高级修复链。
- 私有 STAR-CCM+ macro/template 源码。
- Siemens STAR-CCM+ 软件或授权。

## 核心完整性与本地扩展

AutoStar `v0.3.2` 使用“核心严格、扩展开放”的完整性模型。不要修改核心文件，否则 AutoStar 会认为官方核心不再可信，并在正式命令执行前以退出码 `78` 停止：

- `bin/starccm_engine.exe`
- `starccm_cli.py`
- `public/engine_client.py`
- `AI_USAGE_POLICY.md`
- `LICENSE`

README、INSTALL、examples、普通 docs 和 `SKILL.md` 属于提示性文件。修改这些文件不会阻止运行，但 `integrity-check` 会显示本地修改 warning，来源标记会变成 `official core verified with local warnings`。不要直接修改核心文件来开发功能，也不要把修改后的包表述为未经修改的官方 Release。

所有用户扩展一定要放在以下目录中；不要把扩展脚本散放在 AutoStar 根目录、`bin/` 或 `public/`：

- `extensions/`：独立脚本、适配器、外部工具封装和集成代码。
- `workflows/`：用户自己的 Markdown/YAML/JSON 工作流定义和 agent 操作说明。
- `templates/local/`：本地 case、输入和报告模板；不要放私钥、token、商业敏感几何或 STAR-CCM+ 授权材料。

这些目录中的新增文件不参与官方核心强制哈希。AutoStar 检测到它们后继续运行，并显示 `official core + user extensions`。AutoStar 不会自动执行用户脚本；用户或 agent 必须先审查内容并获得明确执行授权。扩展不能解锁未公开网格、替换 EXE、绕过 preflight 或取消 quick/coarse 限制。

运行时检查使用：

```powershell
python ./starccm_cli.py integrity-check
python ./starccm_cli.py version
```

`tests/verify_public_preview_package.py` 用于验证官方 Release 是否原样完整，因此加入用户扩展后，该严格发布包测试会按预期报告 package mismatch；这不代表官方核心失效。

可以反馈给开发者的内容包括：安装/兼容问题、方向语义、STEP 导入、preflight、quick/coarse 网格、求解稳定性、报告和云图问题、扩展接口建议，以及可复现的文档错误。反馈时请附 `version` 和 `integrity-check` 输出、STAR-CCM+/Windows 版本、脱敏 case、关键日志及最小复现步骤；不要公开上传私有 STEP、`.sim`、许可证文件、token 或商业机密。

## 环境要求

- Windows 10/11。
- Python 3.10+。
- 本机已安装并可正常启动的 Siemens STAR-CCM+ 正版软件。
- 有效的 Siemens STAR-CCM+ license（本项目不提供）。
- STEP/STP 螺旋桨几何文件。
- 已确认的物理工况：直径 D、轴向长度 L、来流速度、转速、来流方向、旋转矢量、流体参数等。

## STAR-CCM+ 版本

当前本地验证环境：

- STAR-CCM+ `18.04.008-R8`
- Windows
- Python 3.13 本地运行环境

建议使用 STAR-CCM+ `18.04+` 同系列或更新版本测试。不同 STAR-CCM+ 大版本可能存在 Java API、宏接口、场函数名称或 GUI 场景导出差异。首次运行务必执行：

```powershell
python ./starccm_cli.py version
```

如果 STAR-CCM+ 版本不同，请先确认 `version` 输出中的 STAR-CCM+ 路径和版本；如遇兼容问题，请在 issue 中附上 `version` 输出、STAR-CCM+ 版本号和报错日志。

## 安装原则

为了避免弄乱用户电脑环境，本项目推荐局部环境、局部运行目录、显式确认路径。

安装或配置前建议先确认：

1. `skill_install_dir`：skill 安装文件夹。
2. `local_python_env_dir`：可选的局部 Python `.venv` 文件夹。
3. `case_workspace_dir`：CFD 算例和输出文件夹。

推荐布局：

```text
Skill install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Local Python environment folder:
C:/Users/<your-user-name>/Documents/autostar_env/.venv

Case workspace folder:
C:/Users/<your-user-name>/Documents/autostar_runs
```

默认不要：

- 修改全局 Python 或 Conda。
- 修改系统 PATH。
- 永久写入环境变量。
- 修改 STAR-CCM+ 安装目录。
- 默认运行 `pip install` 或升级 pip。

详细安装步骤见：`INSTALL.zh.md`。

## 快速开始

在 skill 文件夹内运行：

```powershell
python ./starccm_cli.py version
python ./tests/verify_public_preview_package.py
```

如果使用局部 `.venv`，示例：

```powershell
python -m venv C:/Users/<your-user-name>/Documents/autostar_env/.venv
& C:/Users/<your-user-name>/Documents/autostar_env/.venv/Scripts/python.exe ./starccm_cli.py version
```

复制示例 case：

```powershell
mkdir C:/runs/case1
copy ./examples/preview_quick_case.yaml C:/runs/case1/case.yaml
```

运行 preflight：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow preflight --case C:/runs/case1/case.yaml
```

只有在 preflight 可接受、方向语义清楚、用户确认本次执行后，才启动 workflow：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow run --case C:/runs/case1/case.yaml
```

## 输入模板

preflight 前请确认这些输入：

```text
STEP=你的 STEP/STP 文件路径
run_intent=screening
mesh=quick 或 coarse
D=螺旋桨直径，例如 250 mm
L=螺旋桨轴向长度，例如 53 mm
velocity=正的来流速度大小，例如 3.0 m/s
rpm=正的转速大小，例如 900 rpm
fluid=Water
density=998.2 kg/m3
dynamic viscosity=0.001003 Pa*s
turbulence=K-Omega-SST
shaft_axis=X/Y/Z
flow_direction=水实际流动方向，例如 -X
inlet_side=入口所在侧，例如 +X
outlet_side=出口所在侧，例如 -X
rotation_vector=角速度矢量方向，例如 +X
origin=[0,0,0]
prism_mode=wall_resolved
pilot=400 steps
```

YAML schema 见 `docs/case_schema.md`。

## 推荐流程

1. 运行 `version`，确认 Python、STAR-CCM+ 路径和当前开放网格。
2. 检查 STEP/STP 文件存在、单位、bbox 和明显几何风险。
3. 确认工况模板：D/L、速度、转速、流体、轴向、来流方向、旋转矢量。
4. 运行 `workflow preflight`。
5. 生成 surface/no-prism 和 prism mesh。
6. 运行 400-step pilot。
7. 读取 `run_report.md`、残差、推力/扭矩、y+ 诊断。
8. 如已有 `.sim`，可导出后处理云图。

## 方向约定

不要用一个模糊的 `axis=X` 表达所有方向。请拆开确认：

- `shaft_axis`：几何主轴是 X/Y/Z 哪一根轴。
- `flow_direction`：水实际流动方向。
- `rotation_vector`：角速度矢量方向，按右手定则。
- `velocity`：只填正的速度大小。
- `rpm`：只填正的转速大小。

示例：

```yaml
domain:
  shaft_axis: X
  hub_axis: +X

operating_condition:
  velocity: 3.0 m/s
  flow_direction: -X
  rpm: 900 rpm
  rotation_vector: +X
```

## 后处理输出

`workflow run` 或 `results extract/analyze` 成功后默认会尝试自动导出报告用云图。也可以从已有求解后的 `.sim` 手动补导：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml
```

只想检查命令是否接通、是否能解析 case 并生成宏文件时，可用 dry-run，不会启动 STAR-CCM+：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml --dry-run
```

输出目录为 `postprocess_clouds/figures`，并会生成 `postprocess_clouds/postprocess_clouds_report.md`；如果 `run_report.md` 已存在，也会追加云图索引。当前后处理目标包括：

- 螺旋桨表面压力四视角。
- 螺旋桨表面 y+ 四视角。
- 压力/y+ 合并联系图。
- 中心剖面压力/速度图。
- 网格剖面图。
- 汇总联系图。

## 发布包自检

发布前或安装后可运行：

```powershell
python ./tests/verify_public_preview_package.py
python ./tests/verify_public_preview_package.py --with-engine
```

第二条命令会调用 bundled engine，并要求本机可识别 STAR-CCM+。

## 使用边界

本仓库用于评估、演示、教学和流程验证。为保护作者权益，请遵守：

- 不得将本项目、修改版或重新打包版本作为竞争性产品销售、出租或转售。
- `quick` / `coarse` 结果主要用于初步验证和教学演示；不建议用于正式工程认证、船级社认证或论文最终结论。使用者若基于初步结果作出工程、商业或发表决策，应自行承担判断责任，作者不承担由此产生的责任。
- 公开演示、课程、视频或文章建议注明本仓库或 OSK。

完整条款见：`LICENSE` / `LICENSE.md`。

## 许可证

本项目使用自定义 Public Preview License，不是 MIT。MIT 类许可证非常宽松；当前预览版为了保护作者权益和工作流验证边界，使用更窄的授权条款。

完整条款见：`LICENSE` / `LICENSE.md`。

## Siemens / STAR-CCM+ 声明

STAR-CCM+ 是 Siemens 的商业软件和产品名称。本项目不是 Siemens 官方产品，不包含 STAR-CCM+ 软件本体，不提供 STAR-CCM+ license，不提供破解、绕过授权或替代授权服务。用户必须自行确保其 STAR-CCM+ 安装和使用符合 Siemens 许可条款。

## 反馈建议

提交 issue 时建议附上：

- `python ./starccm_cli.py version` 输出。
- STAR-CCM+ 版本。
- Windows 版本。
- `case.yaml`，可隐藏私有路径或商业敏感几何名称。
- `preflight_report.md` 或 `run_report.md`。
- 关键日志截图或错误片段。

请不要公开上传含商业机密的 STEP/STP、`.sim` 或完整工程文件。

安全漏洞、私钥暴露、凭据泄漏或非预期访问路径不要提交公开 issue，请使用 [GitHub Private Vulnerability Reporting](https://github.com/Ouscar-ou/AutoStar/security/advisories/new)。
