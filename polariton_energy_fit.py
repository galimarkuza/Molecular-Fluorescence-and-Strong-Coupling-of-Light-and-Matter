import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import Model, RealData, ODR

df = pd.read_excel(r'C:\Users\Gali Markuza\Downloads\Book.xlsx')
wavelength = df['Lambda LP [nm]'].values
print(type(wavelength))
angle = df['Angle [deg]'].values
k_lp = df['k_lp'].values
k_err = df['k_lp_err'].values
E_lp = df['E_LP'].values

k_up = df['k'].values
E_up = df['E_up'].values
k_err_up = df['k_err'].values

#lower energy function:
def model_func(B, x):
    a0, a1, a2, a3, a4 = B
    term1 = a0 / 2 + a1 / 2 * np.sqrt((x-a4)**2 + a2**2)
    term2 = np.sqrt(a3**2 + (a0 - a1 * np.sqrt((x-a4)**2 + a2**2))**2)
    return term1 - term2

#upper energy function:
def model_func_up(B, x):
    a0, a1, a2, a3, a4 = B
    term1 = a0 / 2 + a1 / 2 * np.sqrt((x-a4)**2 + a2**2)
    term2 = np.sqrt(a3**2 + (a0 - a1 * np.sqrt((x-a4)**2 + a2**2))**2)
    return term1 + term2


model = Model(model_func)
model_up = Model(model_func_up)

data = RealData(k_lp, E_lp, sx=k_err)
data_up = RealData(k_up, E_up, sx=k_err_up)

initial_guess = [2.23, 132, 0.021, 0.2, -0.001]

odr = ODR(data, model, beta0=initial_guess)
odr_up = ODR(data_up, model_up, beta0=initial_guess)

output = odr.run()
output_up = odr_up.run()

#fitted parameters:

print("Fitted parameters:", output.beta)
print("Fitted parameters up:", output_up.beta)
print("Parameter standard errors:", output.sd_beta)
print("Parameter standard errors up:", output_up.sd_beta)

#plot:

plt.errorbar(k_lp, E_lp, fmt='.', label='Lower Energy data', color='blue')
plt.errorbar(k_up, E_up, fmt='.', label='Upper Energy Data', color='orange')
k_fit = np.linspace(min(k_lp), max(k_lp), 200)
k_fit_up = np.linspace(min(k_up), max(k_up), 200)
E_fit = model_func(output.beta, k_fit)
E_fit_up = model_func_up(output_up.beta, k_fit_up)
plt.plot(k_fit, E_fit, 'g-', label='Lower Energy Fit')
plt.plot(k_fit_up, E_fit_up, 'r-', label='Upper Energy Fit')
plt.title('Upper and Lower Polariton Energy as a function of parallel wave-number k', fontsize=20)
plt.xlabel('k [1/nm]', fontsize=18)
plt.ylabel('E_up/E_lp [eV]', fontsize=18)
plt.legend()
plt.grid(True)
plt.show()

#Reasiduals:

residual_lower = E_lp - model_func(output.beta, k_lp)
residual_upper = E_up - model_func_up(output_up.beta, k_up)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.errorbar(k_lp, residual_lower, xerr=k_err, fmt='.', color='blue')
plt.axhline(0, color='black', linestyle='--')
plt.title('Residuals: Lower Polariton Energy', fontsize=20)
plt.xlabel('k [1/nm]', fontsize=18)
plt.ylabel('Residuals [eV]', fontsize=18)
plt.grid(True)

plt.subplot(1, 2, 2)
plt.errorbar(k_up, residual_upper, xerr=k_err_up, fmt='.', color='orange')
plt.axhline(0, color='black', linestyle='--')
plt.title('Residuals: Upper Polariton Energy', fontsize=20)
plt.xlabel('k [1/nm]', fontsize=18)
plt.ylabel('Residual [eV]', fontsize=18)
plt.grid(True)

plt.tight_layout()
plt.show()
