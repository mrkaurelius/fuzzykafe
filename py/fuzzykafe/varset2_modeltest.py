"""
fuzzy modelin testi amacli, tum dataseti iterate eder
"""

#%% importlar

import numpy as np
import skfuzzy as fuzz
import pandas as pd

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
    
    
#%% iterate_dataset func

def iterate_dataset():
    
    df = preprocess_dataset()
    err_sum = 0

    for index, row in df.iterrows():
        
        aftertaste = row['Aftertaste']
        flavor = row['Flavor']
        cup_points_org = row['Cupper.Points']
        
        # print(row['Aftertaste'], row['Acidity'], row['Cupper.Points'])
        print("Flavor: ", flavor, "Aftertaste: ", aftertaste, "Cupper.Points Org: ", cup_points_org )
        
        cup_points_model = fuzz_system(aftertaste, flavor)
        
        print('cup_points model: ', cup_points_model)
        print('cup_points original: ', cup_points_org)
        
        model_error = abs((cup_points_model - cup_points_org)) / cup_points_org * 100
        err_sum += model_error
      
        print('model error', format(model_error, '.4f'))
        
    
    print('mean of model error: ', format(err_sum / df.shape[0], '.4f') )

#%% read_preprocess_dataset func
# kullanilacak verilerin duzenlenmesi

def preprocess_dataset():
    column_list = ["Aftertaste", "Flavor", "Cupper.Points"]
    df = pd.read_csv("../../data/merged_data_cleaned.csv", usecols = column_list)
    
    columns = df.columns
    print("columns: ", columns)  # columns
    print("raw shape", df.shape)
    
    # drop null/na
    df = df.dropna()
    # drop zeros
    df = df[(df.T != 0).any()]
    
    # filter values
    df = df[df['Aftertaste'] > 6] 
    df = df[df['Flavor'] > 6] 

    print("onislemenden sonra shape: ", df.shape)
    return df

#%% fuzzy fuc
# fuzzy islemlerini yap

def fuzz_system(aftertaste, flavor):
    aftertaste_level_D = fuzz.interp_membership(x_aftertaste, aftertaste_D, aftertaste)
    aftertaste_level_O = fuzz.interp_membership(x_aftertaste, aftertaste_O, aftertaste)
    aftertaste_level_Y = fuzz.interp_membership(x_aftertaste, aftertaste_Y, aftertaste)
    
    flavor_level_D = fuzz.interp_membership(x_flavor, flavor_D, flavor)
    flavor_level_O = fuzz.interp_membership(x_flavor, flavor_O, flavor)
    flavor_level_Y = fuzz.interp_membership(x_flavor, flavor_Y, flavor)
  
    
    rule1 = np.fmin(flavor_level_D, aftertaste_level_D)
    rule2 = np.fmin(flavor_level_D, aftertaste_level_O)
    rule3 = np.fmin(flavor_level_D, aftertaste_level_Y)
    
    rule4 = np.fmin(flavor_level_O, aftertaste_level_D)
    rule5 = np.fmin(flavor_level_O, aftertaste_level_O)
    rule6 = np.fmin(flavor_level_O, aftertaste_level_Y)
    
    rule7 = np.fmin(flavor_level_Y, aftertaste_level_D)
    rule8 = np.fmin(flavor_level_Y, aftertaste_level_O)
    rule9 = np.fmin(flavor_level_Y, aftertaste_level_Y)
    
    cup_points_activation_1 = np.zeros_like(rule1)
    if np.sum(np.fmin(rule1, cup_points_D)) > 0:
        cup_points_activation_1 = np.fmin(rule1, cup_points_D)
    
    elif np.sum(np.fmin(rule2, cup_points_D)) > 0:
        cup_points_activation_1 = np.fmin(rule2, cup_points_D) 
    
    elif np.sum(np.fmin(rule4, cup_points_D)) > 0:
        cup_points_activation_1 = np.fmin(rule4, cup_points_D)
    
    cup_points_activation_2 = np.zeros_like(rule1)
    if np.sum(np.fmin(rule3, cup_points_O)) > 0:
        cup_points_activation_2 = np.fmin(rule3, cup_points_O)
    
    elif np.sum(np.fmin(rule5, cup_points_O)) > 0:
        cup_points_activation_2 = np.fmin(rule5, cup_points_O)
     
    elif np.sum(np.fmin(rule7, cup_points_O)) > 0:
        cup_points_activation_2 = np.fmin(rule7, cup_points_O)
        
    cup_points_activation_3 = np.zeros_like(rule1)
    if np.sum(np.fmin(rule6, cup_points_Y)) > 0:
        cup_points_activation_3 = np.fmin(rule6, cup_points_Y)
    
    elif np.sum(np.fmin(rule8, cup_points_Y)) > 0:
        cup_points_activation_3 = np.fmin(rule8, cup_points_Y) 
    
    elif np.sum(np.fmin(rule9, cup_points_Y)) > 0:
        cup_points_activation_3 = np.fmin(rule9, cup_points_Y)
    
    # cup_points0 = np.zeros_like(x_cup_points)
    aggregated = np.fmax (cup_points_activation_1, 
                      np.fmax(cup_points_activation_2, cup_points_activation_3)) 
    cup_points_model = fuzz.defuzz(x_cup_points, aggregated, 'centroid')
    # cup_points_activation = wash_activation = fuzz.interp_membership(x_cup_points, aggregated, cup_points_model)
    
    return cup_points_model


if __name__ == "__main__":
    iterate_dataset()