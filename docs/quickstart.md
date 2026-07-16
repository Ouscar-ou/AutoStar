# AutoStar Quickstart

## 1. 准备

- 安装并确认 STAR-CCM+ 可正常启动。
- 确认你有可用的 Siemens STAR-CCM+ 授权；当前预览包不提供 STAR-CCM+ 软件或授权。
- 准备 STEP/STP 螺旋桨几何。
- 复制 `examples/preview_quick_case.yaml` 到你的运行目录并改名为 `case.yaml`。

## 2. 填写 case.yaml

必须确认：

- `geometry.stp`：STEP/STP 路径。
- `geometry.diameter`：真实螺旋桨直径 D。
- `geometry.length`：轴向长度 L，可先粗估。
- `operating_condition.velocity`：正的速度大小。
- `operating_condition.flow_direction`：水实际流动方向。
- `operating_condition.rpm`：正的转速大小。
- `operating_condition.rotation_vector`：旋转矢量方向。
- `mesh.preset`：当前版本只能填 `quick` 或 `coarse`。
- `user_confirmation`：确认模板、方向语义和本次执行后才设为 `true`。

## 3. 环境检查

```powershell
python ./starccm_cli.py version
```

应看到 `Edition: public`、`Available mesh presets: quick, coarse` 和 STAR-CCM+ 可执行路径。

如果 STAR-CCM+ 路径没有被识别，请先确认 STAR-CCM+ 安装位置，再临时设置 `STARCCM_BAT` 或 `STARCCM_EXE`。不要直接运行网格或求解。

## 4. 预检

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow preflight --case C:/runs/case1/case.yaml
```

预检失败时先修复 fail 项，不要直接硬跑。

## 5. 运行 400-step pilot

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow run --case C:/runs/case1/case.yaml
```

当前 quick/coarse 结果用于流程验证和筛查。不要把 400 步结果当成最终工程结论。

## 6. 用户确认后续算

400 步完成后先阅读稳定性、残差、网格质量门控和 y+ 风险。网格质量门控为 `fail` 时应优先修网格；当前结果仅作诊断，不应直接进入长算。网格无失败门控但结果可靠性仍为 `fail` 时，只在用户确认后诊断性续算到 1500，不直接建议 2500。

没有网格质量阻塞时，用户明确确认目标总步数后，只续算缺少的步数：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow continue --case C:/runs/case1/case.yaml --to-iterations 1500 --confirmed-execution
```

`--to-iterations` 是总步数，不是追加步数。目标必须大于 `project_state.json` 中的 `solver.iterations_completed`；续算不会重新导入 STEP、建域或划网格。可先加 `--dry-run` 查看只读计划，该模式不会写文件或启动 STAR-CCM+。

如果用户已阅读网格报告并明确要求在风险网格上做诊断性长算，命令还需添加 `--confirm-mesh-risk`。该参数只表示用户接受本次诊断风险，不会把网格质量状态改成通过。

## 7. 后处理云图

顶层工作流成功后只自动导出一次云图。若已有求解后的 `.sim`，也可以手动补导：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml
```

只检查命令接线、不启动 STAR-CCM+：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml --dry-run
```

输出目录：`postprocess_clouds/figures`。主报告存在时会追加云图索引。
