import sys
sys.path.append('.')

from src.engine import (
    generate_prbs_signal,
    apply_channel_filter,
    extract_eye_metrics
)

print("=== SIGNAL INTEGRITY MODULE VERIFICATION ===")

# 1. Generate 16 Gbps PRBS-7 bit stream
data_rate = 16.0  # Gbps
spb = 64
t_vec, v_in, t_bit = generate_prbs_signal(data_rate_gbps=data_rate, samples_per_bit=spb)
print(f"[PRBS Engine]  Bit Period: {t_bit*1e12:.2f} ps | Total Samples: {len(v_in)}")

# 2. Test Channel A: Short Interposer Trace (Low RC, Open Eye)
R_short = 50.0      # Driver (50 Ohm) + short trace
C_short = 0.2e-12   # 200 fF
v_out_short = apply_channel_filter(v_in, t_vec, R_short, C_short)
_, height_short, width_short = extract_eye_metrics(v_out_short, spb, t_bit=t_bit)
print(f"[Channel Short] Eye Height: {height_short:.1f} mV | Eye Width: {width_short:.1f} ps (OPEN)")

# 3. Test Channel B: Long Interposer Trace (High RC, Degraded Eye)
R_long = 250.0      # High trace resistance
C_long = 1.5e-12    # 1.5 pF trace capacitance
v_out_long = apply_channel_filter(v_in, t_vec, R_long, C_long)
_, height_long, width_long = extract_eye_metrics(v_out_long, spb, t_bit=t_bit)
print(f"[Channel Long]  Eye Height: {height_long:.1f} mV | Eye Width: {width_long:.1f} ps (DEGRADED)")

print("===========================================")