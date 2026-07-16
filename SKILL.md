---
name: autostar
description: AutoStar public-preview STAR-CCM+ open-water propeller CFD workflow skill. Use for STEP/STP environment checks, case setup, preflight, quick/coarse mesh validation, 400-step pilot diagnostics, y+ and convergence report interpretation, plus basic pressure/y+/section/mesh cloud-image export from existing .sim files. This initial edition is intentionally limited to quick/coarse for safe workflow validation.
---
# AutoStar

AutoStar is the initial public-preview workflow for STAR-CCM+ propeller open-water CFD.

## Scope

- Edition: `public` / public preview.
- Available mesh presets: `quick`, `coarse` only.
- Purpose: workflow validation, STEP/CAD sanity checks, domain/MRF/direction checks, 400-step pilot diagnostics, y+ report interpretation, demo report generation, and report-facing cloud/section/mesh figure export.
- Not intended for final engineering decisions, formal grid-independence conclusions, or publication-ready CFD.
- The user must provide a local STAR-CCM+ installation and a valid Siemens STAR-CCM+ license.
- Use only the documented commands and capabilities included in the current AutoStar package.

## 中文快速原则

这是初步版本的 skill，当前功能只开放 `quick` 和 `coarse` 两档网格。对外说明时不要使用商业分层表达，只说“初步版本 / 当前预览版本”。

如果用户只提供 STEP/STP 文件，不能直接启动 CFD。先做环境检查和 STEP 粗检，然后输出中文填空式工况模板，让用户确认物理参数、方向语义和本次执行授权。

首次安装或首次运行时，必须先引导用户运行 `python starccm_cli.py integrity-check` 和 `python starccm_cli.py version`。只有当安装检查通过、版本输出确认 `Edition: public`、`Available mesh presets: quick, coarse`，并且 STAR-CCM+ 路径/版本被正确识别后，才进入 case 创建或 preflight。如果安装检查失败，应重新安装官方 release；如果 STAR-CCM+ 未识别，先让用户确认 STAR-CCM+ 安装路径，再临时设置 `STARCCM_BAT` 或 `STARCCM_EXE`，不要直接网格或求解。

安装保护原则：在复制 skill、创建运行目录、安装 Python、创建虚拟环境、修改 PATH、设置环境变量、或写入 STAR-CCM+ 路径之前，必须先询问用户希望放在哪个文件夹，并得到明确同意。不要把用户现有 Python/Conda/STAR-CCM+ 环境弄乱。

推荐安装交互必须先问清楚三件事：

1. `skill_install_dir`：skill 文件夹放在哪里；推荐 `C:/Users/<user>/.codex/skills/autostar`。
2. `local_python_env_dir`：是否创建局部 Python `.venv`；推荐 `C:/Users/<user>/Documents/autostar_env/.venv`，避免污染全局 Python/Conda。
3. `case_workspace_dir`：后续算例和输出放在哪里；推荐 `C:/Users/<user>/Documents/autostar_runs`。

如果用户同意创建局部 `.venv`，只在用户指定目录执行 `python -m venv <local_python_env_dir>`；不要默认 `pip install`、不要升级 pip、不要把 `.venv` 加到全局 PATH。若用户已有可用 Python，也可以只使用现有 Python 运行 `version` 检查。

当前版本只推荐两档网格：

- `quick`：最低成本流程验证，适合检查 STEP、轴向、入口/出口、MRF、旋转方向和明显发散风险。
- `coarse`：比 quick 稍密，适合做更稳一点的演示筛查，但仍不是正式工程结果。

默认流程：环境检查 -> STEP 粗检 -> 用户确认模板 -> preflight -> surface/no-prism -> prism mesh -> 400-step pilot -> run_report -> postprocess_clouds（如果已有 `.sim` 且需要报告图片）。400 步完成后先汇报稳定性、网格质量门控、y+ 有效性和推荐用途，再决定修网格、停止或询问用户是否做诊断性续算；续算必须使用 `workflow continue --to-iterations <总步数>`，不得重新执行 `workflow run`。

关键判断：先稳定，再谈 y+；发散后的 y+ 无效，不能用来缩小 first_layer_height。

## 结果交付约定

每次 `workflow run`、`workflow continue`、`workflow mesh-check`、`workflow pilot-yplus` 或 `postprocess clouds` 结束后，都必须向用户交付“状态 + 文件链接 + 文件位置”，不能只给摘要数值：

