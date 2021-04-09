import numpy as np
import matplotlib.pyplot as plt
from statsmodels import api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels

def read_file(country, region=None):
    data = pd.read_csv("csv_files/covid_19_data.csv")
    data_country = data[data['Country/Region'] == country]

    if region != None:
        data_region_country = data_country[data_country['Province/State'] == region]
        return data_region_country

    return data_country


a = read_file('Russia', 'Adygea Republic')['Confirmed'].head(40).values
train = a[:30]
test = a[30:]
print(test)

mod = sm.tsa.statespace.SARIMAX(train,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()
print(results.get_forecast(10,dynamic=True).conf_int().items)