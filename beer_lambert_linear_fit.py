import pandas as pd
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# List of .ods files to process.
file_list = [
r'C:\Users\Gali Markuza\Downloads\c10RG8000.ods',
r'C:\Users\Gali Markuza\Downloads\c9RG7000.ods',
r'C:\Users\Gali Markuza\Downloads\c8RG6000.ods',
r'C:\Users\Gali Markuza\Downloads\c7RG6000.ods',
r'C:\Users\Gali Markuza\Downloads\c6RG5000.ods'
# r'C:\Users\Gali Markuza\Downloads\c5RG4000.ods',
# r'C:\Users\Gali Markuza\Downloads\c4RG3000.ods',
# r'C:\Users\Gali Markuza\Downloads\c3RG2000.ods',
# r'C:\Users\Gali Markuza\Downloads\c2RG1000.ods',
# r'C:\Users\Gali Markuza\Downloads\c1RG1000.ods'
]

# Dictionary to store results for each file.
results = {}
lst = []      # List to store integrated values.
lst_err = []  # List to store error estimates.

# "con" values (independent variable values)
con = [10**(-4), 5*(10**(-4)), 8*(10**(-4)), 10**(-3), 2.5*(10**(-3))]
# 5*(10**(-3)), 0.01, 0.025, 0.05, 0.1]

# Loop over each file.
for file in file_list:
    try:
        # Load the .ods file (requires odfpy: pip install odfpy)
        df = pd.read_excel(file, engine='odf')
    except Exception as e:
        print(f"Error loading file {file}: {e}")
        continue

    # Filter rows where x > 460.
    df_filtered = df[df['X [nm (air)]'] > 460]
    if df_filtered.empty:
        print(f"No data with x > 460 in file {file}.")
        continue

    # Extract x and y values.
    x_values = df_filtered['X [nm (air)]'].values
    y_values = df_filtered['Y [Intensity]'].values

    # Sort the data by x (necessary for interpolation).
    sort_idx = np.argsort(x_values)
    x_values = x_values[sort_idx]
    y_values = y_values[sort_idx]

    # Create an interpolation function.
    f_interp = interp1d(x_values, y_values, kind='cubic', fill_value="extrapolate")

    # Define integration limits.
    x_min = x_values.min()
    x_max = x_values.max()

    # Integrate the interpolated function over the defined range.
    integral_value, error_estimate = quad(f_interp, x_min, x_max)
    lst.append(integral_value)
    lst_err.append(error_estimate)

    # Store and print the results.
    results[file] = {'integral': integral_value, 'error': error_estimate}
    print(f"File: {file}")
    print(f"  Integrated value: {integral_value}")
    print(f"  Estimated error: {error_estimate}\n")

print("All results:")
print(results)

# Convert lists to numpy arrays.
con_array = np.array(con)
integrals_array = np.array(lst)
lst_err_array = np.array(lst_err)

# Perform a weighted linear fit: y = m*x + b.
# Weights are 1/sigma, where sigma is the error in y (integrals).
weights = 1.0 / lst_err_array
coeffs = np.polyfit(con_array, integrals_array, 1, w=weights)
m, b = coeffs
print(f"Fitted line parameters: slope = {m}, intercept = {b}")

# Evaluate the fit at the original con values.
integrals_fit = np.polyval(coeffs, con_array)
residuals = integrals_array - integrals_fit

# ------------------------------
# Plot 1: Linear Fit Plot
# ------------------------------
plt.figure(figsize=(8, 6))
plt.errorbar(con_array, integrals_array, yerr=lst_err_array, fmt='.', color='blue', label='Data')
# Generate a smooth curve for the fit line.
con_fit = np.linspace(con_array.min(), con_array.max(), 100)
plt.plot(con_fit, np.polyval(coeffs, con_fit), 'r-', label='Linear Fit')
plt.xlabel('Concentration [mM]', fontsize=18)
plt.ylabel('Integrated Intensity (normalized)', fontsize=18)
plt.title('Intensity as a function of Concentration - Linear Fit - Rhodamine 6G (low con.)', fontsize=20)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# Plot 2: Residuals Plot
# ------------------------------
plt.figure(figsize=(8, 6))
plt.errorbar(con_array, residuals, yerr=lst_err_array, fmt='.', color='blue', label='Residuals')
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('Concentration [mM]', fontsize=18)
plt.ylabel('Residuals', fontsize=18)
plt.title('Residuals of Linear Fit - Intensity as a function of Concentration - Rhodamine 6G (low con.)', fontsize=20)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
