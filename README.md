# Multiphysics_interconnect
Multiphysics_interconnect/
├── src/
│   ├── engine/
│   │   ├── __init__.py
│   │   └── physics.py         <-- Deliverable 1: Core Physics Equations
│   ├── sweeps/                <-- Deliverable 2: Parameter Sweeps & SOA
│   └── visualization/         <-- Deliverable 2/3: Heatmaps & Plots
├── tests/
│   └── test_physics.py        <-- Unit tests
├── README.md
└── requirements.txt

The motivation:
Modern AI hardware accelerators are constrained less by monolithic transistor scaling and far more by 2.5D/3D packaging limits-specifically thermo-mechanical reliability, electromigration limits in sub-20 micrometer pitch microbumps, and high-density TSV signal degradation.
The tradeoff is that packing many fine microbumps and Cu-filled TSVs into a small region concentrates current and heat. Copper, silicon, underfill, and dielectric materials expand by different amounts during temperature changes, creating stress; EM, voiding, fatigue cracks, and warpage then become key reliability concerns
Governing equations:
1.Electromigration Kinetics & Self-Heating (Black's Law)
2.Thermo-Mechanical Stress & Fatigue (Coffin-Manson)
3.Signal Integrity & Interconnect Delay (RC)

1.Package initializer (src/engine/__init__.py)
The purpose of __init__.py is to expose a clean public API so users (and your downstream sweep scripts) can import functions directly from src.engine without navigating nested module paths.

2.Physics Module with 6 governing functions:

3.Sweeps and plots
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│ Panel 1: EM SOA         │ Panel 2: Fatigue SOA    │ Panel 3: Pitch Scaling  │
│ Contour: log10(MTTF)    │ Contour: log10(N_f)     │ Twin Axis Plot:         │
│ Overlay: 10-Yr Target   │ Overlay: 3000 Cycles    │ R (mΩ) vs Delay (ps)    │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘



### 1. The Electromigration "Joule Heating Cliff" ($J > 10^5\,\text{A/cm}^2$)

The drop in the 10-year ambient temperature boundary (from $70^\circ\text{C}$ down to $20^\circ\text{C}$) is caused by **super-linear Joule self-heating**.

* Black’s Law depends on both current density $J$ and effective temperature $T_{\text{eff}}$:

$$\text{MTTF} \propto J^{-n} \exp\left(\frac{E_a}{k_B T_{\text{eff}}}\right)$$


* $T_{\text{eff}} = T_{\text{ambient}} + \Delta T_{\text{Joule}}$, where $\Delta T_{\text{Joule}} \propto J^2 \cdot \rho_0 \cdot h_{\text{bump}} \cdot R_{\text{th,eff}}$.
* Below $10^5\,\text{A/cm}^2$, self-heating is negligible ($\Delta T < 1^\circ\text{C}$).
* Once $J$ reaches $10^6\,\text{A/cm}^2$, $J^2$ scales by $100\times$, driving local self-heating up by tens of degrees. To keep total $T_{\text{eff}}$ low enough to hit a 10-year target, the allowable substrate ambient temperature ($T_{\text{ambient}}$) must drop sharply.

---

### 2. Low-Cycle Fatigue Drop ($N_f \sim 10\text{ cycles}$)

At large die radii ($\text{DNP} > 15\,\text{mm}$) and high thermal swings ($\Delta T > 100^\circ\text{C}$), $N_f$ dropping to single/double digits indicates **extreme plastic shear deformation**.

* Engineering shear strain scales linearly with DNP:

$$\gamma_{\text{shear}} = \frac{\text{DNP}}{h_{\text{bump}}} \cdot \Delta \alpha \cdot \Delta T$$


* For a $30\,\text{mm} \times 30\,\text{mm}$ AI accelerator die ($\text{DNP} \approx 21\,\text{mm}$) with a microbump height $h_{\text{bump}} = 15\,\mu\text{m}$, $\gamma_{\text{shear}}$ exceeds $1.5$ ($150\%$ plastic strain).
* Coffin-Manson dictates that fatigue life drops exponentially with strain: $N_f \propto (\Delta \varepsilon_p)^{-1.9}$.
* **Real-World Solution:** This is why commercial 2.5D packages (like TSMC CoWoS) use high-modulus **epoxy underfill** to redistribute stress away from corner microbumps, and place non-electrical "dummy bumps" at high-DNP corners.

---

### 3. Why $R_{\text{bump}}$ and $\tau_{50\%}$ Delay Track Each Other

The identical curve shapes on Panel 3 occur because **coupling capacitance $C$ remains constant while resistance $R$ scales as $1/P^2$**.

1. **Aspect Ratio Invariance:** In your sweep, $d = 0.5 \cdot P$. The capacitance formula depends on the ratio $P/d$:

$$C_{\text{coupling}} \propto \frac{1}{\operatorname{arccosh}(P/d)} = \frac{1}{\operatorname{arccosh}(2.0)} \approx \text{Constant}$$



Because $P/d = 2.0$ throughout the entire sweep, $C_{\text{parasitic}}$ stays flat at $\approx 1.08\,\text{fF}$.
2. **Resistance Quadrupling:** Resistance depends on cross-sectional area:

$$R_{\text{bump}} = \rho \cdot \frac{h_{\text{bump}}}{\pi (d/2)^2} \propto \frac{1}{P^2}$$


3. **Delay Tracking:** In the Elmore delay expression:

$$\tau_{50\%} = 0.35 \cdot R_{\text{bump}} \cdot C_{\text{parasitic}} + R_{\text{driver}} \cdot (C_{\text{parasitic}} + C_{\text{load}})$$



Since $C_{\text{parasitic}}$, $C_{\text{load}}$, and $R_{\text{driver}}$ are constant, $R_{\text{bump}}$ is the **only variable driving the curve shape**. Thus, $\tau(P)$ tracks $R_{\text{bump}}(P)$ directly.
