import matplotlib.pylab as plt
import numpy as np
import pandas as pd, zipfile, dd

with zipfile.ZipFile('earnann.zip', 'r') as z:
    earnann =  pd.read_csv(z.open('earnann.csv'),sep=',')
    op =  pd.read_csv(z.open('earnann-op.csv'),sep=',')
    cl =  pd.read_csv(z.open('earnann-cl.csv'),sep=',')

lookback=90
retC2O=(op-cl.shift(1)) / cl.shift(1)
stdC2O=pd.rolling_std(retC2O, window=lookback)
pos = pd.DataFrame(np.zeros(cl.shape),index=cl.index,columns=cl.columns)
longs=(retC2O >= 0.5*stdC2O).astype(int) * earnann
shorts=(retC2O <= -0.5*stdC2O).astype(int) * earnann;
pos = pos + longs - shorts
ret=(pos*(cl-op)/op).sum(axis=1)/30.

cumret=np.cumprod(1+ret)-1
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)
print 'Dusme Kaliciligi', dd.calculateMaxDD(np.array(cumret))

plt.plot(cumret)
#plt.show()
