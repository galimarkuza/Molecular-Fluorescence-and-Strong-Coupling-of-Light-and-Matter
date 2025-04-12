# Molecular Fluorescence and Strong Coupling of Light and Matter

This repository contains all of the data‑analysis code for our experiments on molecular fluorescence and exciton‑polariton strong coupling. In this experiment we analyze fluorescence spectra vs. fluorophore concentration or path length in a solution (testing deviations from Beer–Lambert law).  In adition, we examine the upper and lower polariton energies within an interferometric setup.

---
List Of Files:

polariton_energy_fit.py:
Receives an excel file with data of polaritons wave-numbers and energies, fits the data to a given formula of polariton energy and plots the obtained graphs + residuals.

exciton_polariton_2_peaks_smoothed.py:
Receives raw data of Intensity to wavelength, smoothes the data and finds the 2 prominent peaks in the graph. plots the obtained graph and outputs the selected peaks.

beer_lambert_linear_fit.py:
Recives excel files of intensity to wavelength, integrates over the intensity at a given range and fits the integrated intensities as a function of concentration (given list) to a linear formula + residuals.

beer_lambert_linear_fit.py:
Recives excel files of intensity to wavelength, integrates over the intensity at a given range and fits the integrated intensities as a function of concentration (given list) to a non-linear given formula + residuals.

partB.m:
A matlab code that receives an image of the fluorescent light in the cuvette, converts the pixles into length units and plots the light intensity as a function of cuvette length, for selected x axis range and y axis single point. outputs a table of the data.

beer_lambert_matlab_fit.py:
Recievs the table from the matlab code and plots a linear\3rd ordoe polynomial (can be configured in the code) to the data (light intensity as a function of path length) + residuals.
