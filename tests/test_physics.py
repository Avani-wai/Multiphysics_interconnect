import sys
sys.path.append('.')

from src.engine.physics import (
    compute_joule_heating,
    compute_blacks_mttf,
    compute_plastic_shear_strain,
    compute_coffin_manson_cycles,
    compute_interconnect_parasitics,
    compute_50_percent_rc_delay
)

print("=== DELIVERABLE 1 VERIFICATION ===")

# Test 1: Electromigration & Self-Heating
T_eff, dT = compute_joule_heating(J_A=2e5, T_amb=85.0)
mttf = compute_blacks_mttf(J_A=2e5, T_eff=T_eff)
print(f"[EM Module]  Joule dT: {dT:.2f} °C | MTTF: {mttf / 8760:.2f} Years")

# Test 2: Thermo-Mechanical Fatigue
shear_strain = compute_plastic_shear_strain(dnp_m=10e-3, delta_T_thermal=165.0) # -40C to 125C
N_f = compute_coffin_manson_cycles(gamma_shear=shear_strain, T_max=125.0 + 273.15)
print(f"[Fatigue]   Plastic Strain: {shear_strain:.4f} | Cycles to Failure: {N_f:.0f} cycles")

# Test 3: Parasitics & Delay for scaled pitches
for pitch_um in [40, 20, 10]:
    p_m = pitch_um * 1e-6
    d_m = p_m * 0.5  # 50% aspect ratio
    R, C = compute_interconnect_parasitics(pitch=p_m, diameter=d_m)
    tau_ps = compute_50_percent_rc_delay(R_bump=R, C_parasitic=C)
    print(f"[SI Module]  Pitch {pitch_um:2d} µm -> R: {R*1e3:6.2f} mΩ | C: {C*1e15:5.2f} fF | Delay: {tau_ps:.2f} ps")

print("==================================")