import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

# List of your .ods files (adjust the names if needed)
file_names = ['m20.ods', 'm18.ods', 'm16.ods', 'm14.ods', 'm12.ods', 'm10.ods', 'm8.ods', 'm6.ods', 'm4.ods', 'm2.ods']
base_folder = r'C:\Users\Gali Markuza\Downloads'

# Dictionary to store the two peak wavelengths for each file
peak_results = {}

# Loop through each file
for file_name in file_names:
    file_path = os.path.join(base_folder, file_name)

    # Load the data from the file (using odf engine for .ods files)
    df = pd.read_excel(file_path, engine='odf')

    # Filter the data between 500 and 600 nm
    filtered_df = df[(df['X [nm (air)]'] >= 500) & (df['X [nm (air)]'] <= 600)]

    # Smooth the intensity data to reduce noise (adjust sigma as needed)
    smoothed_intensity = gaussian_filter1d(filtered_df['Y [Intensity]'], sigma=9)

    # Find peaks on the smoothed data; adjust prominence and distance as needed
    peaks, properties = find_peaks(
        smoothed_intensity,
        prominence=0.001,  # ignore peaks less "prominent" than this value
        distance=10  # peaks must be at least 10 points apart
    )

    # If less than two peaks are detected, save an empty list for this file
    if len(peaks) < 2:
        print(f"Less than two peaks found in {file_name}.")
        peak_results[file_name] = []
        sorted_peaks = []
    else:
        # Use the smoothed intensity values for peak heights
        peak_heights = smoothed_intensity[peaks]

        # Select indices of the two highest peaks
        top_two_indices = np.argsort(peak_heights)[-2:]
        top_peaks = peaks[top_two_indices]

        # Retrieve the corresponding wavelengths and intensities
        peak_wavelengths = filtered_df['X [nm (air)]'].iloc[top_peaks].values
        peak_intensities = smoothed_intensity[top_peaks]

        # Sort the peaks by wavelength (in case the order is not increasing)
        sorted_peaks = sorted(zip(peak_wavelengths, peak_intensities), key=lambda x: x[0])
        peak_results[file_name] = [wave for wave, intensity in sorted_peaks]

        print(f"\nFor file {file_name}, estimated two main peaks (wavelength, intensity):")
        for wave, intensity in sorted_peaks:
            print(f"  Wavelength: {wave:.2f} nm, Intensity: {intensity:.5f}")

    # --- Plotting ---
    plt.figure(figsize=(12, 6))

    # Plot the raw intensity in light gray
    plt.plot(filtered_df['X [nm (air)]'], filtered_df['Y [Intensity]'],
             label='Raw Intensity (noisy)', color='lightgray')

    # Plot the smoothed intensity in blue
    plt.plot(filtered_df['X [nm (air)]'], smoothed_intensity,
             label='Smoothed Intensity', color='blue')

    # Mark all detected peaks in red
    plt.plot(filtered_df['X [nm (air)]'].iloc[peaks],
             smoothed_intensity[peaks],
             'rx', label='Detected Peaks')

    # Highlight the top 2 peaks with black circles and add text labels
    for wave, intensity in sorted_peaks:
        plt.plot(wave, intensity, 'ko')
        plt.text(wave, intensity, f' {wave:.1f}', fontsize=18, va='bottom')

    plt.xlabel('Wavelength [nm]', fontsize=18)
    plt.ylabel('Intensity (normalized)', fontsize=18)

    # Extract the angle value from the file name using regex (e.g., m20 -> 20)
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