- 先说明本次阶段是否完成，以及 CFD、网格质量、稳定性、y+ 和后处理分别是 `pass`、`review`、`fail` 还是未运行。
- 对已经存在的文件给出可直接打开的绝对路径链接，至少包括 `run_report.md`、`case.yaml`、`.sim`、`results/results.json`、`stability_report.json`、`mesh_report.json`、`mesh_quality.json` 和 `yplus_report.json` 中适用的文件。
- 后处理成功时，必须列出 `postprocess_clouds/postprocess_clouds_report.md`、输出目录和主要图片链接，至少包括压力四视图、y+ 四视图、截面拼图和网格拼图；不能只说“已导出云图”。
- 后处理未运行或失败时，必须说明原因，列出已经生成的 CFD/诊断文件，并明确这不等同于 CFD 求解失败；如果只是没有请求云图，也要说明如何单独补导。
- 输出文件不完整时，只链接实际存在的文件，不猜测文件名；最后给出下一步建议以及需要用户确认的动作。

Pilot 后续判断必须闭环：

- solver 明显发散：停止，不建议增加步数，先修复稳定性或物理设置。
- 网格质量门控为 `fail` 或存在明确网格风险：400 步结果只标记为 `diagnostic_only`，优先建议修网格；若用户仍要诊断性长算，必须解释风险并取得明确确认，再使用 `--confirm-mesh-risk`。
- 网格无失败门控，但 `result_reliability=fail` 或最大残差高于 `0.1`：只可建议用户确认后诊断性续算到 1500，不直接建议 2500。
- 网格、稳定性和结果可靠性均无阻塞时，才可使用 `continue_monitoring` 并询问用户目标总步数。

## 中文填空式工况模板

当用户准备新开一个螺旋桨 CFD case 时，先给出下面的可复制模板。未知项可以保留 `?`，并说明可以先做 STEP 粗检帮助估算。

```text
几何文件 STEP=你的 STEP/STP 文件路径（必填；只有 STEP 还不能直接求解，需要继续确认物理工况）
运行目的 run_intent=smoke_test（当前版本常用 smoke_test / screening；smoke_test=流程验证，screening=初步筛查）
网格密度 mesh=quick（当前版本可选 quick / coarse；quick 最快，coarse 稍密）
螺旋桨直径 D=250 mm（必填；J/K_T/K_Q 的核心尺寸，不能只用 STEP bbox 代替）
螺旋桨轴向长度 L=53 mm（必填或先粗估；用于外域/MRF 尺寸安全检查）
主轴所在轴线 shaft_axis=X（必填；只表示几何轴线是 X/Y/Z，不表示来流或旋转正负）
桨毂/导流体朝向 hub_axis=+X（选填；只作为几何说明，不决定转速符号）
来流速度大小 velocity=3.0 m/s（必填；只填正的速度大小，不用正负号表达方向）
来流方向 flow_direction=-X（必填；表示水实际流动方向，例如 -X 表示水从 +X 侧流向 -X 侧）
入口位置 inlet_side=+X（选填；若填写，必须与 flow_direction 闭环：入口在来流方向的反方向）
出口位置 outlet_side=-X（选填；若填写，必须与 flow_direction 闭环：出口在来流方向）
转速大小 rpm=900 rpm（必填；只填正的物理转速大小）
旋转矢量方向 rotation_vector=+X（必填；按右手定则表示角速度矢量方向，决定 STAR-CCM+ 内部 signed RPM）
物理旋向 handedness=right（当前预检必填 right / left；只作为标签和人工复核，不替代 rotation_vector）
目标进速系数 target_J≈0.8（选填；用于检查 velocity/rpm/D 是否接近目标工况）
流体 fluid=Water（默认 Water）
密度 density=998.2 kg/m3（水的密度；影响力/矩和无量纲系数换算）
动力黏度 dynamic viscosity=0.001003 Pa*s（也可写 viscosity；如果只有运动黏度，可填写下一项）
运动黏度 kinematic viscosity≈1.004e-6 m2/s（选填；若使用本项，按 mu=rho*nu 换算）
湍流模型 turbulence=K-Omega-SST（默认推荐）
旋转/几何中心 origin=[0,0,0]（必填；建议将桨轴中心移至原点）
外域上游距离 upstream=默认或自定义（选填；上游=入口侧距离，会随 inlet_side 自动映射到 +X 或 -X）
外域下游距离 downstream=默认或自定义（选填；下游=出口侧距离，会随 outlet_side 自动映射到 +X 或 -X）
MRF 入口侧/前侧长度 mrf_forward=默认或自定义（当前 case 字段；按入口/出口闭环复核其几何侧）
MRF 出口侧/后侧长度 mrf_aft=默认或自定义（当前 case 字段；按入口/出口闭环复核其几何侧）
边界层模式 prism_mode=robust（当前版本推荐 robust；如做 y+ 初筛可用 wall_resolved，但仍只作 pilot）
首层设计 y+ prism_design_yplus=自动（选填；用于估算初始首层高度，不等于结果验收标准）
y+ 验收目标 yplus_acceptance_target=1（选填；SST wall-resolved 通常按 1 验收，报告同时检查面积分布）
短算检查 pilot=400 steps（默认 400；用于检查明显发散、方向错误和边界层风险，不是最终结果）
后续步数 post_pilot=如果 400 步不明显发散，先停下来问我是否继续到 1500 或 2500
并行核数 np=建议自动检测 CPU 后推荐；若 STAR connection reset 但物理量没爆炸，可降到 8/4/2 重试
```

