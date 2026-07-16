# AutoStar Workflow

推荐顺序：

1. 环境检查：确认 Python、STAR-CCM+ 和当前包可用。
2. STEP 粗检查：确认文件存在、单位、bbox、是否明显偏心。
3. 用户确认物理参数：D/L、速度、来流方向、入口/出口、转速、旋转矢量、MRF/domain。
4. 展示当前可用网格：`quick` / `coarse`。
5. `workflow preflight`。
6. surface/no-prism 诊断。
7. prism mesh。
8. 400-step pilot。
9. 输出 `run_report.md`，用中文说明结果等级和风险。
10. 根据网格质量、稳定性和结果可靠性决定修复、停止或请求用户确认诊断性续算；不得自动进入长步数。
11. 用户确认后使用 `workflow continue --to-iterations <总步数>` 续算；不得重新执行新算例流程。
12. 如果需要，从已有 `.sim` 导出后处理云图。

## 判断原则

- 先确认不发散，再谈 y+。
- 发散后的 y+ 不用于调参。
- quick/coarse 的作用是流程验证和演示，不是 final CFD。
- 若用户只给 STEP 路径，不得自动搜索旧工程继续跑。
- `workflow run` 只用于新算例；`workflow continue` 只运行 solver、结果提取、统一 y+ 报告和总报告。
- `mesh_success=true` 只表示网格已生成，不表示网格质量通过。网格质量门控为 `fail` 时，400 步仅用于诊断，长算前必须修网格或由用户明确接受风险。
- 最大残差高于 `0.1` 且网格无失败门控时，只建议确认后诊断性续算到 1500；不得从 400 步直接建议 2500。
- 每个阶段结束后都要检查实际输出并返回文件链接：报告、JSON、`.sim`、云图索引和主要图片；后处理未运行或失败时也要说明原因并保留已生成的 CFD 诊断文件。
- `--dry-run` 是只读计划，不写项目文件、不更新授权记录、不启动 STAR-CCM+。
- 首层设计 y+ 用于估算初始网格；y+ 验收目标用于判断结果，二者必须在报告中分别显示。
- MRF 默认值按 STEP 相对 MRF 原点的正负轴包络分别解析；不要把 `1.2L` 默认均分到两侧。MRF 贴近或小于硬性安全间隙时，preflight 直接停止；只调整不足的一侧，已验证的 P1727 组合为 `mrf_forward=0.08 m`、`mrf_aft=0.075 m`。
- `MRF - Propeller` Boolean 失败或 rotating no-prism 出现 non-manifold 时，先归类为 CAD/Boolean/表面拓扑阶段问题，不要直接继续 prism 或 solver。
- 安装或配置环境前，必须先确认用户希望使用的安装文件夹、局部 `.venv` 文件夹和运行文件夹；推荐局部 `.venv`，不要默认改全局 Python、Conda、PATH 或 STAR-CCM+ 安装目录。

## Postprocess Clouds

手动命令：

```powershell
python ./starccm_cli.py --project-dir <case_dir> postprocess clouds --case <case.yaml>
python ./starccm_cli.py --project-dir <case_dir> postprocess clouds --case <case.yaml> --dry-run
```

默认输出：

- `surface_pressure_four_views_contact.png`
- `surface_yplus_four_views_contact.png`
- `surface_pressure_yplus_four_views_contact.png`
- `centerplane_focus_contact.png`
- `mesh_views_contact.png`
- `clouds_and_sections_contact.png`

截图必须完整包含螺旋桨，不得裁切桨叶或桨毂。
