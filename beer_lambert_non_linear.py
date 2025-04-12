import pandas as pd
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter1d

file_list = [
    r'C:\Users\Gali Markuza\Downloads\c10FL8000.ods',
    r'C:\Users\Gali Markuza\Downloads\c9FL8000.ods',
    r'C:\Users\Gali Markuza\Downloads\c8FL8000.ods',
    r'C:\Users\Gali Markuza\Downloads\c7FL6000.ods',
    r'C:\Users\Gali Markuza\Downloads\c6FL5000.ods',
    r'C:\Users\Gali Markuza\Downloads\c5Fl4000.ods',
    r'C:\Users\Gali Markuza\Downloads\c4FL3000.ods',
    r'C:\Users\Gali Markuza\Downloads\c3FL2000.ods',
    r'C:\Users\Gali Markuza\Downloads\c2FL1000.ods',
    r'C:\Users\Gali Markuza\Downloads\c1FL1000.ods'
]

results = {}
lst = []     
lst_err = [] 

# concentrations:
con = [1*(10**(-4)), 5*(10**(-4)), 8*(10**(-4)), 10**(-3), 2.5*(10**(-3)),
       5*(10**(-3)), 0.01, 0.025, 0.05, 0.1]

for file in file_list:
    try:
        df = pd.read_excel(file, engine='odf')
    except Exception as e:
        print(f"Error loading file {file}: {e}")
        continue

    # Filtering rows where x > 460.
    df_filtered = df[df['X [nm (air)]'] > 460]
    if df_filtered.empty:
        print(f"No data with x > 460 in file {file}.")
        continue

    x_values = df_filtered['X [nm (air)]'].values
    y_values = df_filtered['Y [Intensity]'].values

    sort_idx = np.argsort(x_values)
    x_values = x_values[sort_idx]
    y_values = gaussian_filter1d(y_values[sort_idx], sigma=9)

    f_interp = interp1d(x_values, y_values, kind='cubic', fill_value="extrapolate")

    x_min = x_values.min()
    x_max = x_values.max()

    integral_value, error_estimate = quad(f_interp, x_min, x_max)
    lst.append(integral_value)
    lst_err.append(error_estimate)

    results[file] = {'integral': integral_value, 'error': error_estimate}
    print(f"File: {file}")
    print(f"  Integrated value: {integral_value}")
    print(f"  Estimated error: {error_estimate}\n")

print("All results:")
print(results)

con_array = np.array(con)
integrals_array = np.array(lst)
integrals_array_log = np.log10(integrals_array)
lst_err_array = np.array(lst_err)


def nonlinear_model(x, a0, a1, a2, a3):
    return (a0 / (1 + a1 * x + a2 * x ** 2)) * (1 - np.exp(-a3 * x))


p0 = [integrals_array.max(), 100.8, -503, 76.6]

popt, pcov = curve_fit(nonlinear_model, con_array, integrals_array, sigma=lst_err_array,
                        absolute_sigma=True, p0=p0)
print("Fitted parameters:", popt)

integrals_fit = nonlinear_model(con_array, *popt)
residuals = integrals_array - integrals_fit

# ------------------------------
# Plot 1: Non-linear Fit Plot
# ------------------------------
plt.figure(figsize=(8, 6))
plt.errorbar(con_array, integrals_array, yerr=lst_err_array, fmt='o', color='blue', label='Data')
con_fit = np.linspace(con_array.min(), con_array.max(), 100)
plt.plot(con_fit, nonlinear_model(con_fit, *popt), 'r-', label='Non-linear Fit')
plt.xlabel('Concentration [mM]', fontsize=18)
plt.ylabel('Integrated Intensity (normalized)', fontsize=18)
plt.title('Intensity as a Function of Concentration - non Linear Fit - Fluorescein', fontsize=20)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# Plot 2: Residuals Plot
# ------------------------------
plt.figure(figsize=(8, 6))
plt.errorbar(con_array, residuals, yerr=lst_err_array, fmt='o', color='blue', label='Residuals')
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('Concentration [mM]', fontsize=18)
plt.ylabel('Residuals', fontsize=18)
plt.title('Intensity as a Function of Concentration - non Linear Fit - Fluorescein - Residuals', fontsize=20)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
