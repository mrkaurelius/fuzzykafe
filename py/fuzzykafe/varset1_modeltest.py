"""
fuzzy modelin testi amacli, tum dataseti iterate eder
"""

#%% importlar

import numpy as np
import skfuzzy as fuzz
import pandas as pd

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

#%% iterate_dataset func

def iterate_dataset():
    
    df = preprocess_dataset()
    err_sum = 0

    for index, row in df.iterrows():
        
        aftertaste = row['Aftertaste']
        acidity = row['Acidity']
        flavor_org = row['Flavor']
        
        print(row['Aftertaste'], row['Acidity'], row['Flavor'])
        print("Acidity: ", acidity, "Aftertaste: ", aftertaste, "Flavor Org: ", flavor_org )
        
        flavor_model = fuzz_system(aftertaste, acidity)
        
        print('flavor model: ', flavor_model)
        print('flavor original: ', flavor_org)
        
        model_error = abs((flavor_model - flavor_org) / flavor_org) * 100
        err_sum += model_error
      
        print('model error', format(model_error, '.4f'))
        
    
    print('mean of model error: ', format(err_sum / df.shape[0], '.4f') )

#%% read_preprocess_dataset func
# kullanilacak verilerin duzenlenmesi

def preprocess_dataset():
    column_list = ["Aftertaste", "Acidity", "Flavor"]
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
    df = df[df['Acidity'] > 6] 

    print("0 degerler dusuruldukten sonra shape: ", df.shape)
    return df

#%% fuzzy fuc
# fuzzy islemlerini yap

def fuzz_system(aftertaste, acidity):
    aftertaste_level_D = fuzz.interp_membership(x_aftertaste, aftertaste_D, aftertaste)
    aftertaste_level_O = fuzz.interp_membership(x_aftertaste, aftertaste_O, aftertaste)
    aftertaste_level_Y = fuzz.interp_membership(x_aftertaste, aftertaste_Y, aftertaste)
    
    # print("membership aftertaste_level_D: ", aftertaste_level_D)
    # print("membership aftertaste_level_O: ", aftertaste_level_O)
    # print("membership aftertaste_level_Y: ", aftertaste_level_Y)
    
    acidity_level_D = fuzz.interp_membership(x_acidity, acidity_D, acidity)
    acidity_level_O = fuzz.interp_membership(x_acidity, acidity_O, acidity)
    acidity_level_Y = fuzz.interp_membership(x_acidity, acidity_Y, acidity)
    
    # print("membership acidity_level_D: ", acidity_level_D)
    # print("membership acidity_level_O: ", acidity_level_O)
    # print("membership acidity_level_Y: ", acidity_level_Y)
    
    active_rule1 = np.fmin(acidity_level_D, aftertaste_level_D)
    active_rule2 = np.fmin(acidity_level_O, aftertaste_level_O)
    active_rule3 = np.fmin(acidity_level_Y, aftertaste_level_Y)
    
    flavor_activation_1 = np.fmin(active_rule1, flavor_D)
    flavor_activation_2 = np.fmin(active_rule2, flavor_O)
    flavor_activation_3 = np.fmin(active_rule3, flavor_Y)
    
    # flavor0 = np.zeros_like(x_flavor)
    aggregated = np.fmax (flavor_activation_1, 
                      np.fmax(flavor_activation_2, flavor_activation_3)) 
    flavor_model = fuzz.defuzz(x_flavor, aggregated, 'centroid')
    # flavor_activation = wash_activation = fuzz.interp_membership(x_flavor, aggregated, flavor_model)
    
    return flavor_model


if __name__ == "__main__":
    iterate_dataset()



