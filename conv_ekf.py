import scipy.io as sio
import pandas as pd
mat = sio.loadmat('inputData_ETF.mat')
ewa=10;ewc=11
ewa = mat['cl'][:,ewa]
ewc = mat['cl'][:,ewc]
df = pd.DataFrame(index=range(len(ewa)))
df['ewa'] = ewa
df['ewc'] = ewc
print df.head()
df.to_csv('inputData_ETF.csv')
