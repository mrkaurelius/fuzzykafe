"""
Degiskenler: Aftertaste, Flavor, Cupper.Points
Flavor ve Cupper.Points Arasinda kayda deger pozitif kolerasyon var
Sweetness ile ise negatif kolerasyon var

Ornek Kurallar Kurallar

# IF (Aftertaste Düşük) and (Flavor Düşük) then Cupper.Points Düşük
# IF (Aftertaste Düşük) and (Flavor Orta) then Cupper.Points Düşük
# IF (Aftertaste Düşük) and (Flavor Yüksek) then Cupper.Points Orta

# IF (Aftertaste Orta) and (Flavor Düşük) then Cupper.Points Düşük
# IF (Aftertaste Orta) and (Flavor Orta) then Cupper.Points Orta
# IF (Aftertaste Orta) and (Flavor Yüksek) then Cupper.Points Yüksek

# IF (Aftertaste Yüksek) and (Flavor Düşük) then Cupper.Points Orta
# IF (Aftertaste Yüksek) and (Flavor Orta) then Cupper.Points Yüksek
# IF (Aftertaste Yüksek) and (Flavor Yüksek) then Cupper.Points Yüksek

Uyelik Fonksyonlari
ucgenin trimf 6 7 8, 7 8 9, 8 9 10
AZ ORTA COK

degiskenlerde cup_points yerine cupper points te kullanilabilir
"""

#%% importlar

import numpy as np
import skfuzzy as fuzz
import pandas as pd
import matplotlib.pyplot as plt

#%% kullanilacak verilerin duzenlenmesi

column_list = ["Aftertaste", "Flavor", "Cupper.Points"]
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
df = df[df['Flavor'] > 6] 
print("onislemenden sonra shape: ", df.shape)

#%% uyelik fonksyonlarini olusturma

x_aftertaste = np.arange(6, 10.1, 0.1)
x_flavor = np.arange(6, 10.1, 0.1)
x_cup_points = np.arange(6, 10.1, 0.1)
    
aftertaste_D = fuzz.trimf(x_aftertaste, [6, 7, 8])
aftertaste_O = fuzz.trimf(x_aftertaste, [7, 8, 9])
aftertaste_Y = fuzz.trimf(x_aftertaste, [8, 9, 10])

flavor_D = fuzz.trimf(x_flavor, [6, 7, 8])
flavor_O = fuzz.trimf(x_flavor, [7, 8, 9])
flavor_Y = fuzz.trimf(x_flavor, [8, 9, 10])

cup_points_D = fuzz.trimf(x_cup_points, [6, 7, 8])
cup_points_O = fuzz.trimf(x_cup_points, [7, 8, 9])
cup_points_Y = fuzz.trimf(x_cup_points, [8, 9, 10])

for i in range(10):
    aftertaste_D[i] = 1 
    flavor_D[i] = 1
    cup_points_D[i] = 1
    
for i in range(30,41):
    aftertaste_Y[i] = 1
    flavor_Y[i] = 1 
    cup_points_Y[i] = 1


fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(12, 12))
ax0.plot(x_aftertaste, aftertaste_D, 'b', linewidth=1.5, label='Düşük')
ax0.plot(x_aftertaste, aftertaste_O, 'g', linewidth=1.5, label='Orta')
ax0.plot(x_aftertaste, aftertaste_Y, 'r', linewidth=1.5, label='Yüksek')
ax0.set_title('Aftertaste')
ax0.legend()

ax1.plot(x_flavor, flavor_D, 'b', linewidth=1.5, label='Düşük')
ax1.plot(x_flavor, flavor_O, 'g', linewidth=1.5, label='Orta')
ax1.plot(x_flavor, flavor_Y, 'r', linewidth=1.5, label='Yüksek')
ax1.set_title('Flavor')
ax1.legend()

ax2.plot(x_cup_points, cup_points_D, 'b', linewidth=1.5, label='Düşük')
ax2.plot(x_cup_points, cup_points_O, 'g', linewidth=1.5, label='Orta')
ax2.plot(x_cup_points, cup_points_Y, 'r', linewidth=1.5, label='Yüksek')
ax2.set_title('Cupper.Points')
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
flavor = random_row.iloc[0]['Flavor']
cup_points_org = random_row.iloc[0]['Cupper.Points']

# aftertaste =  6.92
# flavor =  6.92
# cup_points_org =  6.92

df.max(axis = 0) 
df.min(axis = 0) 

row_t  = (aftertaste, flavor, cup_points_org,)
print("random data sample")
print("Flavor: ", flavor )
print("Aftertaste: ", aftertaste)
print("Cupper.Points: ", cup_points_org)

#%% aftertaste memberships
aftertaste_level_D = fuzz.interp_membership(x_aftertaste, aftertaste_D, aftertaste)
aftertaste_level_O = fuzz.interp_membership(x_aftertaste, aftertaste_O, aftertaste)
aftertaste_level_Y = fuzz.interp_membership(x_aftertaste, aftertaste_Y, aftertaste)

print("membership aftertaste_level_D: ", aftertaste_level_D)
print("membership aftertaste_level_O: ", aftertaste_level_O)
print("membership aftertaste_level_Y: ", aftertaste_level_Y)

#%% flavor

