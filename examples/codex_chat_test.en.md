# Codex Chat-Based Test Case

This file gives users copy-and-paste prompts for testing AutoStar through Codex chat. It is easier for first-time validation than manually editing YAML.

The public preview includes the editable `preview_quick_case.yaml` template, but it does not bundle a propeller STEP/STP geometry file. A real CFD test requires the user's own STEP/STP geometry and confirmed physical conditions.

## Test 1: Post-Install Smoke Check

Purpose: confirm that AutoStar is installed correctly, Python runs, STAR-CCM+ is detected, and the available mesh presets are `quick/coarse`.

Copy this into Codex:

```text
Use AutoStar for a post-install smoke check.

AutoStar install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Only do the following:
1. Enter the install folder.
2. Run python ./starccm_cli.py version.
3. Run python ./tests/verify_public_preview_package.py.
4. Summarize Edition, available mesh presets, STAR-CCM+ path/version, and whether verification passed.

Do not create a CFD case, do not mesh, do not solve, and do not modify global Python, PATH, or the STAR-CCM+ installation directory.
```

Expected pass signals:

- `Edition: public`
- `Available mesh presets: quick, coarse`
- `OSK activation: not required for this preview edition`
- `OK: public-preview release package checks passed`

## Test 2: Quick Preflight With Your Own STEP

Purpose: let Codex create a test case through chat and run preflight only.

Replace `STEP`, `D`, `L`, speed, rpm, and directions with your real values, then copy this into Codex:

```text
Use AutoStar with my STEP file for a quick preview test. Only run preflight first.

AutoStar install folder:
C:/Users/<your-user-name>/.codex/skills/autostar

Case output folder:
C:/Users/<your-user-name>/Documents/autostar_runs/my_first_case

Geometry STEP:
C:/path/to/your_propeller.stp

Conditions:
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

Please do this in order:
1. Check whether the STEP file exists.
2. Copy examples/preview_quick_case.yaml into the case folder and update it with my parameters.
3. Run version.
4. Run workflow preflight.
5. If preflight passes or only has acceptable warnings, stop and summarize. Do not automatically mesh or solve.
```

Expected pass signals:

- Codex creates `case.yaml`.
- `workflow preflight` completes.
- Direction semantics are clear: `shaft_axis`, `flow_direction`, `inlet_side`, `outlet_side`, and `rotation_vector` do not conflict.
- Codex does not start meshing or solving without confirmation.

## Test 3: 400-Step Pilot

Purpose: after Test 2 preflight is acceptable, run the public-preview short workflow validation.

Copy this into Codex:

```text
Continue with AutoStar and run a quick 400-step pilot for the existing case.

Requirements:
1. Use the existing case.yaml.
2. Do not modify global Python, PATH, or the STAR-CCM+ installation directory.
3. Do not switch to unavailable or higher-density meshes; the current public preview only uses quick/coarse.
4. Run workflow run, maximum 400 steps.
5. After completion, read run_report.md, results, y+, or stability diagnostics.
6. Summarize whether it is non-divergent, whether thrust/torque are finite, whether y+ is valid, and whether it is suitable as preliminary workflow validation.
```

Note: a 400-step pilot is for workflow validation and preliminary screening only. It is not a formal engineering conclusion.

## Common Pitfalls

- If Codex cannot see AutoStar right after installation: open a new Codex task/window, or restart Codex, so it can rescan `.codex/skills`.
- If the install folder becomes `autostar/AutoStar/SKILL.md`: the folder is nested incorrectly. It should be `autostar/SKILL.md`.
- If you do not have a STEP/STP file: you can only run Test 1, not a real CFD case.
- If STAR-CCM+ is not detected: confirm the local STAR-CCM+ installation path, then set the current PowerShell session variable as described in `INSTALL.md`.
