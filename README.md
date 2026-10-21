# Multiphysics_interconnect

```text
Multiphysics_interconnect/
├── src/
│   ├── engine/
│   │   ├── __init__.py
│   │   └── physics.py          # Deliverable 1: Core Physics Equations
│   ├── sweeps/                # Deliverable 2: Parameter Sweeps & SOA
│   └── visualization/         # Deliverable 2/3: Heatmaps & Plots
├── tests/
│   └── test_physics.py        # Unit tests
├── README.md
├── requirements.txt
└── .gitignore
```

The motivation:
Modern AI hardware accelerators are constrained less by monolithic transistor scaling and far more by 2.5D/3D packaging limits—specifically thermo-mechanical reliability, electromigration limits in 3D packages, and RC delay scaling across dense interconnect arrays.

The tradeoff is that packing many fine microbumps and Cu-filled TSVs into a small region concentrates current and heat. Copper, silicon, underfill, and dielectric materials expand by different amounts, creating stress hotspots and accelerating interconnect degradation.

Governing equations:

- a) Electromigration Kinetics & Self-Heating (Black's Law)

  T_eff = T_amb + (J_A · 1e4)^2 · rho · (1 + alpha_T · (T_amb + 273.15 - 298.15)) · h_bump · R_th

  MTTF = A_const · J_A^n_exp · exp(E_act / (k_B · T_eff))

  where:
  - J_A is the current density in A/cm^2, converted in code as J_A · 1e4 to A/m^2
  - T_amb is ambient temperature in °C
  - rho is the electrical resistivity in Ω·m
  - alpha_T is the temperature coefficient of resistivity
  - h_bump is bump height in m
  - R_th is the thermal resistance term used in the self-heating approximation
  - k_B = 8.6173332621e-5 eV/K is the Boltzmann constant
  - n_exp = -2 and E_act = 0.68 eV are the default empirical values

- b) Thermo-Mechanical Stress & Fatigue (Coffin-Manson)

  gamma_shear = (dnp_m / h_bump) · |alpha_sub - alpha_chip| · delta_T_thermal

  N_f = C_fatigue · (gamma_shear / 2)^m_exp · exp(E_act_fatigue / (k_B · (T_max + 273.15)))

  where:
  - dnp_m is the distance to the neutral point in m
  - alpha_chip and alpha_sub are the chip and substrate CTEs
  - delta_T_thermal is the thermal excursion in K
  - T_max is the peak temperature in °C before conversion to K
  - m_exp = -1.9 and E_act_fatigue = 0.12 eV are the default fatigue parameters

- c) Signal Integrity & Interconnect Delay (RC)

  A = pi · (diameter^2 / 4)

  R_bump = rho · h_bump / A

  C_parasitic = (pi · epsilon_0 · Er_dielectric · h_bump) / arccosh(pitch / diameter)

  tau_50 = (0.35 · R_bump · C_parasitic + R_driver · (C_parasitic + C_load)) · 1e12

  where:
  - A is the bump cross-sectional area
  - pitch is the interconnect pitch in m
  - diameter is the bump diameter in m
  - epsilon_0 = 8.854e-12 F/m is the vacuum permittivity
  - Er_dielectric is the relative dielectric constant
  - R_driver and C_load are the driver resistance and load capacitance

1. Package initializer (src/engine/__init__.py)
The purpose of __init__.py is to expose a clean public API so users (and your downstream sweep scripts) can import functions directly from src.engine without navigating nested module paths.

2. Physics Module with 6 governing functions:

3. Sweeps and plots

| Panel | Quantity / Plot | Overlay / Interpretation |
| --- | --- | --- |
| Panel 1: EM SOA | Contour: log10(MTTF) | Overlay: 10-Year Target |
| Panel 2: Fatigue SOA | Contour: log10(Nf) | Overlay: 3000 Cycles |
| Panel 3: Pitch Scaling | Twin-axis plot: R (mΩ) vs Delay (ps) | Tradeoff analysis across pitch and stackup |

This project provides a compact physical model for evaluating whether a package interconnect design remains within electromigration, fatigue, and delay constraints under realistic operating conditions.
