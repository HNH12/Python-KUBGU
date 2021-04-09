import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def MAPE(real, forecast):
    n = len(real)
    sum = 0
    for i in range(n):
        sum += abs(real[i] - forecast[i]) / (real[i] if real[i] !=0 else 1)
    return (sum / n)*100


def display_SEIRD(real_value, solve_SEIRD, country, start, end):
    SEIRD_confirmed = list()
    SEIRD_recovered = list()
    SEIRD_deaths = list()
    for i in range(len(solve_SEIRD)):
        SEIRD_confirmed.append(solve_SEIRD[i][2])
        SEIRD_recovered.append(solve_SEIRD[i][3])
        SEIRD_deaths.append(solve_SEIRD[i][4])

    fig, ax = plt.subplots(figsize=(12, 5))
    if country == 'Russia':
        ax.set_title('Модель SEIRD для России')
    elif country == 'Italy':
        ax.set_title('Модель SEIRD для Италии')
    elif country == 'Spain':
        ax.set_title('Модель SEIRD для Испании')
    else:
        ax.set_title('Модель SEIRD')

    mape_confirmed = round(MAPE(real_value.head(end)['Confirmed'].values[start:],SEIRD_confirmed), 5)
    mape_recovered = round(MAPE(real_value.head(end)['Recovered'].values[start:], SEIRD_recovered), 5)
    mape_deaths = round(MAPE(real_value.head(end)['Deaths'].values[start:], SEIRD_deaths), 5)

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Confirmed'].values[start:], 'o:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIRD_confirmed, 'o:')

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Recovered'].values[start:], 's:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIRD_recovered, 's:')

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Deaths'].values[start:], 'x:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIRD_deaths, 'x:')

    ax.legend(("Заражения (Реальные данные)",
               "Заражения (SEIRD). Ошибка прогнозирования {}%".format(mape_confirmed),
               "Выздоровления (Реальные данные)",
               "Выздоровления (SEIRD). Ошибка прогнозирования {}%".format(mape_recovered),
               "Смерти (Реальные данные)",
               "Смерти (SEIRD). Ошибка прогнозирования {}%".format(mape_deaths)))

    ax.set_xlabel('Дата')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def display_SI(real_value, solve_SI, start, end, S=False):
    SI_confirmed = list()
    SI_susceptible = list()
    for i in range(len(solve_SI)):
        SI_confirmed.append(solve_SI[i][1])
        SI_susceptible.append(solve_SI[i][0])

    fig, ax = plt.subplots(figsize=(12,5))
    if end - start == 41:
        ax.set_title('Модель SI для {} дня'.format(end-start))
    else:
        ax.set_title('Модель SI для {} дней'.format(end-start))

    mape_confirmed = round(MAPE(real_value.head(end)['Confirmed'].values[start:], SI_confirmed), 5)

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Confirmed'].values[start:], 'o:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SI_confirmed, 'o:')

    if S:
        ax.plot(real_value.head(end)['ObservationDate'].values[start:], SI_susceptible, 'o:')

    ax.legend(("Заражения (Реальные данные)",
               "Заражения (SI). Ошибка прогнозирования {}%".format(mape_confirmed),
               "Восприимчивые (SI)"))

    ax.set_xlabel('Дата')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def display_SIR(real_value, solve_SIR, start, end):
    SIR_confirmed = list()
    SIR_recovered = list()
    for i in range(len(solve_SIR)):
        SIR_confirmed.append(solve_SIR[i][1])
        SIR_recovered.append(solve_SIR[i][2])

    fig, ax = plt.subplots(figsize=(12, 5))
    if end - start == 41:
        ax.set_title('Модель SIR для {} дня'.format(end - start))
    else:
        ax.set_title('Модель SIR для {} дней'.format(end - start))

    mape_confirmed = round(MAPE(real_value.head(end)['Confirmed'].values[start:], SIR_confirmed), 5)
    mape_recovered = round(MAPE(real_value.head(end)['Recovered'].values[start:], SIR_recovered), 5)

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Confirmed'].values[start:], 'o:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SIR_confirmed, 'o:')

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Recovered'].values[start:], 's:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SIR_recovered, 's:')

    ax.legend(("Заражения (Реальные данные)",
               "Заражения (SIR). Ошибка прогнозирования {}%".format(mape_confirmed),
               "Выздоровления (Реальные данные)",
               "Выздоровления (SIR). Ошибка прогнозирования {}%".format(mape_recovered)))

    ax.set_xlabel('Дата')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def display_SEIR(real_value, solve_SEIR, start, end):
    SEIR_confirmed = list()
    SEIR_recovered = list()
    for i in range(len(solve_SEIR)):
        SEIR_confirmed.append(solve_SEIR[i][2])
        SEIR_recovered.append(solve_SEIR[i][3])

    fig, ax = plt.subplots(figsize=(12, 5))
    if end - start == 41:
        ax.set_title('Модель SEIR для {} дня'.format(end - start))
    else:
        ax.set_title('Модель SEIR для {} дней'.format(end - start))

    mape_confirmed = round(MAPE(real_value.head(end)['Confirmed'].values[start:], SEIR_confirmed), 5)
    mape_recovered = round(MAPE(real_value.head(end)['Recovered'].values[start:], SEIR_recovered), 5)

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Confirmed'].values[start:], 'o:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIR_confirmed, 'o:')

    ax.plot(real_value.head(end)['ObservationDate'].values[start:],
            real_value.head(end)['Recovered'].values[start:], 's:')
    ax.plot(real_value.head(end)['ObservationDate'].values[start:], SEIR_recovered, 's:')

    ax.legend(("Заражения (Реальные данные)",
               "Заражения (SEIR). Ошибка прогнозирования {}%".format(mape_confirmed),
               "Выздоровления (Реальные данные)",
               "Выздоровления (SEIR). Ошибка прогнозирования {}%".format(mape_recovered)))

    ax.set_xlabel('Дата')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.show()


def display_time_series(start, count, real, forec, date):
    fig, ax = plt.subplots(figsize=(12, 5))
    if count == 41:
        ax.set_title('Прогнозирование временных рядов для {} дня'.format(count))
    else:
        ax.set_title('Прогнозирование временных рядов для {} дней'.format(count))

    mape_confirmed = round(MAPE(real[start:(count+start)], forec),5)

    ax.plot(date[start:(count+start)], real[start:(count+start)], 's:')
    ax.plot(date[start:(count+start)], forec, 'o:')

    ax.legend(("Заражения (Реальные данные)",
                "Заражения (Прогноз). Ошибка прогнозирования {}%".format(mape_confirmed)))

    ax.set_xlabel('Дни')
    ax.set_ylabel('Число подтвержденных случаев')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.show()