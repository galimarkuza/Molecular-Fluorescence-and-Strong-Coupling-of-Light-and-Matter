import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

file_names = ['m20.ods', 'm18.ods', 'm16.ods', 'm14.ods', 'm12.ods', 'm10.ods', 'm8.ods', 'm6.ods', 'm4.ods', 'm2.ods']
base_folder = r'C:\Users\Gali Markuza\Downloads'

peak_results = {}

for file_name in file_names:
    file_path = os.path.join(base_folder, file_name)

    df = pd.read_excel(file_path, engine='odf')

    # Filtering the data between 500 and 600 nm
    filtered_df = df[(df['X [nm (air)]'] >= 500) & (df['X [nm (air)]'] <= 600)]

    smoothed_intensity = gaussian_filter1d(filtered_df['Y [Intensity]'], sigma=9)

    peaks, properties = find_peaks(
        smoothed_intensity,
        prominence=0.001,  
        distance=10  
    )

    if len(peaks) < 2:
        print(f"Less than two peaks found in {file_name}.")
        peak_results[file_name] = []
        sorted_peaks = []
    else:
        peak_heights = smoothed_intensity[peaks]

        top_two_indices = np.argsort(peak_heights)[-2:]
        top_peaks = peaks[top_two_indices]

        peak_wavelengths = filtered_df['X [nm (air)]'].iloc[top_peaks].values
        peak_intensities = smoothed_intensity[top_peaks]

        sorted_peaks = sorted(zip(peak_wavelengths, peak_intensities), key=lambda x: x[0])
        peak_results[file_name] = [wave for wave, intensity in sorted_peaks]

        print(f"\nFor file {file_name}, estimated two main peaks (wavelength, intensity):")
        for wave, intensity in sorted_peaks:
            print(f"  Wavelength: {wave:.2f} nm, Intensity: {intensity:.5f}")

    # --- Plotting ---
    plt.figure(figsize=(12, 6))

    plt.plot(filtered_df['X [nm (air)]'], filtered_df['Y [Intensity]'],
             label='Raw Intensity (noisy)', color='lightgray')

    plt.plot(filtered_df['X [nm (air)]'], smoothed_intensity,
             label='Smoothed Intensity', color='blue')

    plt.plot(filtered_df['X [nm (air)]'].iloc[peaks],
             smoothed_intensity[peaks],
             'rx', label='Detected Peaks')

    for wave, intensity in sorted_peaks:
        plt.plot(wave, intensity, 'ko')
        plt.text(wave, intensity, f' {wave:.1f}', fontsize=18, va='bottom')

    plt.xlabel('Wavelength [nm]', fontsize=18)
    plt.ylabel('Intensity (normalized)', fontsize=18)

    match = re.search(r"m(\d+)", file_name)
    angle_value = match.group(1) if match else "?"
    plt.title(f"Spectral Intensity / Wavelength with Reduced Noise, Angle = -{angle_value}°", fontsize=20)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# After processing all files, print the list of peak wavelengths for each file:
print("\nAll estimated peak wavelengths per file:")
for file_name, peaks_list in peak_results.items():
    print(f"{file_name}: {peaks_list}")
