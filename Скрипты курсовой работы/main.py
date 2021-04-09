import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.integrate import odeint
import pandas as pd
from graph_model import *
from time_series import *


def show_result_model(attribute, time_period, forecast_time_period, value_model, real_value, model, country):
    mpl.rcParams['figure.figsize'] = [12.0, 5.0]
    mpl.rcParams['figure.dpi'] = 100

    plt.title(model + ' ' + country, fontsize=14)
    plt.plot(time_period, real_value.head(len(time_period))[attribute].values, 'o:')
    plt.plot(forecast_time_period, value_model, 'o:')

    plt.legend(("{0} (Real)".format(attribute),
                "{0} ({1})".format(attribute, model)))

    plt.xlabel('Дни')
    plt.ylabel('Число подтвержденных случаев')

    plt.show()


def show_result_SEIRD(attribute, time_period, forecast_time_period, seird, real_value, model, country):
    mpl.rcParams['figure.figsize'] = [12.0, 5.0]
    mpl.rcParams['figure.dpi'] = 100

    con_value_SEIRD = list()
    death_value_SEIRD = list()
    rec_value_SEIRD = list()
    for i in range(len(seird)):
        death_value_SEIRD.append(seird[i][4])
        con_value_SEIRD.append(seird[i][2])
        rec_value_SEIRD.append(seird[i][3])

    plt.title(model + ' ' + country, fontsize=14)
    plt.plot(time_period, real_value.head(len(time_period))[attribute], 'o:')
    plt.plot(forecast_time_period, con_value_SEIRD, 'o:')
    plt.plot(time_period, real_value.head(len(time_period))['Recovered'], 's:')
    plt.plot(forecast_time_period, rec_value_SEIRD, 's:')
    plt.plot(time_period, real_value.head(len(time_period))['Deaths'], 'x:')
    plt.plot(forecast_time_period, death_value_SEIRD, 'x:')

    plt.legend(("{0} (Real)".format(attribute),
                "{0} ({1})".format(attribute, model),
                "Recovered (Real)",
                "Recovered ({})".format(model),
                "Deaths (Real)",
                "Deaths ({})".format(model)))

    plt.show()


def displaying_graphs_model(attribute, real_value, value_SIS, value_SIR, value_SEIR, value_modificate_SEIR, rec_solve_SEIR,
                            forecast_start_day, forecast_end_day, SEIRD, SEIRD_with_smoothing, SEIRD_with_exp, country,
                            end_day = None, start_day = None):
    if end_day == None:
        end_day = forecast_end_day
    if start_day == None:
        start_day = 0

    forecast_time_period = list(range(forecast_start_day, forecast_end_day))
    time_period = list(range(start_day, end_day))

    show_result_model(attribute,time_period, forecast_time_period, value_SIR, real_value, 'SIR', country)
    show_result_model(attribute, time_period, forecast_time_period, value_SIS, real_value, 'SIS', country)
    show_result_model(attribute, time_period, forecast_time_period, value_SEIR, real_value, 'SEIR', country)
    show_result_model(attribute, time_period, forecast_time_period, value_modificate_SEIR, real_value, 'mod. SEIR', country)

    show_result_SEIRD(attribute, time_period, forecast_time_period, SEIRD, real_value, 'SEIRD', country)
    show_result_SEIRD(attribute, time_period, forecast_time_period, SEIRD_with_smoothing, real_value, 'SEIRD with smoothing', country)
    show_result_SEIRD(attribute, time_period, forecast_time_period, SEIRD_with_exp, real_value, 'SEIRD with exp', country)



def get_attribute_value_graph_model(attribute, value_SIS, value_SIR, value_SEIR, value_mod_SEIR):
    if attribute == 'Confirmed':
        con_value_SIS = list()
        for i in range(len(value_SIS)):
            con_value_SIS.append(value_SIS[i][1])

        con_value_SIR = list()
        for i in range(len(value_SIR)):
            con_value_SIR.append(value_SIR[i][1])

        con_value_SEIR = list()
        rec_value_SEIR = list()
        for i in range(len(value_SEIR)):
            con_value_SEIR.append(value_SEIR[i][2])
            rec_value_SEIR.append(value_SEIR[i][3])

        con_value_mod_SEIR = list()
        for i in range(len(value_mod_SEIR)):
            con_value_mod_SEIR.append(value_mod_SEIR[i][2])

        return con_value_SIS, con_value_SIR, con_value_SEIR, con_value_mod_SEIR, rec_value_SEIR


