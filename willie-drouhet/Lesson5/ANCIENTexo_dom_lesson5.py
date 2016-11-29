# -*- coding: utf-8 -*-

# Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires ? Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les dépassement d'honoraires ? Est ce que la densité de certains médecins / praticiens est corrélé à la densité de population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

#lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Recuperation des données du fichier csv R2015
#    '/Users/Bense/Documents/Exercices/Charles/TP5/R2015_sans_lib/R201501_sanslib.CSV', delimiter=';')
#dataFrame_final_r2015 = pd.read_csv('rpps-medecins-tab7_36171637131987.csv', delimiter=',')
dataFrame_final_r2015 = pd.read_csv('density.csv', delimiter=',',skiprows=3)
print dataFrame_final_r2015
print "dataFrame_final_r2015"
raw_input()

file_name_honoraires = 'depass.csv'
df_depass = pd.read_csv(file_name_honoraires, delimiter=',',skiprows=3)
print df_depass
print "df_depass"
raw_input()

# Recuperation du fichier d'honoraires en format excel
#file_name_honoraires = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'
honoraires_data = pd.ExcelFile(file_name_honoraires)
honoraires_data_generalistes = honoraires_data.parse('Généralistes et MEP')
honoraires_data_specialistes = honoraires_data.parse('Spécialistes')
print honoraires_data
print "honoraires_data"
raw_input()



# Recuperation des equivalents du code CPAM
cpam_variable = pd.read_excel(
    '/Users/Documents/Exercices/Charles/TP5/R2015_sans_lib/descriptif_table_R.xls', sheetname=4)
cpam_variable.columns = ['cpam', 'region']
cpam_variable.set_index('cpam')

result = pd.merge(dataFrame_final_r2015, cpam_variable, on='cpam')

# Recuperation du fichier d'honoraires en format excel
file_name_honoraires = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls'
honoraires_data = pd.ExcelFile(honoraires_file)
honoraires_data_generalistes = honoraires_data.parse('Généralistes et MEP')
honoraires_data_specialistes = honoraires_data.parse('Spécialistes')

file_name_densite = './sante/Effectif_et_densite_par_departement_en_2014.xls'
densite_data = pd.ExcelFile(file_name_densite)
densite_data_generalistes = densite_data.parse('Généralistes et MEP')
densite_data_specialistes = densite_data.parse('Spécialistes')

file_name_income = './sante/base-cc-filosofi-13.xls'
income_data = pd.ExcelFile(file_name_income)
dataFrame_final_income = income_data.parse('DEP', skiprows=3, header=2)

for i in range(5, 12):
    del densite_data_specialistes['Unnamed: ' + str(i)]

honoraires_data_generalistes.rename(
    columns={'Généralistes et compétences MEP': 'Spécialité'}, inplace=True)
honoraires_data_specialistes.rename(
    columns={'Spécialistes': 'Spécialité'}, inplace=True)
densite_data_generalistes.rename(
    columns={'Généralistes et compétences MEP': 'Spécialité'}, inplace=True)
densite_data_specialistes.rename(
    columns={'Spécialistes': 'Spécialité'}, inplace=True)

dataFrame_densite = pd.concat(
    [densite_data_specialistes, densite_data_generalistes])
dataFrame_honoraires = pd.concat([honoraires_data_specialistes,
                                  honoraires_data_generalistes])

dataFrame_densite.rename(columns={'EFFECTIF': 'EFFECTIFS'}, inplace=True)

dataFrame_final = pd.merge(dataFrame_densite, dataFrame_honoraires)

dataFrame_final['EFFECTIFS'] = dataFrame_final['EFFECTIFS'].astype('float64')
dataFrame_final['EFFECTIFS'] = dataFrame_final[
    'EFFECTIFS'].replace({0: np.nan})
dataFrame_final['TOTAL DES HONORAIRES (Euros)'] = dataFrame_final[
    'TOTAL DES HONORAIRES (Euros)'].replace({'nc': np.nan})
dataFrame_final['DEPASSEMENTS (Euros)'] = dataFrame_final[
    'DEPASSEMENTS (Euros)'].replace({'nc': np.nan})

dataFrame_final['Honoraires totaux par médecin'] = dataFrame_final[
    'TOTAL DES HONORAIRES (Euros)'] / dataFrame_final['EFFECTIFS'].replace({0: np.nan})

dataFrame_final['Pct dépassement'] = dataFrame_final[
    'DEPASSEMENTS (Euros)'] / dataFrame_final['TOTAL DES HONORAIRES (Euros)']

dataFrame_finaldrop = dataFrame_final.drop(
dataFrame_final[np.isnan(dataFrame_final['Pct dépassement'])].index)