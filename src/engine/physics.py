import numpy as np
Kb=8.6173332621e-5 #boltzmann constant
Kt=273.15 #Kelvin conversion
Eo=8.8541878128e-12 #permittivity in vacuum
'''J_A defined in cm^2
T_amb in C
rho in ohm m
R_th is 
h_bump in m'''

def compute_joule_heating(J_A,T_amb,h_bump=15e-6,rho=1.7e-8,alpha_T=0.00393,R_th=2.5e-7):
    J_A=np.asarray(J_A,dtype=float)
    T_amb=np.asarray(T_amb,dtype=float)
   
    J_A_m2=J_A*1e4
    T_amb_K=T_amb+Kt
    delta_T=(J_A_m2**2)*rho*(1+alpha_T*(T_amb_K-298.15))*h_bump*R_th
    T_eff=T_amb_K+delta_T #T_eff is in Kelvin
    return T_eff,delta_T


'''E_act is in eV
n_exp is taken as 2 for accounting void nucleation
A is emperical material scaling constant'''
def compute_blacks_mttf(J_A,T_eff,E_act=0.68,n_exp=-2.0,A_const=1.2e5):
    J_A=np.asarray(J_A,dtype=float)
    T_eff=np.asarray(T_eff,dtype=float)
   
    mttf=A_const*(J_A**n_exp)*np.exp(E_act/(Kb*T_eff))
    return mttf
'''dnp is distance to neutral point
CTE of chip and substrate is defined in the parameters'''


def compute_plastic_shear_strain(dnp_m,delta_T_thermal,h_bump=15e-6,alpha_chip=2.6e-6,alpha_sub=16.5e-6):
    dnp_m=np.asarray(dnp_m,dtype=float)
    delta_T_thermal=np.asarray(delta_T_thermal,dtype=float)
    
    delta_alpha=np.abs(alpha_sub-alpha_chip)
    gamma_shear=(dnp_m/h_bump)*delta_alpha*delta_T_thermal
    return gamma_shear


'''T_max is in kelvin.'''
def compute_coffin_manson_cycles(gamma_shear,T_max,C_fatigue=0.8,m_exp=-1.9,E_act_fatigue=0.12):
    gamma_shear=np.asarray(gamma_shear,dtype=float)
    T_max=np.asarray(T_max,dtype=float)+Kt
    
    N_f=C_fatigue*((gamma_shear/2)**m_exp)*np.exp(E_act_fatigue/(Kb*T_max))
    return N_f


'''pitch,diameter in metre
    er is relative permittivity of the dielectric
Coupling capacitance using parallel cylinder/CPW geometry approximation'''
def compute_interconnect_parasitics(pitch,diameter,h_bump=15e-6,rho=1.7e-8,Er_dielectric=3.4):
    pitch=np.asarray(pitch,dtype=float)
    diameter=np.asarray(diameter,dtype=float)
    
    Area=np.pi*(diameter**2/4)
    R_bump=rho*(h_bump/Area)
    C_parasitic=(np.pi*Eo*Er_dielectric*h_bump)/np.maximum(np.arccosh(pitch/diameter),1.001)
    return R_bump,C_parasitic


'''tau_50 is defined in ps'''
def compute_50_percent_rc_delay(R_bump,C_parasitic,R_driver=50.0,C_load=5e-15):
    R_bump=np.asarray(R_bump,dtype=float)
    C_parasitic=np.asarray(C_parasitic,dtype=float)

    tau_50=(0.35*R_bump*C_parasitic+R_driver*(C_parasitic+C_load))*1e12
    return tau_50