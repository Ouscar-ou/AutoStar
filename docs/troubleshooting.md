# Troubleshooting

## Preflight says only quick/coarse are available

This is expected in the current public preview. Use:

```yaml
mesh:
  preset: quick
```

or:

```yaml
mesh:
  preset: coarse
```

## STAR-CCM+ path is not found

Confirm the STAR-CCM+ install path with the user first. Then set the launcher path for the current PowerShell session:

```powershell
$env:STARCCM_BAT="C:/Program Files/Siemens/<version>/STAR-CCM+<version>/star/bin/starccm+.bat"
python ./starccm_cli.py version
```

Do not start meshing or solving until `version` shows the correct STAR-CCM+ executable. Do not set permanent environment variables unless the user explicitly wants that.

## STEP imports but body name is unexpected

Some STEP files import into STAR-CCM+ with CAD body names such as `brep_1` instead of `Propeller`. The workflow attempts to normalize imported CAD bodies during domain creation. If geometry still fails, open the STEP in CAD/STAR-CCM+ and confirm that the propeller is a valid solid/surface body.

## Axis or direction looks wrong

Do not use a single ambiguous `axis=X` to describe everything. Confirm separately:

- `domain.shaft_axis`: geometric shaft axis.
- `operating_condition.flow_direction`: actual water flow direction.
- `operating_condition.rotation_vector`: angular velocity vector direction.

## STAR connection reset

If STAR-CCM+ connection resets but residuals and force/torque did not physically explode, retry with fewer parallel cores, such as `np=8`, `np=4`, or `np=2`.

## y+ is invalid

If the solver diverged, y+ is invalid. Do not use diverged y+ values to resize first-layer height.

`prism_design_yplus` is the first-layer design input. `yplus_acceptance_target` is the solved-result acceptance target. They may differ, but the report must show both and produce one canonical assessment in `yplus_report.json`.

## Continue an existing solved case

Do not run `workflow run` again. Use an absolute target:

```powershell
python ./starccm_cli.py --project-dir C:/runs/case1 workflow continue --case C:/runs/case1/case.yaml --to-iterations 1500 --confirmed-execution
```

Add `--dry-run` first when you want to inspect the plan. A continuation plan must not contain geometry import, domain creation, or mesh generation.

If AutoStar reports a `fail` or `review` mesh-quality gate, repair the mesh before a long run. A 400-step pilot may remain useful for diagnosis, but `mesh_success=true` only means mesh generation completed. If the user deliberately accepts the risk for diagnostic continuation, add `--confirm-mesh-risk`; this does not convert the mesh-quality gate to pass.

If mesh quality is not blocking but result reliability still fails or the maximum residual exceeds `0.1`, continue only after user confirmation and use 1500 as the next diagnostic target. Do not recommend jumping directly from 400 to 2500.

## Postprocess images are cropped

The current exporter uses safe framing. If a special geometry is still cropped, rerun postprocess after confirming `domain.shaft_axis` / `domain.hub_axis` and report the generated image.
## MRF Boolean or surface topology failure

If `MRF - Propeller` reports a Parasolid entity error, or the rotating no-prism mesh reports a non-manifold surface, first inspect the side-specific MRF clearance. Do not increase both axial sides by default: change only the side identified by preflight, then retry in a fresh case directory. A passing raw envelope estimate does not replace the STAR-CCM+ Boolean and no-prism checks.
