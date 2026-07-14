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

## 6. 后处理云图

`workflow run` 或 `results extract/analyze` 成功后默认会尝试自动导出云图。若已有求解后的 `.sim`，也可以手动补导：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml
```

只检查命令接线、不启动 STAR-CCM+：

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 postprocess clouds --case C:/runs/case1/case.yaml --dry-run
```

输出目录：`postprocess_clouds/figures`。主报告存在时会追加云图索引。