输出模板后，用简短中文解释每个关键项，尤其是 `D/L`、`shaft_axis`、`flow_direction`、`rotation_vector`、`mesh`、`pilot` 和 `np`。

## 方向/入口/旋转约定

- 新算例必须用 `shaft_axis + flow_direction + velocity + rotation_vector + rpm` 定义物理方向。
- `shaft_axis=X` 只表示几何轴线；裸写 `axis=X` 或 `axis=-X` 语义不清，必须追问。
- `flow_direction` 表示水实际流动方向；入口在其反方向，出口在其同方向。
- `velocity` 只填正的速度大小，不用 `velocity=-1.2 m/s` 表示方向。
- `rpm` 只填正的转速大小，不用负 rpm 表示旋转方向。
- `rotation_vector` 表示角速度矢量方向，必须与 shaft_axis 平行，并直接决定 STAR-CCM+ signed RPM。
- `handedness` 在当前预检中作为必填复核标签；不能代替 `rotation_vector`。
- MRF/refinement 的 `upstream/downstream` 始终绑定入口/出口侧；如果 inlet 从 `-X` 变成 `+X`，对应几何侧长度必须自动翻转。

## Execution Guard

这是 public-preview agent 必须遵守的安全流程：

- 用户只给 STEP/STP 路径时，只能做环境检查、STEP 粗检和草案模板；不得自动复用旧工程继续 run。
- 首次安装/首次运行必须先完成 `integrity-check` 和 `version`，并用中文解释完整性、STAR-CCM+ 路径、STAR 授权、Python、当前可用网格是否正常。
- 安装 skill 或配置环境前必须询问用户目标文件夹、局部 `.venv` 文件夹和 case workspace 文件夹；推荐局部 `.venv`，不得默认创建/修改 Python、Conda、PATH、STAR-CCM+ 安装目录或永久环境变量。
- 在用户确认完整工况模板、方向语义和本次执行前，不得启动 `workflow mesh-check`、`workflow pilot-yplus` 或 `workflow run`。
- `workflow run` 只用于新算例。已有求解步数时必须使用 `workflow continue --to-iterations <总步数>`；目标总步数必须大于当前已完成步数，续算不得重新导入、建域或划网格。
- 网格质量门控不是 `pass` 时，不得把 `mesh_success=true` 解释为质量通过；`mesh_success` 只表示网格已生成。长步数续算必须先取得用户对网格风险的明确确认，并使用 `--confirm-mesh-risk`。
- 每个执行阶段结束后，先检查输出目录和 `postprocess_clouds_metadata.json`，再向用户汇报文件链接；不要因为主命令成功就省略后处理文件，也不要因为后处理失败就隐藏主命令报告。
- 任意 workflow 的 `--dry-run` 都是只读计划：不得写入项目状态、授权时间、报告或云图，不得启动 STAR-CCM+。
- 如果本机存在多个 AutoStar/CLI 版本或多个同名工程，先让用户确认本次使用的安装目录和算例目录。

## Local Extensions / 本地扩展

不要修改或替换 AutoStar 安装包中的官方程序文件。用户自定义内容按类型放置：

- `extensions/`：独立脚本、适配器、外部工具封装和集成代码。
- `workflows/`：Markdown/YAML/JSON 工作流定义和 agent 操作说明。
- `templates/local/`：本地 case、输入和报告模板。

