#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portfolio optimization code for the paper:

D. Petturiti and B. Vantaggi. 
The impact of ambiguity on dynamic portfolio selection in the 
epsilon-contaminated binomial market model. 
European Journal of Operational Research, 314(3):1029–1039, 2024.
"""
"""
EXPLANATION OF THE CODE:
Market calibration for the META stock.
"""

import numpy as np
import yfinance as yf
import statistics as stat

print('*** Market data on 2023-06-30 ***')

# Download historical META data
hist_data = yf.download(['META'], start='2023-01-01', end='2023-07-01')['Close']

# Compute daily log-returns
log_rets = np.log(hist_data/hist_data.shift(1))
log_rets = log_rets.dropna()

# Compute the daily historical volatility
vol_day = stat.stdev(log_rets)

# Compute the annual historical volatility
vol_year = vol_day * np.sqrt(250)

# Estimate p
p = len(log_rets[log_rets >= 0]) / len(log_rets)
print('p:', p)

# Value of r per period
Delta_t = 1 / 250

# Return rate of a US T-bill maturing in 1 month
r_year = 5.08 / 100 
r_day = (1 + r_year)**Delta_t - 1
r = r_day
print('r:', r)

# Estimate u and d and q
sigma = vol_year
u = np.exp(sigma * np.sqrt(Delta_t))
d = np.exp(-sigma * np.sqrt(Delta_t))
print('u:', u)
print('d:', d)

# Compute the risk-neutral probability
q = ((1 + r) - d) / (u - d)
print('q:', q)

# Extract the last META stock price
S0 = (yf.download(['META'], start='2023-06-30', end='2023-07-01')['Close'])
print('S0:', S0)

# Plot the META stock price time series
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.title('META stock price time series')
plt.plot(hist_data,label='META stock price',c='red')
plt.xlabel('Date')
plt.ylabel('Stock price')
plt.savefig('meta.png', dpi=300)



