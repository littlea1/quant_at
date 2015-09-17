import statsmodels.tsa.stattools as st
import matplotlib.pylab as plt
import numpy as np
import pandas as pd, os, sys
from scipy import io as spio

cols = ['tday','cl','lo','hi','hhmm','op']
base = '%s/Dropbox/Public/data' % os.environ['HOME']
a = spio.loadmat(base + '/inputData_USDCAD_20120426.mat')
usdcad = pd.concat([pd.DataFrame(a[x]) for x in cols], axis=1)
usdcad.columns = cols
a = spio.loadmat(base + '/inputData_AUDUSD_20120426.mat')
audusd = pd.concat([pd.DataFrame(a[x]) for x in cols], axis=1)
audusd.columns = cols

usdcad2 = usdcad[(usdcad.tday>20090101) & (usdcad.hhmm == 1659)]
audusd2 = audusd[(audusd.tday>20090101) & (audusd.hhmm == 1659)]
usdcad2 = usdcad2.set_index(['tday','hhmm'])
audusd2 = audusd2.set_index(['tday','hhmm'])
cad = 1 / usdcad2.cl
aud=audusd2.cl
y = pd.concat([aud, cad],axis=1)

from johansen import coint_johansen
trainlen=250
lookback=20
numUnits = np.ones(len(y))*np.nan
hedgeRatio = np.ones(y.shape)*np.nan
for t in range(trainlen,len(y)):
   df = y[t-trainlen:t]
   hedgeRatio[t] = coint_johansen(df, 0, 1).evec[:,0]
   tmp1 = np.array(y[t-lookback:t])
   tmp2 = np.kron(np.ones((lookback,1)),hedgeRatio[t])
   yport = np.sum(tmp1*tmp2,axis=1)
   ma=np.mean(yport)
   mstd=np.std(yport)
   zScore=(yport[-1]-ma)/mstd;
   numUnits[t] = -(yport[-1]-ma)/mstd


# copy positions in multiple coumns. positions are market values of AUDUSD and CADUSD in portfolio expressed
# in US.
tmp1=np.kron(np.ones((y.shape[1],1)),numUnits)
positions = tmp1.T * hedgeRatio * y
pnl = positions.shift(1) * (y - y.shift(1))  / y.shift(1)
pnl = pnl.sum(axis=1)
ret=pnl / np.sum(np.abs(positions.shift(1)),axis=1)
ret = ret[trainlen:-1] # trainlen kadar ilk bolumu disarida birak
print 'APR', ((np.prod(1.+ret))**(252./len(ret)))-1
print 'Sharpe', np.sqrt(252.)*np.mean(ret)/np.std(ret)

plt.plot(np.cumprod(1+ret)-1)
plt.title('Kumulatif Birlesik Getiri')
#plt.show()
