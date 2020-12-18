
"""
Degiskenler: Aftertaste, Acidity, Flavor
Acidity ve Flavor Arasinda kayda deger pozitif kolerasyon var
Sweetness ile ise negatif kolerasyon var

Ornek Kurallar Kurallar
IF (Aftertaste Yuksek) and (Acidity Yuksek) then Flavor Yuksek

Uyelik Fonksyonlari
ucgenin trimf 6 7 8, 7 8 9, 8 9 10
AZ ORTA COK

modeli test ederken veri setinde belirli ozellikler disinda olanlari 

modelde olmayan verileri drop etmek gerekir
"""

#%% importlar

import numpy as np
import skfuzzy as fuzz
import pandas as pd
import matplotlib.pyplot as plt

#%% kullanilacak verilerin duzenlenmesi

column_list = ["Aftertaste", "Acidity", "Flavor"]

df = pd.read_csv("../../data/merged_data_cleaned.csv", usecols = column_list)

columns = df.columns
print("columns: ", columns)  # columns
print("raw shape", df.shape)

# drop null and zero values values
df = df.dropna()
df = df[(df.T != 0).any()]

print("0 degerler dusuruldukten sonra shape: ", df.shape)
#%% pandas histograms


#%% uyelik fonksyonlarini olusturma

x_aftertaste = np.arange(6, 10.1, 0.1)
x_acidity = np.arange(6, 10.1, 0.1)
x_flavor = np.arange(6, 10.1, 0.1)

aftertaste_D = fuzz.trimf(x_aftertaste, [6, 7, 8])
aftertaste_O = fuzz.trimf(x_aftertaste, [7, 8, 9])
aftertaste_Y = fuzz.trimf(x_aftertaste, [8, 9, 10])

acidity_D = fuzz.trimf(x_acidity, [6, 7, 8])
acidity_O = fuzz.trimf(x_acidity, [7, 8, 9])
acidity_Y = fuzz.trimf(x_acidity, [8, 9, 10])

flavor_D = fuzz.trimf(x_flavor, [6, 7, 8])
flavor_O = fuzz.trimf(x_flavor, [7, 8, 9])
flavor_Y = fuzz.trimf(x_flavor, [8, 9, 10])


fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8,9))
ax0.plot(x_aftertaste, aftertaste_D, 'b', linewidth=1.5, label='D')
ax0.plot(x_aftertaste, aftertaste_O, 'g', linewidth=1.5, label='O')
ax0.plot(x_aftertaste, aftertaste_Y, 'r', linewidth=1.5, label='Y')
ax0.set_title('Sweetness')
ax0.legend()

ax1.plot(x_acidity, acidity_D, 'b', linewidth=1.5, label='D')
ax1.plot(x_acidity, acidity_O, 'g', linewidth=1.5, label='O')
ax1.plot(x_acidity, acidity_Y, 'r', linewidth=1.5, label='Y')
ax1.set_title('Acidity')
ax1.legend()

ax2.plot(x_flavor, flavor_D, 'b', linewidth=1.5, label='D')
ax2.plot(x_flavor, flavor_O, 'g', linewidth=1.5, label='O')
ax2.plot(x_flavor, flavor_Y, 'r', linewidth=1.5, label='Y')
ax2.set_title('Flavor')
ax2.legend()

for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()    

#%% get randaom sample
random_row = df.sample(n = 1) 

# print(random_row)
aftertaste = random_row.iloc[0]['Aftertaste']
acidity = random_row.iloc[0]['Acidity']
flavor = random_row.iloc[0]['Flavor']
row_t  = (aftertaste, acidity, flavor,)
# print(aftertaste, flavor, acidity)

#%% aftertaste memberships
aftertaste_level_D = fuzz.interp_membership(x_aftertaste, aftertaste_D, aftertaste)
aftertaste_level_O = fuzz.interp_membership(x_aftertaste, aftertaste_O, aftertaste)
aftertaste_level_Y = fuzz.interp_membership(x_aftertaste, aftertaste_Y, aftertaste)

print(aftertaste_level_D)
print(aftertaste_level_O)
print(aftertaste_level_Y)

#%% acidity

acidity_level_D = fuzz.interp_membership(x_acidity, acidity_D, acidity)
acidity_level_O = fuzz.interp_membership(x_acidity, acidity_O, acidity)
acidity_level_Y = fuzz.interp_membership(x_acidity, acidity_Y, acidity)

print(acidity_level_D)
print(acidity_level_O)
print(acidity_level_Y)

#%% fuzzy inference

# Tek kural
# IF (Aftertaste Yuksek) and (Acidity Yuksek) then Flavor Yuksek

active_rule1 = np.fmin(acidity_level_Y, aftertaste_level_Y)
# active_rule2 = np.fmin(mud_level_MD, axunge_level_LG)
# active_rule3 = np.fmin(mud_level_LD, axunge_level_MG)
# active_rule4 = np.fmin(mud_level_LD, axunge_level_LG)
# print(active_rule1)

flavor_activation_1 = np.fmin(active_rule1, flavor_Y)
# wash_activation2 = np.fmin(active_rule2, wash_L)
# wash_activation3 = np.fmin(active_rule3, wash_L)
# wash_activation4 = np.fmin(active_rule4, wash_VL)
flavor0 = np.zeros_like(x_flavor)

#%% plot outputs

fig, ax0 = plt.subplots(figsize=(8, 3))
ax0.fill_between(x_flavor, flavor0, flavor_activation_1, facecolor='b', alpha=0.7)
ax0.plot(x_flavor, flavor_Y, 'b', linewidth=0.5, linestyle='--', )

# ax0.fill_between(x_wash, wash0, wash_activation2, facecolor='g', alpha=0.7)
# ax0.plot(x_wash, wash_L, 'g', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_wash, wash0, wash_activation3, facecolor='r', alpha=0.7)
# ax0.plot(x_wash, wash_L, 'r', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_wash, wash0, wash_activation4, facecolor='r', alpha=0.7)
# ax0.plot(x_wash, wash_VL, 'y', linewidth=0.5, linestyle='--', )
# ax0.set_title('Output membership activity')

# # Turn off top/right exes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout() 

# aggregated = np.fmax (wash_activation1, 
#                       np.fmax(wash_activation2, np.fmax(wash_activation3, wash_activation4))) 

# buradaki aggregated olayini anlamak lazim
# burada kaldim
# aggregated = np.fmax (flavor_activation_1,  np.fmax(flavor_activation_1)) 

# flavor = fuzz.defuzz(x_flavor, aggregated, 'centroid')
# flavor_activation = wash_activation = fuzz.interp_membership(x_flavor, aggregated, flavor)
# fig, ax0 = plt.subplots(figsize=(8, 3))

# ax0.plot(x_wash, wash_VS, 'b', linewidth=1.5, linestyle='--')
# ax0.plot(x_wash, wash_S, 'g', linewidth=1.5, linestyle='--')
# ax0.plot(x_wash, wash_M, 'r', linewidth=1.5, linestyle='--')
# ax0.plot(x_wash, wash_L, 'y', linewidth=1.5, linestyle='--')
# ax0.plot(x_wash, wash_VL, 'm', linewidth=1.5, linestyle='--')
# ax0.fill_between(x_wash, wash0, aggregated, facecolor='Orange', alpha=0.7)
# ax.plot([wash, wash], [0, wash_activation], 'k', linewidth=1.5, alpha=0.9)
# ax0.set_title('Aggregated membership and result (line)')
# plt.tight_layout()
# plt.show()


 