def read_file(country, region=None):
    data = pd.read_csv("csv_files/covid_19_data.csv")
    data_country = data[data['Country/Region'] == country]

    if region != None:
        data_region_country = data_country[data_country['Province/State'] == region]
        return data_region_country

    return data_country


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

    return float(data_country)


def data_by_age(country):
    data = pd.read_csv("csv_files/WorldPopulationByAge2020.csv")
    data_country = data[data['Location'] == country]

    print(data_country)


def full_data_country(country):
    data = pd.read_csv("csv_files/countries.csv")
    data_country = data[data['name'] == country]

    return data_country['population'].values[0], data_country['land_area'].values[0], \
           data_country['density'].values[0], data_country['urban_pop_rate'].values[0], \
           data_country['median_age'].values[0]


def data_russian_region(region):
    data = pd.read_csv("csv_files/russia_regions.csv")
    data_region = data[data['name'] == region]

    print(data_region)


def data_health_nurse_and_physicians_per_1000(country):
    data = pd.read_csv("csv_files/2.12_Health_systems.csv")
    data_country = data[data['Country_Region'] == country]

    Health_exp_pct = data_country['Health_exp_pct_GDP_2016'].values
    Health_exp_public = data_country['Health_exp_public_pct_2016'].values
    Health_exp_out_of_pocket_pct_2016 = data_country['Health_exp_out_of_pocket_pct_2016'].values
    Physicians_per_1000 = data_country['Physicians_per_1000_2009-18'].values[0]
    Nurse_per_1000 = data_country['Nurse_midwife_per_1000_2009-18'].values[0]

    return Nurse_per_1000,Physicians_per_1000


def data_health(country):
    data = pd.read_csv("csv_files/covid19countryinfo.csv")
    data_country = data[data['country'] == country]

    return int(data_country['healthexp'].values[0].replace(',','')), float(data_country['healthperpop'].values[0])


def solve_graph_model(N,S1,S2,S3,E,I,R,d,fi,alpha,beta,gamma):
    solve_SIS = SIS_model(N, S3, I, d, beta, gamma)
    solve_SIR = SIR_model(N, S2, I, R, d, beta, gamma, alpha)
    solve_SEIR = SEIR_model(N, S1, E, I, R, d, beta, gamma, alpha)
    solve_mod_SEIR = modificate_SEIR_model(N, S1, E, I, R, d, fi, beta, gamma, alpha)
    return solve_SIS,solve_SIR,solve_SEIR,solve_mod_SEIR


