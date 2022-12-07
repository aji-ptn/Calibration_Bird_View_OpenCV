import os
import numpy as np

for filename in os.listdir('./'):
    if filename.endswith(".npy"):
        print(filename)  # printing file name of desired extension
        with open(filename, 'wb') as f:
            np.save(f, None)
    else:
        continue