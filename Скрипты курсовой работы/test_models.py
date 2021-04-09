import numpy as np
from scipy.integrate import odeint
import pandas as pd
from graph_model import *
from time_series import *
from get_data import Data
from display_result import *


def run_mod_SEIRD_real_data(country, officical_country, R0, alpha, beta, gamma, fi, mu, sigma, K0,
                  count_train, last_forecast_day):
    country = country
    official_country = officical_country

    data = Data.data_read_file(country)

    # Получаем данные для страны
    data_per_full_data_country = Data.full_data_country(official_country)
    country_population = data_per_full_data_country[0]
    country_land_area = data_per_full_data_country[1]
    country_density =data_per_full_data_country[2]
    country_urban_pop_rate = data_per_full_data_country[3]
    country_median_age = data_per_full_data_country[4]

    data_health_country = Data.data_health(country)
    data_health_ph_and_n_per_1000 = Data.data_health_nurse_and_physicians_per_1000(country)
    country_health_exp = data_health_country[0]
    country_health_per_pop = data_health_country[1]
    country_smokers = Data.data_smokers(country)
    country_nurse = data_health_ph_and_n_per_1000[0]
    country_physicians = data_health_ph_and_n_per_1000[1]

    average_time_recovered = 14
    average_days_before_infection = 5.2

    N = country_population
    I = int(data.head(count_train).tail()['Confirmed'].values[-1])
    E = R0 * I
    R = int(data.head(count_train).tail()['Recovered'].values[-1])
    D = int(data.head(count_train)['Deaths'].values[-1])
    S = N - I - E - R - D

    forecast_start_day = count_train
    forecast_end_day = last_forecast_day
    days = forecast_end_day - forecast_start_day
    start_day = 0
    end_day = forecast_end_day

    solve_SEIRD = SEIRD_model_with_exp(N,S,E,I,R,D,days, beta,alpha,gamma,mu,fi, sigma, K0)
    display_SEIRD(data, solve_SEIRD, country, forecast_start_day, forecast_end_day)


def run_SI():
     beta = 4 / 14
     gamma = 1 / 14

     country = 'Russia'
     official_country = 'Russian Federation'

     data = Data.data_read_file(country)
     data_per_full_data_country = Data.full_data_country(official_country)
     country_population = data_per_full_data_country[0]

     N = country_population
     I = int(data.head(40).tail()['Confirmed'].values[-1])
     S = N - I
     d = 41
     sec_d = 60

     solve_SI = SI_model(N, S, I, d, beta)
     sec_solve_SI = SI_model(N, S, I, sec_d, beta)
     display_SI(data, solve_SI, 40, d+40)
     display_SI(data, sec_solve_SI, 40, sec_d+40, True)


def run_SIR():
    beta = 4 / 14
    gamma = 1 / 14

    country = 'Russia'
    official_country = 'Russian Federation'

    data = Data.data_read_file(country)
    data_per_full_data_country = Data.full_data_country(official_country)
    country_population = data_per_full_data_country[0]

    N = country_population
    I = int(data.head(40).tail()['Confirmed'].values[-1])
    R = int(data.head(40).tail()['Recovered'].values[-1])
    S = N - I - R
    d = 41
    sec_d = 60

    solve_SIR = SIR_model(N, S, I, R, d, beta, gamma)
    display_SIR(data, solve_SIR, 40, d+40)

    solve_SIR = SIR_model(N, S, I, R, sec_d, beta, gamma)
    display_SIR(data, solve_SIR, 40, sec_d + 40)


def run_SEIR():
    beta = 4 / 14
    gamma = 1 / 14
    alpha = 1 / 5
    fi = 0.6

    country = 'Russia'
    official_country = 'Russian Federation'

    data = Data.data_read_file(country)
    data_per_full_data_country = Data.full_data_country(official_country)
    country_population = data_per_full_data_country[0]

    N = country_population
    I = int(data.head(40).tail()['Confirmed'].values[-1])
    R = int(data.head(40).tail()['Recovered'].values[-1])
    E = 3.5 * I
    S = N - I - R - E
    d = 41

    solve_SEIR = modificate_SEIR_model(N, S, E, I, R, d, fi, beta, gamma, alpha)
    display_SEIR(data, solve_SEIR, 40, d+40)


def run_SEIRD():
    beta = 4 / 14
    gamma = 1 / 14
    alpha = 1 / 5
    mu = gamma / 10
    fi = 0.6

    country = 'Russia'
    official_country = 'Russian Federation'

    data = Data.data_read_file(country)
    data_per_full_data_country = Data.full_data_country(official_country)
    country_population = data_per_full_data_country[0]

    N = country_population
    I = int(data.head(40).tail()['Confirmed'].values[-1])
    R = int(data.head(40).tail()['Recovered'].values[-1])
    D = int(data.head(40).tail()['Deaths'].values[-1])
    E = 3.5 * I
    S = N - I - R - E
    d = 41

    solve_SEIRD = SEIRD_model(N, S, E, I, R, D, d, beta, alpha, gamma, mu, fi)
    display_SEIRD(data, solve_SEIRD, None,40, d+40)


def run_time_series():
    country = 'Russia'
    official_country = 'Russian Federation'

    data = Data.data_read_file(country)
    data_per_full_data_country = Data.full_data_country(official_country)
    country_population = data_per_full_data_country[0]

    N = country_population
    real_values = data['Confirmed'].head(100).values
    date = data['ObservationDate'].head(100).values
    count_train = 40
    needed_days = 41
    train = real_values[:count_train]
    test = real_values[count_train:]
    param_forecast = moving_average_param(train, needed_days, 2)
    display_time_series(count_train, needed_days, real_values, param_forecast, date)


if __name__ == '__main__':
    run_SI()
    run_SIR()
    run_SEIR()
    run_SEIRD()
    run_time_series()
    run_mod_SEIRD_real_data('Spain', 'Spain', 3.2, 1 / 5, 2.595, 0.0238, 0.34, 0.005, 1 / 8.3, 1 / 3.5, 40, 81)
    run_mod_SEIRD_real_data('Russia', 'Russian Federation', 3.2, 1 / 5, 0.77, 0.0086, 0.2, 0.002, 1 / 8.1, 1 / 4.1, 40, 81)
    run_mod_SEIRD_real_data('Italy', 'Italy', 3.2, 1 / 5, 1.515, 0.0124, 0.2, 0.005, 1 / 8.59, 1 / 3.49, 40, 81)