flavor_level_D = fuzz.interp_membership(x_flavor, flavor_D, flavor)
flavor_level_O = fuzz.interp_membership(x_flavor, flavor_O, flavor)
flavor_level_Y = fuzz.interp_membership(x_flavor, flavor_Y, flavor)

print("membership flavor_level_D: ", flavor_level_D)
print("membership flavor_level_O: ", flavor_level_O)
print("membership flavor_level_Y: ", flavor_level_Y)
#%% fuzzy inference burayi anlamak lazim

active_rule1 = np.fmin(flavor_level_D, aftertaste_level_D)
active_rule2 = np.fmin(flavor_level_D, aftertaste_level_O)
active_rule3 = np.fmin(flavor_level_D, aftertaste_level_Y)

active_rule4 = np.fmin(flavor_level_O, aftertaste_level_D)
active_rule5 = np.fmin(flavor_level_O, aftertaste_level_O)
active_rule6 = np.fmin(flavor_level_O, aftertaste_level_Y)

active_rule7 = np.fmin(flavor_level_Y, aftertaste_level_Y)
active_rule8 = np.fmin(flavor_level_Y, aftertaste_level_Y)
active_rule9 = np.fmin(flavor_level_Y, aftertaste_level_Y)

cup_points_activation_1 = np.zeros_like(active_rule1)
if np.sum(np.fmin(active_rule1, cup_points_D)) > 0:
    cup_points_activation_1 = np.fmin(active_rule1, cup_points_D)

elif np.sum(np.fmin(active_rule2, cup_points_D)) > 0:
    cup_points_activation_1 = np.fmin(active_rule2, cup_points_D) 

elif np.sum(np.fmin(active_rule4, cup_points_D)) > 0:
    cup_points_activation_1 = np.fmin(active_rule4, cup_points_D)

cup_points_activation_2 = np.zeros_like(active_rule1)
if np.sum(np.fmin(active_rule3, cup_points_O)) > 0:
    cup_points_activation_2 = np.fmin(active_rule3, cup_points_O)

elif np.sum(np.fmin(active_rule5, cup_points_O)) > 0:
    cup_points_activation_2 = np.fmin(active_rule5, cup_points_O)
 
elif np.sum(np.fmin(active_rule7, cup_points_O)) > 0:
    cup_points_activation_2 = np.fmin(active_rule7, cup_points_O)
    
cup_points_activation_3 = np.zeros_like(active_rule1)
if np.sum(np.fmin(active_rule6, cup_points_Y)) > 0:
    cup_points_activation_3 = np.fmin(active_rule6, cup_points_Y)

elif np.sum(np.fmin(active_rule8, cup_points_Y)) > 0:
    cup_points_activation_3 = np.fmin(active_rule8, cup_points_Y) 

elif np.sum(np.fmin(active_rule9, cup_points_Y)) > 0:
    cup_points_activation_3 = np.fmin(active_rule9, cup_points_Y)   
    

#%% plot outputs

cup_points0 = np.zeros_like(x_cup_points)

fig, ax0 = plt.subplots(figsize=(10, 4))
ax0.set_title('Üyelik Aktivasyonu')
ax0.fill_between(x_cup_points, cup_points0, cup_points_activation_1, facecolor='b', alpha=0.7)
ax0.plot(x_cup_points, cup_points_Y, 'b', linewidth=0.5, linestyle=':', )

ax0.fill_between(x_cup_points, cup_points0, cup_points_activation_2, facecolor='g', alpha=0.7)
ax0.plot(x_cup_points, cup_points_O, 'g', linewidth=0.5, linestyle=':', )

ax0.fill_between(x_cup_points, cup_points0, cup_points_activation_3, facecolor='r', alpha=0.7)
ax0.plot(x_cup_points, cup_points_D, 'r', linewidth=0.5, linestyle=':', )


# Turn off top/right exes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout() 

aggregated = np.fmax (cup_points_activation_1, 
                      np.fmax(cup_points_activation_2, cup_points_activation_3)) 

cup_points_model = fuzz.defuzz(x_cup_points, aggregated, 'centroid')
# !!! cup_points_activation bunun olayini anlamak lazim
cup_points_activation = fuzz.interp_membership(x_cup_points, aggregated, cup_points_model)

print('cup_points model: ', cup_points_model)
print('cup_points original: ', cup_points_org)
print('model error', format(abs((cup_points_model - cup_points_org) / cup_points_org) * 100, '.4f'))


fig, ax0 = plt.subplots(figsize=(10, 4))
ax0.plot(x_cup_points, cup_points_D, 'b', linewidth=1.5, linestyle=':')
ax0.plot(x_cup_points, cup_points_O, 'g', linewidth=1.5, linestyle=':')
ax0.plot(x_cup_points, cup_points_Y, 'r', linewidth=1.5, linestyle=':')

ax0.fill_between(x_cup_points, cup_points0, aggregated, facecolor='cyan', alpha=0.7)
ax0.plot([cup_points_model, cup_points_model], [0, cup_points_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Üyeliklerin Kümelenmesi ve Durulama Çıktısı')

''' cup_points, fuzz.defuzz()

'''

''' aggregated, np.fmax()
    np.fmax() 
    npCompare two arrays and returns a new array containing the element-wise maxima
'''