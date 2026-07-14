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
10. 如果需要，从已有 `.sim` 导出后处理云图。

## 判断原则

- 先确认不发散，再谈 y+。
- 发散后的 y+ 不用于调参。
- quick/coarse 的作用是流程验证和演示，不是 final CFD。
- 若用户只给 STEP 路径，不得自动搜索旧工程继续跑。
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
