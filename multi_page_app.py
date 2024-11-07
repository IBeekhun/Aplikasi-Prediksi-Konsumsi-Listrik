import pandas as pd
import numpy as np

# Setting random seed for reproducibility
np.random.seed(0)

# Generate 200 rows of data with two-digit numbers
n_samples = 200
data_train = pd.DataFrame({
    "Area": np.random.randint(30, 60, size=n_samples),  # Two-digit values for Area
    "Jumlah_Penghuni": np.random.randint(30, 50, size=n_samples),  # Two-digit values for Jumlah_Penghuni
    "Jumlah_Alat_Listrik": np.random.randint(10, 30, size=n_samples),  # Two-digit values for Jumlah_Alat_Listrik
    "Jam_Penggunaan": np.random.randint(50, 80, size=n_samples),  # Two-digit values for Jam_Penggunaan
    "Konsumsi_Listrik": np.random.randint(25, 50, size=n_samples)  # Two-digit values for Konsumsi_Listrik
})

# Save as CSV
data_train.to_csv('data_train_mlr_200.csv', index=False)

# Print the first few rows to confirm
print(data_train.head())