def start_program():
    # country = 'Russia'
    # official_country = 'Russian Federation'

    country = 'Japan'
    official_country = country

    # country = 'Spain'
    # official_country = country

    data = read_file(country)

    # Получаем данные для страны
    data_per_full_data_country = full_data_country(official_country)
    country_population = data_per_full_data_country[0]
    country_land_area = data_per_full_data_country[1]
    country_density = data_per_full_data_country[2]
    country_urban_pop_rate = data_per_full_data_country[3]
    country_median_age = data_per_full_data_country[4]

    data_health_country = data_health(country)
    data_health_ph_and_n_per_1000 = data_health_nurse_and_physicians_per_1000(country)
    country_health_exp = data_health_country[0]
    country_health_per_pop = data_health_country[1]
    country_smokers = data_smokers(country)
    country_nurse = data_health_ph_and_n_per_1000[0]
    country_physicians = data_health_ph_and_n_per_1000[1]

    average_time_recovered = 14
    average_days_before_infection = 5.2
    R0 = 3.2

    print('Площадь: {}\nНаселение: {}\nПлотность населения:{}\nСредний возраст: {}'
          '\nДоля городского населения: {}\n'.format(
        country_land_area, country_population, country_density, country_median_age,country_urban_pop_rate)
    )
    print('Медицинский опыт: {}\nДоля медицины на население: {}\nПроцент курящих: {}\n'.format(
        country_health_exp, country_health_per_pop, country_smokers)
    )
    print('Кол-во врачей на 1000: {}\nКол-во медсестер на 1000: {}\n'.format(
        country_physicians, country_nurse
    ))

    N = country_population

    count_train = 40
    I = int(data.head(count_train).tail()['Confirmed'].values[-1])
    E = R0 * I
    R = int(data.head(count_train).tail()['Recovered'].values[-1])
    D = int(data.head(count_train)['Deaths'].values[-1])

    mu = 0.0020
    fi = 0.20
    alpha = 1/5
    beta = 0.715
    gamma = ((country_health_per_pop/14)*(1/((country_health_exp/1000)*60)))
    print(gamma)

    # # gamma = 0.0112
    # # (country_health_per_pop/18) * (1/(RO*(country_percent_very_old + country_percent_old + country_percent_middle))

    # Italy
    # mu = 0.0050
    # fi = 0.20
    # alpha = 1 / 5
    # beta = 1.515
    # gamma = ((country_health_per_pop / 18) * (1 / ((country_health_exp / 1000) * 80)))

    # # Spain
    # mu = 0.0050
    # fi = 0.20
    # alpha = 1 / 6
    # beta = 2.295
    # gamma = ((country_health_per_pop / 18) * (1 / ((country_health_exp / 1000) * 55)))

    S1 = N - (I + E + R)
    S2 = N - (I + R)
    S3 = N - I
    S4 = N - (I + E + R + D)

    forecast_start_day = count_train
    forecast_end_day = 100
    days = forecast_end_day - forecast_start_day
    start_day = 0
    end_day = 100
    attribute = 'Confirmed'

    solve_SI, solve_SIR, solve_SEIR, solve_mod_SEIR = \
        solve_graph_model(N,S1,S2,S3,E,I,R,days,fi,alpha,beta,gamma)

    att_solve_SI, att_solve_SIR, att_solve_SEIR, att_solve_mod_SEIR, rec_solve_SEIR = \
        get_attribute_value_graph_model(attribute, solve_SIS, solve_SIR, solve_SEIR, solve_mod_SEIR)

    SEIRD = SEIRD_model(N, S4, E, I, R, D, days,
                beta, alpha, gamma, mu)

    SEIRD_with_smoothing = SEIRD_model_with_smoothing(N, S4, E, I, R, D, days,
                beta, alpha, gamma, mu, fi, 0.0504)

    SEIRD_with_exp = SEIRD_model_with_exp(N, S4, E, I, R, D, days,
                beta, alpha, gamma, mu, fi)

    displaying_graphs_model(attribute, data, att_solve_SIS, att_solve_SIR, att_solve_SEIR, att_solve_mod_SEIR,
                            rec_solve_SEIR, forecast_start_day, forecast_end_day, SEIRD, SEIRD_with_smoothing,
                            SEIRD_with_exp, country, end_day, start_day)


def display_SI(real_value, value_SI, start_time, time, R=False, E=False):
    # mpl.rcParams['figure.figsize'] = [12.0, 5.0]
    # mpl.rcParams['figure.dpi'] = 100
    SI_confirmed = list()
    SI_sus = list()
    for i in range(len(value_SI)):
        SI_confirmed.append(value_SI[i][1])
        SI_sus.append(value_SI[i][0])
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(real_value.head(start_time+time)['ObservationDate'].values[start_time:], real_value.head(start_time + time)['Confirmed'].values[start_time:], 'o:')
    ax.plot(real_value.head(start_time+time)['ObservationDate'].values[start_time:], SI_confirmed, 'o:')
    ax.plot(real_value.head(start_time + time)['ObservationDate'].values[start_time:], SI_sus, 'o:')
    ax.legend(("{0} (Real)".format('Confirmed'),
                "{0} ({1})".format('Confirmed', 'SI'),
               "Susceptible (SI)"))

    ax.set_xlabel('Дни')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def display_SIR(real_value, value_SI, start_time, time, model, R=False, E=False, D=False):
    # mpl.rcParams['figure.figsize'] = [12.0, 5.0]
    # mpl.rcParams['figure.dpi'] = 100
    SI_confirmed = list()
    for i in range(len(value_SI)):
        SI_confirmed.append(value_SI[i][1])
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(real_value.head(start_time+time)['ObservationDate'].values[start_time:], real_value.head(start_time + time)['Confirmed'].values[start_time:], 'o:')
    ax.plot(real_value.head(start_time+time)['ObservationDate'].values[start_time:], SI_confirmed, 'o:')
    if R:
        SI_recovered = list()
        for i in range(len(value_SI)):
            if E:
                SI_recovered.append(value_SI[i][3])
            else:
                SI_recovered.append(value_SI[i][2])
        ax.plot(real_value.head(start_time + time)['ObservationDate'].values[start_time:], real_value.head(start_time + time)['Recovered'].values[start_time:], 'o:')
        ax.plot(real_value.head(start_time + time)['ObservationDate'].values[start_time:], SI_recovered, 'o:')
        SI_deaths = list()
        if D:
            for i in range(len(value_SI)):
                SI_deaths.append(value_SI[i][4])
            ax.plot(real_value.head(start_time + time)['ObservationDate'].values[start_time:],
                   real_value.head(start_time + time)['Deaths'].values[start_time:], 'o:')
            ax.plot(real_value.head(start_time + time)['ObservationDate'].values[start_time:], SI_deaths, 'o:')

    ax.legend(("{0} (Real)".format('Confirmed'),
                "{0} ({1})".format('Confirmed', model),
               "Recovered (real)",
               "Recovered (model)",
               "Deaths (real)",
               "Deaths (SEIRD)"))

    ax.set_xlabel('Дни')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def graphics(start, count, real, forec, date):
    # mpl.rcParams['figure.figsize'] = [12.0, 5.0]
    # mpl.rcParams['figure.dpi'] = 100
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(date[start:], real[start:(start+count)], 's:')
    ax.plot(date[start:], forec, 'o:')

    ax.legend(("Real",
                "Forecast"))

    ax.set_xlabel('Дни')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.show()



