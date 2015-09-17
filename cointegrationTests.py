import statsmodels.tsa.stattools as st
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

import pandas as pd
df = pd.read_csv('ETF.csv',index_col=0)
plt.hold(True)
df[['ewa','ewc']].plot()
#plt.show()

plt.scatter(df['ewa'],df['ewc'])
plt.title('ewa / ewc')
#plt.show()

import statsmodels.formula.api as smf
results = smf.ols('ewc ~ ewa', data=df).fit()
hedgeRatio = results.params['ewa']
print hedgeRatio

df['coint'] = df['ewc']-hedgeRatio*df['ewa']
plt.hold(False)
df['coint'].plot()
#plt.show()

import pyconometrics
print pyconometrics.cadf(np.matrix(df['ewa']).H,
                         np.matrix(df['ewc']).H,0,1)

import statsmodels.tsa.stattools as st
import hurst 
print 'hurst', hurst.hurst(df['coint'])
print st.adfuller(df['coint'],maxlag=1)

from johansen import coint_johansen, print_johan_stats
res = coint_johansen(df[['ewa','ewc']], 0, 1)
print_johan_stats(res)

cols = ['ewc','ewa','ige']
res3 = coint_johansen(df[cols], 0, 1)
print_johan_stats(res3)

df['yport'] = np.dot(df[cols], res3.evec[:,0])
plt.hold(False)
df['yport'].plot()
#plt.show()

import halflife
hf = halflife.halflife(df, 'yport')[1]
data_mean = pd.rolling_mean(df['yport'], window=hf)
data_std = pd.rolling_std(df['yport'], window=hf)
# yport evec ile senet carpimi
# numUnits yport'un Z skoru
df['numUnits'] = -1*(df['yport']-data_mean) / data_std

# Z skoru 3 kolon yap
tmp1 = np.ones(df[cols].shape) * np.array([df['numUnits']]).T
# evec tekrarla, her satirda tekrar tekrar
tmp2 = np.ones(df[cols].shape) * np.array([res3.evec[:,0]])
# evec sermayenin nasil bolusturuldugu olarak gorulebilir
# positions ise her senete dolar biriminde ne kadar para ayrildigi
positions = tmp1 * tmp2 * df[cols]
positions = pd.DataFrame(positions)
# stratejinin gunluk kar/zarari
pnl = positions.shift(1) * (df[cols] - df[cols].shift(1))  / df[cols].shift(1)
pnl = pnl.sum(axis=1)
# getiri ise pnl'in portfoyun brut piyasa degeri ile bolunmesi
ret=pnl / np.sum(np.abs(positions.shift(1)),axis=1)
# Kumulatif birlesik getiri
plt.plot(np.cumprod(1+ret)-1)
#plt.show()

print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
