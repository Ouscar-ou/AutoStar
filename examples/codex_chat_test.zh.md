# Codex 对话式测试案例

这个文件给用户一套“直接复制到 Codex 里”的测试提示词。它比手动编辑 YAML 更适合第一次验证 AutoStar。

当前公开预览包包含 `preview_quick_case.yaml` 模板，但不内置螺旋桨 STEP/STP 几何文件。真实 CFD 测试需要用户提供自己的 STEP/STP 文件，以及直径、转速、来流方向等物理工况。

## 测试 1：安装后冒烟检查

用途：确认 AutoStar 被正确安装、Python 能运行、STAR-CCM+ 能被识别、当前开放网格为 `quick/coarse`。

复制给 Codex：

```text
使用 AutoStar 做安装后冒烟检查。

AutoStar 安装目录是：
C:/Users/<your-user-name>/.codex/skills/autostar

请只做以下事情：
1. 进入安装目录。
2. 运行 python ./starccm_cli.py version。
3. 运行 python ./tests/verify_public_preview_package.py。
4. 总结 Edition、可用 mesh presets、STAR-CCM+ 路径/版本、验证是否通过。

不要创建 CFD case，不要网格，不要求解，不要修改全局 Python、PATH 或 STAR-CCM+ 安装目录。
```

通过标准：

- `Edition: public`
- `Available mesh presets: quick, coarse`
- 验证脚本输出 `OK: public-preview release package checks passed`

## 测试 2：用自己的 STEP 做 quick 预检

用途：用对话方式让 Codex 生成测试 case，并先跑 preflight，不直接求解。

把下面的 `STEP`、`D`、`L`、速度、转速、方向改成你的实际值后复制给 Codex：

```text
使用 AutoStar，用我的 STEP 做一个 quick 预览测试，只先跑 preflight。

AutoStar 安装目录：
C:/Users/<your-user-name>/.codex/skills/autostar

算例输出目录：
C:/Users/<your-user-name>/Documents/autostar_runs/my_first_case

几何文件 STEP：
C:/path/to/your_propeller.stp

工况：
run_intent=smoke_test
mesh=quick
D=250 mm
L=53 mm
velocity=3.0 m/s
rpm=900 rpm
fluid=Water
density=998.2 kg/m3
dynamic viscosity=0.001003 Pa*s
turbulence=K-Omega-SST
shaft_axis=X
flow_direction=-X
inlet_side=+X
outlet_side=-X
rotation_vector=+X
origin=[0,0,0]
prism_mode=robust
pilot=400 steps

请按顺序做：
1. 先检查 STEP 文件是否存在。
2. 复制 examples/preview_quick_case.yaml 到算例目录并改成我的参数。
3. 运行 version。
4. 运行 workflow preflight。
5. 如果 preflight 通过或只有可接受警告，先停下来总结，不要自动网格或求解。
```

通过标准：

- Codex 能生成 `case.yaml`。
- `workflow preflight` 能完成。
- 方向语义清楚：`shaft_axis`、`flow_direction`、`inlet_side`、`outlet_side`、`rotation_vector` 没有互相矛盾。
- Codex 没有在未确认前启动网格或求解。

## 测试 3：400-step pilot

用途：在测试 2 的 preflight 可接受后，继续做公开预览版的短步数流程验证。

复制给 Codex：

```text
继续使用 AutoStar 对刚才的 case 做 quick 400-step pilot。

要求：
1. 使用现有 case.yaml。
2. 不修改全局 Python、PATH 或 STAR-CCM+ 安装目录。
3. 不切换到未开放或更高密度网格；当前公开预览只用 quick/coarse。
4. 运行 workflow run，最多 400 steps。
5. 完成后读取 run_report.md、results、y+ 或稳定性诊断。
6. 总结是否 non-divergent、推力/扭矩是否有限、y+ 是否有效、是否适合作为初步流程验证。
```

注意：400-step pilot 只用于流程验证和初步筛查，不代表正式工程结论。

## 测试 4：确认后安全续算

用途：验证 AutoStar 只追加缺少的求解步数，不重新导入、建域或划网格。

复制给 Codex：

```text
继续使用 AutoStar，把刚才已完成 400 步的算例续算到总计 1000 步。

要求：
1. 先读取 project_state.json 中的 solver.iterations_completed。
2. 先读取网格质量门控、稳定性和结果可靠性；若网格存在风险，解释后停下来让我确认，不要默认添加 --confirm-mesh-risk。
3. 使用 workflow continue --to-iterations 1000，不要重新运行 workflow run。
4. 先用 --dry-run 展示只读计划；计划中不得出现 geometry run、domain create 或 mesh generate。
5. dry-run 后先停下来汇报，得到我确认后再移除 --dry-run 正式续算。
6. 正式续算完成后更新结果、统一 y+ 报告、总报告和一套云图。
```

`--to-iterations` 表示目标总步数。若当前已经达到或超过目标，AutoStar 应拒绝启动 STAR-CCM+。

## 常见卡点

- 如果 Codex 当前任务刚安装完 AutoStar 但识别不到 skill：新开一个 Codex 任务/窗口，或重启 Codex，让它重新扫描 `.codex/skills`。
- 如果安装目录变成 `autostar/AutoStar/SKILL.md`：目录层级错了，应改成 `autostar/SKILL.md`。
- 如果没有 STEP/STP：只能做测试 1，不能跑真实 CFD case。
- 如果 STAR-CCM+ 路径未识别：先确认本机 STAR-CCM+ 安装位置，再按 `INSTALL.zh.md` 中的方式设置当前 PowerShell 会话变量。
