import statsmodels.tsa.stattools as st
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

df_caus = pd.read_csv('USDCAD.csv')
plt.hold(False)
df_caus.y.plot()
#plt.show()
print st.adfuller(df_caus.y,maxlag=1)

import hurst as h
print 'H doviz kuru', h.hurst(df_caus.y)

from arch.unitroot import VarianceRatio
vr = VarianceRatio(np.log(df_caus.y))
print(vr.summary().as_text())

df_caus['ylag'] = df_caus['y'].shift(1)
df_caus['deltaY'] = df_caus['y'] - df_caus['ylag']

import statsmodels.formula.api as smf
results = smf.ols('deltaY ~ ylag', data=df_caus).fit()
lam = results.params['ylag']
print lam

halflife=-np.log(2)/lam
print halflife, 'days'
