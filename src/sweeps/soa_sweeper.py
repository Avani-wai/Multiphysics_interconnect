import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "plots"))

from src.engine import (
    compute_joule_heating,
    compute_blacks_mttf,
    compute_plastic_shear_strain,
    compute_coffin_manson_cycles,
    compute_interconnect_parasitics,
    compute_50_percent_rc_delay,
)

def sweep_electromigration_soa():
    J_range=np.logspace(4,6,100)
    T_amb_range=np.linspace(25,125,100)
    J_mesh,T_mesh=np.meshgrid(J_range,T_amb_range)
    T_eff_range,delta_T_range=compute_joule_heating(J_mesh,T_mesh)
    mttf_hours=compute_blacks_mttf(J_mesh,T_eff_range)
    return(J_mesh,T_mesh,mttf_hours/8760) #mttf in years

def sweep_fatigue_soa():
    dnp_range=np.linspace(0.1,25,100)*1e-3
    dT_range=np.linspace(0,150,100)
    dnp_mesh,dT_mesh=np.meshgrid(dnp_range,dT_range)
    strain_array=compute_plastic_shear_strain(dnp_mesh,dT_mesh)
    N_f_array=compute_coffin_manson_cycles(strain_array,T_max=125 + 273.15) #125 C
    return(dnp_mesh,dT_mesh,N_f_array)

def sweep_pitch_scaling():
    pitch_range=np.linspace(5,40,100)*1e-6
    diameter_range=0.5*pitch_range
    R_bump,C_parasitic=compute_interconnect_parasitics(pitch_range,diameter_range)
    tau_ps=compute_50_percent_rc_delay(R_bump,C_parasitic)
    return(pitch_range*1e6,R_bump,C_parasitic,tau_ps)

def generate_soa_plots():
    """
    Generates a publication-quality 3-panel figure summarizing multi-physics reliability limits.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=150)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # --------------------------------------------------------------------------
    # Panel 1: Electromigration Safe Operating Area (SOA)
    # --------------------------------------------------------------------------
    J_mesh, T_mesh, mttf_years = sweep_electromigration_soa()
    log_mttf = np.log10(np.clip(mttf_years, 1e-2, 1e4))

    contour1 = axes[0].contourf(J_mesh, T_mesh, log_mttf, levels=25, cmap='viridis_r')
    cbar1 = fig.colorbar(contour1, ax=axes[0])
    cbar1.set_label('Log10(MTTF in Years)', fontsize=10, fontweight='bold')

    # Highlight 10-Year Target Limit Boundary
    target_line = axes[0].contour(
        J_mesh, T_mesh, mttf_years, levels=[10.0], 
        colors='red', linewidths=2.0, linestyles='--'
    )
    axes[0].clabel(target_line, fmt={10.0: '10-Yr Target'}, inline=True, fontsize=9)
    axes[0].set_xscale('log')
    axes[0].set_title('Electromigration SOA Map', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Current Density $J$ ($\mathrm{A/cm^2}$)', fontsize=10, fontweight='bold')
    axes[0].set_ylabel('Ambient Temperature $T_{amb}$ (°C)', fontsize=10, fontweight='bold')

    # --------------------------------------------------------------------------
    # Panel 2: Thermo-Mechanical Fatigue SOA
    # --------------------------------------------------------------------------
    DNP_mesh_mm, DT_mesh, N_f = sweep_fatigue_soa()
    log_Nf = np.log10(np.clip(N_f, 10, 1e6))

    contour2 = axes[1].contourf(DNP_mesh_mm, DT_mesh, log_Nf, levels=25, cmap='magma_r')
    cbar2 = fig.colorbar(contour2, ax=axes[1])
    cbar2.set_label('Log10(Cycles to Failure $N_f$)', fontsize=10, fontweight='bold')

    # Highlight 3,000 Cycle Target Limit Boundary
    cycle_line = axes[1].contour(
        DNP_mesh_mm, DT_mesh, N_f, levels=[3000.0], 
        colors='cyan', linewidths=2.0, linestyles='--'
    )
    axes[1].clabel(cycle_line, fmt={3000.0: '3,000 Cycles Target'}, inline=True, fontsize=9)
    axes[1].set_title('Thermo-Mechanical Fatigue SOA', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Distance to Neutral Point DNP (mm)', fontsize=10, fontweight='bold')
    axes[1].set_ylabel('Thermal Cycling Range $\Delta T$ (°C)', fontsize=10, fontweight='bold')

    # --------------------------------------------------------------------------
    # Panel 3: Pitch Scaling vs Parasitic Resistance
    # --------------------------------------------------------------------------
    pitch_um, R_bump, C_parasitic, tau_ps = sweep_pitch_scaling()

    ax3_twin = axes[2].twinx()
    line1 = axes[2].plot(pitch_um, R_bump * 1e3, color='crimson', lw=2.5, label='Resistance $R_{bump}$ (mΩ)')
    line2 = ax3_twin.plot(pitch_um, tau_ps, color='navy', lw=2.5, ls='--', label='50% Delay $\\tau_{50\\%}$ (ps)')

    axes[2].set_title('Interconnect Scaling ($40\,\mu\mathrm{m} \\rightarrow 5\,\mu\mathrm{m}$)', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Microbump Pitch $P$ ($\mu\mathrm{m}$)', fontsize=10, fontweight='bold')
    axes[2].set_ylabel('Microbump Resistance $R$ ($\mathrm{m\Omega}$)', color='crimson', fontsize=10, fontweight='bold')
    ax3_twin.set_ylabel('Signal Delay $\\tau_{50\\%}$ (ps)', color='navy', fontsize=10, fontweight='bold')
    axes[2].grid(True, ls=':', alpha=0.6)

    # Combine legends for twin axis plot
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    axes[2].legend(lines, labels, loc='center right')

    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filepath = os.path.join(OUTPUT_DIR, "chiplet_reliability_soa_analysis.png")
    plt.savefig(output_filepath, dpi=300)
    print(f"[+] Sweeps complete. SOA dashboard successfully saved to '{output_filepath}'.")
    plt.show()


if __name__ == "__main__":
    print("[+] Running Multi-Physics Parameter Sweeps & SOA Engine...")
    generate_soa_plots()