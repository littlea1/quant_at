import statsmodels.tsa.stattools as st
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

df = pd.read_csv('gld_uso.csv')

cols = ['GLD','USO']

df['hedgeRatio'] = df['USO'] / df['GLD']
data_mean = pd.rolling_mean(df['hedgeRatio'], window=20)
data_std = pd.rolling_std(df['hedgeRatio'], window=20)
df['numUnits'] = -1*(df['hedgeRatio']-data_mean) / data_std
positions = df[['numUnits','numUnits']].copy()
positions = positions * np.array([-1., 1.])
pnl = positions.shift(1) * np.array((df[cols] - df[cols].shift(1))  / df[cols].shift(1))
pnl = pnl.fillna(0).sum(axis=1)
ret=pnl / np.sum(np.abs(positions.shift(1)),axis=1)
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1.
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
