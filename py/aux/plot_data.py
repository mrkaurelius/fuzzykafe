import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% funcs


# %% read dataset with pandas and explore dataset

df = pd.read_csv("../../data/merged_data_cleaned.csv")

columns = df.columns
print("columns: ", columns)  # columns

# rlv_col_df = df.head()
# print(rlv_col_df) # head

# %% Flavor

fl_df = df["Flavor"]
fl_vals = fl_df.values
fl_vals = fl_vals[fl_vals != 0]
fl_vals = np.sort(fl_vals)

plt.style.use('ggplot')
plt.plot(fl_vals)
plt.ylabel("Flavor")
plt.show()

plt.hist(fl_vals, bins=60)
plt.ylabel("Flavor")
plt.show()


# %% Acidity

ac_df = df["Acidity"]
ac_vals = ac_df.values
ac_vals = ac_vals[ac_vals != 0]
ac_vals = np.sort(ac_vals)

plt.style.use('ggplot')
plt.ylabel("Acidity")
plt.plot(ac_vals)
plt.show()

plt.hist(ac_vals, bins=60)
plt.ylabel("Acidity")
plt.show()

# %% Aroma

ar_df = df["Aroma"]
ar_vals = ar_df.values
ar_vals = ar_vals[ar_vals != 0]
ar_vals = np.sort(ar_vals)

plt.style.use('ggplot')
plt.ylabel("Aroma")
plt.plot(ar_vals)
plt.show()

plt.hist(ar_vals, bins=60)
plt.ylabel("Aroma")
plt.show()

# %% Moisture

ar_df = df["Moisture"]
ar_vals = ar_df.values


plt.style.use('ggplot')

plt.hist(ar_vals, bins=30)
plt.show()
#%% describe



