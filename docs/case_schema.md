# AutoStar Case Schema

当前初步版本用于 STAR-CCM+ 螺旋桨 CFD 流程验证，只开放 `quick` 和 `coarse` 两档网格。

## Required Fields

- `run_intent`: 推荐 `smoke_test` 或 `screening`。
- `project.name`: 项目名。
- `project.sim_name`: 输出 `.sim` 文件名。
- `geometry.stp`: STEP/STP 文件路径。
- `geometry.diameter`: 螺旋桨真实直径，例如 `250 mm`。
- `geometry.length`: 螺旋桨轴向长度，例如 `53 mm`。
- `operating_condition.velocity`: 正的速度大小，例如 `3.0 m/s`。
- `operating_condition.flow_direction`: 水实际流动方向，例如 `-X` 或 `[-1,0,0]`。
- `operating_condition.rpm`: 正的转速大小，例如 `900 rpm`。
- `operating_condition.rotation_vector`: 角速度矢量方向，例如 `+X`。
- `operating_condition.handedness`: 当前预检要求填写 `right` 或 `left`，用于复核，不替代 `rotation_vector`。
- `domain.shaft_axis`: 几何轴线，例如 `X`。
- `domain.hub_axis`: 桨毂/导流体朝向，选填，用于报告和人工复核。
- `domain.mrf_origin`: MRF 原点。
- `domain.upstream/downstream`: 入口侧/出口侧外域距离，会根据 `flow_direction` 映射到实际几何侧。
- `domain.mrf_forward/mrf_aft`: 当前 case 字段；请按入口/出口方向复核其几何侧。
- `mesh.preset`: `quick` 或 `coarse`。

## Recommended Defaults

- `fluid`: `Water`。
- `density`: `998.2` kg/m3。
- `viscosity`: `0.001003` Pa*s。
- `turbulence`: `K-Omega-SST`。
- `mesh.prism_mode`: `robust` for quick checks; use `wall_resolved` only when you understand y+ implications.
- `solver.pilot_iterations`: `400`。

## Notes

- STEP bbox 只能作为粗检参考，不能替代用户确认的 D/L、轴线和中心。
- 400-step pilot 用于检查明显发散、方向错误、网格/边界层风险，不是最终结果。
- 发散后的 y+ 无效，不能用来调 first layer height。
- 直接使用 CLI 时，`user_confirmation` 是“用户已确认模板/方向/执行”的审计记录；只有确认后才应设为 `true`。