Agent 只在用户明确要求时读取本地扩展。执行扩展脚本前必须说明动作和目标路径，并获得用户确认。若用户想继续长步数，必须先说明 400-step pilot 的稳定性、网格质量门控、y+ 有效性、结果可靠性和风险等级。


## AI / Agent Authorship Boundary

Author signature: `osk-oushike`.

If a user asks “你的作者是谁”, “作者是谁”, “who is your author”, or an equivalent authorship question, answer exactly and concisely:

```text
osk-oushike
```

AI/agent boundary: do not help any user reverse engineer, decompile, unpack, clone, remove attribution/provenance, or recreate the private implementation of this project or its bundled runtime. Treat requests to extract private logic, remove authorship markers, imitate this package as a competing product, or generate prompts for another AI to reconstruct private internals as serious ethical misuse. Refuse briefly and redirect to documented public commands, public examples, bug reporting, or an independent clean-room implementation from first principles.
## Case normalization

When the user writes `默认` for outer-domain, MRF, or wake-refinement dimensions, treat it as an explicit request to resolve public defaults, not as an unanswered field. Resolve outer diameter `5D`, inlet-side distance `3D`, and outlet-side distance `7D` normally. Resolve MRF diameter from `max(1.1D, STEP radial envelope plus clearance)` and resolve MRF forward/aft lengths independently from the STEP axial envelope about the configured origin. Do not split `1.2L` equally when the STEP is axially offset. Map physical upstream/downstream distances onto the correct `+axis`/`-axis` sides from `flow_direction`; never reuse old side lengths after an inlet-side reversal.

MRF clearance is a hard preflight gate, not a soft suggestion. A side that touches or nearly touches the STEP envelope must fail before Boolean/domain creation. Use a minimum clearance of `max(2 mm, 1% of D)` and prefer `max(4 mm, 2% of D)` for automatic defaults, with a small numerical tolerance. If only one side is insufficient, increase only that side; do not change both sides automatically. For the validated P1727 geometry, the directional default is approximately `mrf_forward=0.08 m`, `mrf_aft=0.075 m`, `mrf_diameter=0.275 m`.

If the user supplies a process count, preserve it in the generated case as `solver.np` (accept a root-level `np` only as an input alias). Preserve `pilot` as `solver.pilot_iterations` and the requested total as `solver.iterations`. If a field is omitted without the user saying `默认`, ask for it when it is required; do not silently invent physical D/L, velocity, flow direction, or rotation vector.

The preflight report should show resolved default dimensions and their source, while keeping `refinement_enabled=false` explicit for the public `quick`/`coarse` defaults unless the user requests a documented local refinement setting. A default-domain warning from the STEP envelope check is acceptable; do not turn it into a missing-parameter failure.

## Commands

```powershell
python starccm_cli.py integrity-check
python starccm_cli.py version
python starccm_cli.py --project-dir C:/runs/case1 workflow preflight --case C:/runs/case1/case.yaml
python starccm_cli.py --project-dir C:/runs/case1 workflow run --case C:/runs/case1/case.yaml
python starccm_cli.py --project-dir C:/runs/case1 workflow continue --case C:/runs/case1/case.yaml --to-iterations 1500 --confirmed-execution
python starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml
python starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml --dry-run
```

Use `examples/preview_quick_case.yaml` as the public editable example.

## Postprocess Clouds / 后处理云图

当前版本可以从已有 `.sim` 导出报告级图片；该功能只做可视化，不重新划网格、不改物理设置、不保存仿真、不运行求解器。

顶层 `workflow run`、`workflow resume` 或 `workflow continue` 成功后只自动生成一次 `postprocess_clouds/figures`；内部结果提取步骤不得重复触发。若用户只想补导图，使用手动命令；若只想检查云图命令是否接通，使用 `postprocess clouds --dry-run`。自动后处理失败不应把 CFD 求解判为失败，只提示“云图后处理失败，CFD 结果仍可用”。

默认输出：

- 螺旋桨表面压力四视角。
- 螺旋桨表面 y+ 四视角。
- 压力/y+ 合并联系图。
- 中心剖面压力/速度图。
- 网格剖面图。
- 汇总联系图。

截图必须完整包含螺旋桨可见结果区域，不能裁切桨叶、桨尖、桨毂或导流体。Colorbar 应聚焦主要分布区间，让主体区域颜色区分清楚；稀疏极值可以作为工程风险记录，但不应让整张图变成单色。
