import matplotlib.pylab as plt
import numpy as np
import pandas as pd

dftu = pd.read_csv('TU.csv')

import corr

res = []
for lookback in [1, 5, 10, 25, 60, 120, 250]:
   for holddays in [1, 5, 10, 25, 60, 120, 250]:
       df_Close_lookback = dftu.Close.shift(lookback)
       df_Close_holddays = dftu.Close.shift(-holddays)
       dftu['ret_lag'] = (dftu.Close-df_Close_lookback)/df_Close_lookback
       dftu['ret_fut'] = (df_Close_holddays-dftu.Close)/dftu.Close
       dfc = dftu[['ret_lag','ret_fut']].dropna()
       idx = None
       if lookback >= holddays: 
           idx = np.array(range(0,len(dfc.ret_lag), holddays))
       else: 
           idx = np.array(range(0,len(dfc.ret_lag), lookback))
       dfc = dfc.ix[idx]
       t, x, p = corr.p_corr(dfc.ret_lag, dfc.ret_fut)
       res.append([lookback, holddays,  t, p])
res = pd.DataFrame(res,columns=['geriye bakis','tutma gunu','korelasyon','p degeri'])
print res[res['geriye bakis'] >= 25]

import dd

def report(df,lookback,holddays):

    longs = df.Close > df.Close.shift(lookback)
    shorts = df.Close < df.Close.shift(lookback)
    df['pos'] = 0.
    for h in range(holddays):
       long_lag = longs.shift(h).fillna(False)
       short_lag = shorts.shift(h).fillna(False)
       df.loc[long_lag,'pos'] += 1
       df.loc[short_lag,'pos'] -= 1

    ret=(df.pos.shift(1)* (df.Close-df.Close.shift(1)) / df.Close.shift(1)) \
         / holddays

    cumret=np.cumprod(1+ret)-1

    print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
    print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
    print 'Dusus Kaliciligi', dd.calculateMaxDD(np.array(cumret))
    return cumret

cumret=report(dftu,lookback = 250,holddays = 25)

plt.plot(cumret)
plt.show()
