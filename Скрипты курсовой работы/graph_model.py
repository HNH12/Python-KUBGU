import numpy as np
import math
from scipy.integrate import odeint


def SI(STATE,t,beta,N):
    S, I = STATE
    der_S = -beta*S*I/N
    der_I = beta*S*I/N
    return [der_S,der_I]


def SI_model(N,S,I,days,beta):
    t = np.arange(0,days, 1)
    p = odeint(SI, [S,I], t, args=(beta, N))
    return p


def SIR(STATE, t, beta, gamma, N):
    S, I, R = STATE
    dSdt = -beta * S * I / N
    dIdt = (beta * S * I / N) - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


def SIR_model(N, S, I, R, days, beta, gamma):
    t = np.arange(0, days, 1)
    p = odeint(SIR, [S,I,R], t, args=(beta, gamma, N))
    return p


def SEIR(STATE, t, beta, gamma, alpha, N):
    S, E, I, R = STATE
    der_S = -beta*S*I/N
    der_E = beta*S*I/N - alpha*E
    der_I = alpha*E - gamma*I
    der_R = gamma*I
    return [der_S,der_E,der_I,der_R]


def SEIR_model(N, S, E, I, R, days, beta, gamma, alpha):
    t = np.arange(0, days, 1)
    y0 = S, E, I, R
    p = odeint(SEIR, y0, t, args=(beta, gamma, alpha, N))
    return p


def modificate_SEIR(STATE, t, fi, beta, gamma, alpha, N):
    S, E, I, R = STATE
    der_S = (-beta*S*(I + fi*E))/N
    der_E = (beta*S*(I + fi*E))/N - alpha*E
    der_I = alpha*E - gamma*I
    der_R = gamma*I
    return der_S,der_E,der_I,der_R


def modificate_SEIR_model(N, S, E, I, R, days, fi, beta, gamma, alpha):
    t = np.arange(0, days, 1)
    y0 = S, E, I, R
    p = odeint(modificate_SEIR, y0, t, args=(fi,beta, gamma, alpha, N))
    return p


def funct(I, fi, E, sigma, K0):
    return math.exp(-sigma*math.pow((I+fi*E),K0))


def SEIRD_with_exp(STATE, t, fi, alpha, beta, gamma, mu, sigma, K0, N):
    S, E, I, R, D = STATE
    der_S = -(beta*S*(I + fi*E)*funct(I,fi,E,sigma,K0))/N
    der_E = beta*S*(I + fi*E)*funct(I,fi,E,sigma,K0)/N - alpha*E
    der_I = alpha*E - gamma*I - mu*I
    der_R = gamma*I
    der_D = mu*I
    return [der_S, der_E, der_I, der_R, der_D]


def SEIRD_model_with_exp(N, S, E, I, R, D, days,
                beta, alpha, gamma, mu, fi, sigma, K0):
    t = np.arange(0, days, 1)
    y0 = S, E, I, R, D
    p = odeint(SEIRD_with_exp, y0, t, args=(fi, alpha, beta, gamma, mu, sigma, K0, N))
    return p


def SEIRD_with_smoothing(STATE, t, fi, alpha, gamma, mu, smoothing, N):
    S, E, I, R, D,beta = STATE
    der_S = -(beta*S*(I + fi*E))/N
    der_E = beta*S*(I + fi*E)/N - alpha*E
    der_I = alpha*E - gamma*I - mu*I
    der_R = gamma*I
    der_D = mu*I
    del_beta = -beta*smoothing
    # del_beta = -beta * 0.0310=
    # del_beta = -beta*0.0014*((3*t+t)/10)
    return [der_S, der_E, der_I, der_R, der_D, del_beta]


def SEIRD_model_with_smoothing(N, S, E, I, R, D, days,
                beta, alpha, gamma, mu, fi, smoothing=0):
    t = np.arange(0, days, 1)
    y0 = S, E, I, R, D, beta
    p = odeint(SEIRD_with_smoothing, y0, t, args=(fi, alpha,gamma, mu, smoothing, N))
    return p


def SEIRD(STATE, t, fi, alpha, beta, gamma, mu, N):
    S, E, I, R, D = STATE
    der_S = -(beta * S * (I + fi * E)) / N
    der_E = beta * S * (I + fi * E) / N - alpha * E
    der_I = alpha * E - gamma * I - mu * I
    der_R = gamma * I
    der_D = mu * I
    return [der_S, der_E, der_I, der_R, der_D]


def SEIRD_model(N, S, E, I, R, D, days,
                beta, alpha, gamma, mu, fi):
    t = np.arange(0, days, 1)
    y0 = S, E, I, R, D
    p = odeint(SEIRD, y0, t, args=(fi, alpha, beta, gamma, mu, N))
    return p