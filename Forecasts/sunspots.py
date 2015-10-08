from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.stats.stattools as stattools
import statsmodels.stats.diagnostic as diag
from statsmodels.graphics.api import qqplot

# Load and clean data
sunspot_data = sm.datasets.sunspots.load_pandas().data
sunspot_data.index = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
del sunspot_data["YEAR"]

sunspot_data.plot(figsize=(12,8));

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(sunspot_data.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(sunspot_data, lags=40, ax=ax2)

arma_mod20 = sm.tsa.ARMA(sunspot_data, (2,0)).fit()
arma_mod30 = sm.tsa.ARMA(sunspot_data, (3,0)).fit()

stattools.durbin_watson(arma_mod30.resid.values)

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ax = arma_mod30.resid.plot(ax=ax)

resid = arma_mod30.resid

diag.normal_ad(resid)

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
data = np.c_[range(1,41), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))

predict_sunspots = arma_mod30.predict('1990', '2012', dynamic=True)
print(predict_sunspots)

fig, ax = plt.subplots(figsize=(12, 8))
ax = sunspot_data.ix['1950':].plot(ax=ax)
fig = arma_mod30.plot_predict('1990', '2012', dynamic=True, ax=ax, plot_insample=False)


def mean_forecast_err(y, yhat):
    return y.sub(yhat).mean()

mean_forecast_err(sunspot_data.SUNACTIVITY, predict_sunspots)

best_order = sm.tsa.arma_order_select_ic(sunspot_data.SUNACTIVITY, max_ar = 8, max_ma = 3, ic='aic').get('aic_min_order')
arma_select_mod = sm.tsa.ARMA(sunspot_data, best_order).fit()

fig, ax = plt.subplots(figsize=(12, 8))
ax = sunspot_data.ix['1950':].plot(ax=ax)
fig = arma_select_mod.plot_predict('1990', '2020', dynamic=True, ax=ax, plot_insample=True)

select_mod_prediction = arma_select_mod.predict('1990','2012', dynamic=True)
mean_forecast_err(sunspot_data.SUNACTIVITY, select_mod_prediction)