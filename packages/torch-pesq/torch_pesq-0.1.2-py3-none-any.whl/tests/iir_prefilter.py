from scipy.signal import sos2tf

coeffs_sos = [[2.740826, -5.4816519, 2.740826, 1.0, -1.9444777, 0.94597794]]
b, a = sos2tf(coeffs_sos)

print(b, a)
