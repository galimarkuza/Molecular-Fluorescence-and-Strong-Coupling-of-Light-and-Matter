import scipy.io
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

file_names = [fr'C:\Users\Gali Markuza\OneDrive - mail.tau.ac.il\Documents\סמסטר ו\מעבדה ג\molecular flouresence\matlab part 2\RB{i}.mat' for i in range(1, 11)]


def linear(l, a, b):
    return a * l + b


def polynomial(l, a, b, c, d):
    return a*(l**3) + b*(l**2) + c*l + d


con = [10**(-4), 5*(10**(-4)), 8*(10**(-4)), 10**(-3), 2.5*(10**(-3)), 5*(10**(-3)), 0.01, 0.025, 0.05, 0.1]
con_array = np.array(con[::-1])

for file in file_names:
    data = scipy.io.loadmat(file)

    x = data['x'].squeeze()
    Avl = data['Avl'].squeeze()

    mask = np.isfinite(Avl)
    x = x[mask]
    Avl = Avl[mask]

    popt, pcov = curve_fit(linear, x, Avl)
    Avl_fit = linear(x, *popt)

    residuals = Avl - Avl_fit

    plt.figure(figsize=(10, 8))

    # Upper subplot: Data and Linear Fit.
    plt.subplot(2, 1, 1)
    plt.plot(x, Avl, 'b.', label='Data')
    plt.plot(x, Avl_fit, 'r-', label='Linear Fit')
    plt.title(f'Intensity as a function of Path Length - Linear Fit & Residuals (Rhodamine B, con. = {con_array[file_names.index(file)]} [mM])', fontsize=16.5)
    plt.xlabel('x [cm]', fontsize=18)
    plt.ylabel('Intensity [AU]', fontsize=18)
    plt.legend()
    plt.grid(True)

    # Lower subplot: Residuals.
    plt.subplot(2, 1, 2)
    plt.plot(x, residuals, 'ko', label='Residuals')
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('x [cm]', fontsize=18)
    plt.ylabel('Residuals', fontsize=18)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
