import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd
from graph_model import *


def data_health(country):
    data = pd.read_csv("csv_files/2.12_Health_systems.csv")
    data_country = data[data['Country_Region'] == country]

    Health_exp_pct = data_country['Health_exp_pct_GDP_2016'].values
    Health_exp_public = data_country['Health_exp_public_pct_2016'].values
    Health_exp_out_of_pocket_pct_2016 = data_country['Health_exp_out_of_pocket_pct_2016'].values
    Physicians_per_1000 = data_country['Physicians_per_1000_2009-18'].values
    Nurse_per_1000 = data_country['Nurse_midwife_per_1000_2009-18'].values

    return(Health_exp_pct, Health_exp_public, Health_exp_out_of_pocket_pct_2016, Physicians_per_1000, Nurse_per_1000)


def data_smokers(country):
    data = pd.read_csv("csv_files/share-of-adults-who-smoke.csv")
    data_country = data[data['Entity'] == country]
    data_country = data_country[data_country['Year'] == 2016].values[0][-1]

    print(data_country)


def data_by_age(country):
    data = pd.read_csv("csv_files/WorldPopulationByAge2020.csv")
    data_country = data[data['Location'] == country]

    print(data_country)


def full_data_country(country):
    data = pd.read_csv("csv_files/countries.csv")
    data_country = data[data['name'] == country]

    return data_country['land_area'].values[0]/data_country['population'].values[0]


def data_russian_region(region):
    data = pd.read_csv("csv_files/russia_regions.csv")
    data_region = data[data['name'] == region]

    print(data_region)


def data_health_per_pop_country(country):
    data = pd.read_csv("csv_files/covid19countryinfo.csv")
    data_country = data[data['country'] == country]

    print(float(data_country['healthexp'].values[0].replace(',','.')))


# country = 'Italy'
# a = data_health(country)
# print(1/sum(a),'\n\n')
# b = data_health('Russia')
# print(1/sum(b),'\n\n')
# data_smokers(country)
# print()
# data_by_age(country)
# print()
# print(sum(a) * full_data_country(country))
# print(sum(b) * full_data_country('Russian Federation'))

data_health_per_pop_country('Russia')
data_health_per_pop_country('Italy')