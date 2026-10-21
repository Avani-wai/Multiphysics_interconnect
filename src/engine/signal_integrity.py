import numpy as np

'''def compute_R_line(w,t,rho_Cu=):
    R_line=rho_Cu/(w*t) #accounting for high frequency skin effect

def compute_L_line(h,w,Uo=,Ur=):
    L_line=(uo*ur*np.arccosh((2*h)/w))/2*np.pi()

def compute_C_line(h,w,Eo=,Er=):'''

def generate_prbs_signal(data_rate_gbps=16.0,v_dd=1.0,samples_per_bit=64,num_bits=127):
    t_bit=1/(data_rate_gbps*1e9)
    dt=t_bit/samples_per_bit #time step per sample
    lfsr=np.array([1,1,1,1,1,1,1])
    bits=[]
    for i in range(num_bits):
        bits.append(lfsr[-1])
        new_bit=lfsr[6]^lfsr[5]
        lfsr=[new_bit]+lfsr[:-1]
    bit_array=np.array(bits)

    v_in=np.repeat(bit_array*v_dd,samples_per_bit)
    total_samples=len(v_in)
    t_vec=np.arange(total_samples)*dt
    
    return(t_vec,v_in,t_bit)

