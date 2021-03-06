"""
Degiskenler: Aftertaste, Acidity, Flavor
Acidity ve Flavor Arasinda kayda deger pozitif kolerasyon var
Sweetness ile ise negatif kolerasyon var

Ornek Kurallar Kurallar
IF (Aftertaste Yüksek) and (Acidity Yüksek) then Flavor Yüksek
IF (Aftertaste Yüksek) and (Acidity Yüksek) then Flavor Yüksek
IF (Aftertaste Yüksek) and (Acidity Yüksek) then Flavor Yüksek

Uyelik Fonksyonlari
ucgenin trimf 6 7 8, 7 8 9, 8 9 10
AZ ORTA COK

degiskenlerde flavor yerine cupper points te kullanilabilir
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
# print("columns: ", columns)  # columns
print("raw shape", df.shape)

# drop null/na
df = df.dropna()
# drop zeros
df = df[(df.T != 0).any()]
# filter values
df = df[df['Aftertaste'] > 6] 
df = df[df['Acidity'] > 6] 
print("onislemenden sonra shape: ", df.shape)

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

for i in range(10):
    aftertaste_D[i] = 1 
    acidity_D[i] = 1
    flavor_D[i] = 1
    
for i in range(30,41):
    aftertaste_Y[i] = 1
    acidity_Y[i] = 1 
    flavor_Y[i] = 1


fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(12, 12))
ax0.plot(x_aftertaste, aftertaste_D, 'b', linewidth=1.5, label='Düşük')
ax0.plot(x_aftertaste, aftertaste_O, 'g', linewidth=1.5, label='Orta')
ax0.plot(x_aftertaste, aftertaste_Y, 'r', linewidth=1.5, label='Yüksek')
ax0.set_title('Aftertaste')
ax0.legend()

ax1.plot(x_acidity, acidity_D, 'b', linewidth=1.5, label='Düşük')
ax1.plot(x_acidity, acidity_O, 'g', linewidth=1.5, label='Orta')
ax1.plot(x_acidity, acidity_Y, 'r', linewidth=1.5, label='Yüksek')
ax1.set_title('Acidity')
ax1.legend()

ax2.plot(x_flavor, flavor_D, 'b', linewidth=1.5, label='Düşük')
ax2.plot(x_flavor, flavor_O, 'g', linewidth=1.5, label='Orta')
ax2.plot(x_flavor, flavor_Y, 'r', linewidth=1.5, label='Yüksek')
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

print(random_row)
aftertaste = random_row.iloc[0]['Aftertaste']
acidity = random_row.iloc[0]['Acidity']
flavor_org = random_row.iloc[0]['Flavor']

# aftertaste = 5.25
# acidity = 6.17
# flavor_org = 6.08

df.max(axis = 0) 
df.min(axis = 0) 

row_t  = (aftertaste, acidity, flavor_org,)
print("random data sample")
print("Acidity: ", acidity )
print("Aftertaste: ", aftertaste)
print("Flavor: ", flavor_org)

#%% aftertaste memberships
aftertaste_level_D = fuzz.interp_membership(x_aftertaste, aftertaste_D, aftertaste)
aftertaste_level_O = fuzz.interp_membership(x_aftertaste, aftertaste_O, aftertaste)
aftertaste_level_Y = fuzz.interp_membership(x_aftertaste, aftertaste_Y, aftertaste)

print("membership aftertaste_level_D: ", aftertaste_level_D)
print("membership aftertaste_level_O: ", aftertaste_level_O)
print("membership aftertaste_level_Y: ", aftertaste_level_Y)

#%% acidity

acidity_level_D = fuzz.interp_membership(x_acidity, acidity_D, acidity)
acidity_level_O = fuzz.interp_membership(x_acidity, acidity_O, acidity)
acidity_level_Y = fuzz.interp_membership(x_acidity, acidity_Y, acidity)

print("membership acidity_level_D: ", acidity_level_D)
print("membership acidity_level_O: ", acidity_level_O)
print("membership acidity_level_Y: ", acidity_level_Y)
#%% fuzzy inference burayi anlamak lazim

# Active rule un olayini anlamak lazim, mamdani ile mi alakali yoksa genel

'''
# * IF (Aftertaste Düşük) and (Acidity Düşük) then Flavor Düşük
# IF (Aftertaste Düşük) and (Acidity Orta) then Flavor Düşük
# IF (Aftertaste Düşük) and (Acidity Yüksek) then Flavor Orta

# IF (Aftertaste Orta) and (Acidity Düşük) then Flavor Düşük
# * IF (Aftertaste Orta) and (Acidity Orta) then Flavor Orta
# IF (Aftertaste Orta) and (Acidity Yüksek) then Flavor Yüksek

# IF (Aftertaste Yüksek) and (Acidity Düşük) then Flavor Orta
# IF (Aftertaste Yüksek) and (Acidity Orta) then Flavor Yüksek
# * IF (Aftertaste Yüksek) and (Acidity Yüksek) then Flavor Yüksek
'''

active_rule1 = np.fmin(acidity_level_D, aftertaste_level_D)
active_rule2 = np.fmin(acidity_level_D, aftertaste_level_D)
active_rule3 = np.fmin(acidity_level_D, aftertaste_level_D)

active_rule4 = np.fmin(acidity_level_O, aftertaste_level_O)
active_rule5 = np.fmin(acidity_level_O, aftertaste_level_O)
active_rule6 = np.fmin(acidity_level_O, aftertaste_level_O)

active_rule7 = np.fmin(acidity_level_Y, aftertaste_level_Y)
active_rule8 = np.fmin(acidity_level_Y, aftertaste_level_Y)
active_rule9 = np.fmin(acidity_level_Y, aftertaste_level_Y)

print("active_rule1: ", active_rule1)
print("active_rule4: ", active_rule4)
print("active_rule9: ", active_rule9)


'''
mamdaninin devami
'''

flavor_activation_1 = np.fmin(active_rule1, flavor_D)
flavor_activation_2 = np.fmin(active_rule4, flavor_O)
flavor_activation_3 = np.fmin(active_rule9, flavor_Y)

flavor0 = np.zeros_like(x_flavor)
#%% plot outputs


fig, ax0 = plt.subplots(figsize=(10, 4))
ax0.set_title('Üyelik Aktivasyonu')
ax0.fill_between(x_flavor, flavor0, flavor_activation_1, facecolor='b', alpha=0.7)
ax0.plot(x_flavor, flavor_Y, 'b', linewidth=0.5, linestyle=':', )

ax0.fill_between(x_flavor, flavor0, flavor_activation_2, facecolor='g', alpha=0.7)
ax0.plot(x_flavor, flavor_O, 'g', linewidth=0.5, linestyle=':', )

ax0.fill_between(x_flavor, flavor0, flavor_activation_3, facecolor='r', alpha=0.7)
ax0.plot(x_flavor, flavor_D, 'r', linewidth=0.5, linestyle=':', )


# Turn off top/right exes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout() 

''' aggregated, np.fmax()
    np.fmax() 
    npCompare two arrays and returns a new array containing the element-wise maxima
'''

aggregated = np.fmax (flavor_activation_1, 
                      np.fmax(flavor_activation_2, flavor_activation_3)) 

''' flavor, fuzz.defuzz()

'''

flavor_model = fuzz.defuzz(x_flavor, aggregated, 'centroid')
# !!! flavor_activation bunun olayini anlamak lazim
flavor_activation = fuzz.interp_membership(x_flavor, aggregated, flavor_model)

print('flavor model: ', flavor_model)
print('flavor original: ', flavor_org)
print('model error', format(abs((flavor_model - flavor_org) / flavor_org) * 100, '.4f'))

fig, ax0 = plt.subplots(figsize=(10, 4))
ax0.plot(x_flavor, flavor_D, 'b', linewidth=1.5, linestyle=':')
ax0.plot(x_flavor, flavor_O, 'g', linewidth=1.5, linestyle=':')
ax0.plot(x_flavor, flavor_Y, 'r', linewidth=1.5, linestyle=':')

ax0.fill_between(x_flavor, flavor0, aggregated, facecolor='cyan', alpha=0.7)
ax0.plot([flavor_model, flavor_model], [0, flavor_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Üyeliklerin Kümelenmesi ve Durulama Çıktısı')