def run_SI():
    beta = 4/14
    gamma = 1/14
    data = read_file('Russia')
    data_per_full_data_country = full_data_country('Russian Federation')
    N = data_per_full_data_country[0]
    I = int(data.head(40).tail()['Confirmed'].values[-1])

    S = N - I
    d = 60
    solve_SI = SI_model(N, S, I, d, beta)
    display_SI(data, solve_SI, 40, d)


def run_SIR():
    beta = 4/14
    gamma = 1/14
    data = read_file('Russia')
    data_per_full_data_country = full_data_country('Russian Federation')
    N = data_per_full_data_country[0]
    I = int(data.head(40).tail()['Confirmed'].values[-1])
    R = int(data.head(40).tail()['Recovered'].values[-1])
    S = N - I - R
    d = 41
    solve_SIS = SIR_model(N, S, I, R, d, beta, gamma)
    display_SIR(data, solve_SIS, 40, d, 'SIR', R=True)


def run_SEIR():
    beta = 4/14
    gamma = 1/14
    alpha = 1/5
    fi = 0.6
    data = read_file('Russia')
    data_per_full_data_country = full_data_country('Russian Federation')
    N = data_per_full_data_country[0]
    I = int(data.head(40).tail()['Confirmed'].values[-1])
    R = int(data.head(40).tail()['Recovered'].values[-1])
    E = 2.5*I
    S = N - I - R - E
    d = 41
    solve_SIS = modificate_SEIR_model(N, S, E, I, R, d, fi, beta, gamma, alpha)
    display_SIR(data, solve_SIS, 40, d, 'SEIR', R=True,E=True)


def run_SEIRD():
    beta = 4/14
    gamma = 1/14
    alpha = 1/5
    mu = gamma/10
    fi = 0.6
    data = read_file('Russia')
    data_per_full_data_country = full_data_country('Russian Federation')
    N = data_per_full_data_country[0]
    I = int(data.head(40).tail()['Confirmed'].values[-1])
    R = int(data.head(40).tail()['Recovered'].values[-1])
    D = int(data.head(40).tail()['Deaths'].values[-1])
    E = 2.5*I
    S = N - I - R - E
    d = 60
    solve_SIS = SEIRD_model(N, S, E, I, R, D, d, beta, alpha, gamma, mu, fi)
    display_SIR(data, solve_SIS, 40, d, 'SEIRD', R=True,E=True,D=True)


def run_time_series():
    data = read_file('Russia')
    data_per_full_data_country = full_data_country('Russian Federation')
    N = data_per_full_data_country[0]
    a = read_file('Russia')['Confirmed'].head(100).values
    date = read_file('Russia')['ObservationDate'].head(100).values
    count_train = 40
    needed_days = 60
    train = a[:count_train]
    test = a[count_train:]
    param_forecast = moving_average_param(train, needed_days, 2)
    graphics(count_train, needed_days, a, param_forecast, date)


