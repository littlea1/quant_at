import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import dd

df = pd.read_csv('FSTX.csv')
entryZscore=0.1

stdret = pd.rolling_mean(df.cl.pct_change(), window=90).shift(1)
longs = df.op >= df.hi.shift(1)*(1+entryZscore*stdret)
shorts = df.op <= df.lo.shift(1)*(1-entryZscore*stdret)
df['pos'] = 0
df.loc[longs,'pos'] = 1
df.loc[shorts,'pos'] = -1
ret=df.pos * (df.op-df.cl) / df.op
ret = ret.dropna()
cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
print 'Dusme Kaliciligi', dd.calculateMaxDD(np.array(cumret))

plt.plot(cumret)
#plt.show()
