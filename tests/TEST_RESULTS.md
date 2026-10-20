# Physics test run

Command (PowerShell):

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python tests\test_physics.py
```

Result: passed (exit code 0).

```text
=== DELIVERABLE 1 VERIFICATION ===
[EM Module]  Joule dT: 0.32 °C | MTTF: 1.24 Years
[Fatigue]   Plastic Strain: 1.5290 | Cycles to Failure: 44 cycles
[SI Module]  Pitch 40 µm -> R:   0.81 mΩ | C:  1.08 fF | Delay: 0.30 ps
[SI Module]  Pitch 20 µm -> R:   3.25 mΩ | C:  1.08 fF | Delay: 0.30 ps
[SI Module]  Pitch 10 µm -> R:  12.99 mΩ | C:  1.08 fF | Delay: 0.30 ps
==================================
```
