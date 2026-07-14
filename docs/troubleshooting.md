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

## Postprocess images are cropped

The current exporter uses safe framing. If a special geometry is still cropped, rerun postprocess after confirming `domain.shaft_axis` / `domain.hub_axis` and report the generated image.
