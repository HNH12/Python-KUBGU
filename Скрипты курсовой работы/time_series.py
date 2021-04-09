import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels


def moving_average(test, needed, count_days):
    n_d = list(test[-count_days:])
    forecast = list()
    for i in range(needed):
        forecast.append((1/count_days) * sum(n_d[-count_days:]))
        n_d.append(forecast[i])
    return forecast


def moving_average_param(test, needed, count_days):
    n_d = list(test[-count_days:])
    forecast = list()
    for i in range(needed):
        w = list()
        for j in range(count_days):
            w.append(1)
        w[count_days-1] = 1.311
        for j in range(1,count_days+1):
            n_d[-j] = n_d[-j]*w[-j]
        forecast.append((1 / count_days) * sum(n_d[-count_days:]))
        n_d.append(forecast[i])
    return forecast