def display_SEIRD(real_value, solve_SEIRD, start, end):
    fig, ax = plt.subplots(figsize=(12, 5))
    SEIRD_confirmed = list()
    SEIRD_recovered = list()
    SEIRD_deaths = list()
    for i in range(len(solve_SEIRD)):
        SEIRD_confirmed.append(solve_SEIRD[i][2])
        SEIRD_recovered.append(solve_SEIRD[i][3])
        SEIRD_deaths.append(solve_SEIRD[i][4])

    ax.plot(real_value.head(end)['ObservationDate'].values[start:], real_value.head(end)['Confirmed'].values[start:], 'o:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIRD_confirmed, 'o:')

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Recovered'].values[start:], 's:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIRD_recovered, 's:')

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Deaths'].values[start:], 'x:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIRD_deaths, 'x:')

    ax.legend(("{0} (Real)".format('Confirmed'),
               "{0} (SEIRD)".format('Confirmed'),
               "Recovered (real)",
               "Recovered (SEIRD)",
               "Deaths (real)",
               "Deaths (SEIRD)"))

    ax.set_xlabel('Дни')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def run_mod_SEIRD():
    country = 'Italy'
    official_country = 'Italy'

    data = read_file(country)

    # Получаем данные для страны
    data_per_full_data_country = full_data_country(official_country)
    country_population = data_per_full_data_country[0]
    country_land_area = data_per_full_data_country[1]
    country_density = data_per_full_data_country[2]
    country_urban_pop_rate = data_per_full_data_country[3]
    country_median_age = data_per_full_data_country[4]

    data_health_country = data_health(country)
    data_health_ph_and_n_per_1000 = data_health_nurse_and_physicians_per_1000(country)
    country_health_exp = data_health_country[0]
    country_health_per_pop = data_health_country[1]
    country_smokers = data_smokers(country)
    country_nurse = data_health_ph_and_n_per_1000[0]
    country_physicians = data_health_ph_and_n_per_1000[1]

    average_time_recovered = 14
    average_days_before_infection = 5.2
    R0 = 3.2

    print('Площадь: {}\nНаселение: {}\nПлотность населения:{}\nСредний возраст: {}'
          '\nДоля городского населения: {}\n'.format(
        country_land_area, country_population, country_density, country_median_age, country_urban_pop_rate)
    )
    print('Медицинский опыт: {}\nДоля медицины на население: {}\nПроцент курящих: {}\n'.format(
        country_health_exp, country_health_per_pop, country_smokers)
    )
    print('Кол-во врачей на 1000: {}\nКол-во медсестер на 1000: {}\n'.format(
        country_physicians, country_nurse
    ))

    N = country_population

    count_train = 40
    I = int(data.head(count_train).tail()['Confirmed'].values[-1])
    E = R0 * I
    R = int(data.head(count_train).tail()['Recovered'].values[-1])
    D = int(data.head(count_train)['Deaths'].values[-1])
    S = N - I - E - R - D
    #Russia
    # mu = 0.0020
    # fi = 0.20
    # alpha = 1 / 5
    # beta = 0.770
    # gamma = ((country_health_per_pop / 14) * (1 / ((country_health_exp / 1000) * 48)))
    #Italy
    # mu = 0.0050
    # fi = 0.20
    # alpha = 1 / 5
    # beta = 1.515
    # gamma = ((country_health_per_pop / 18) * (1 / ((country_health_exp / 1000) * 80)))
    #Spain
    mu = 0.0050
    fi = 0.34
    alpha = 1 / 5
    beta = 2.595
    gamma = ((country_health_per_pop / 18) * (1 / ((country_health_exp / 1000) * 50)))
    print('1 ' + str(gamma))

    forecast_start_day = count_train
    forecast_end_day = 81
    days = forecast_end_day - forecast_start_day
    start_day = 0
    end_day = 81
    attribute = 'Confirmed'
    solve_SEIRD = SEIRD_model_with_exp(N,S,E,I,R,D,days, beta,alpha,gamma,mu,fi)
    display_SEIRD(data, solve_SEIRD, forecast_start_day, forecast_end_day)


if __name__ == '__main__':
    # run_SI()
    # run_SIR()
    # run_SEIR()
    # run_SEIRD()
    # run_time_series()
    run_mod_SEIRD()
