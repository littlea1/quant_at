# Python Code for Algorithmic Trading

This project is a collection of Python codes that aim to replicate the
Matlab codes for Dr. Ernest Chan's book *Algorithmic Trading*.

The file names for scripts reflect Dr. Chan's Matlab script names, for
example the code for `Ratio.m` is in `Ratio.py`.

All feedback, comments, pull requests are welcome. 

## Requirements

Run `pip install` on

```
numpy
scipy
statsmodels
pandas
arch
```

There are three big data files that are hard to share through Github,
they can be downloaded through the links below:

[AUDCAD](https://dl.dropboxusercontent.com/u/1570604/data/inputData_AUDCAD_20120426.mat)

[AUDUSD](https://dl.dropboxusercontent.com/u/1570604/data/inputData_AUDUSD_20120426.mat)

[USDCAD](https://dl.dropboxusercontent.com/u/1570604/data/inputData_USDCAD_20120426.mat)

## Converting MAT Files to CSV

I prefer to work with CSV files, the Pandas library makes it a breeze
to access them plus I can view the contents of CSV files easily,
manipulate them with Unix based tools if necessary, etc. For
converting any of mat files into csv, this is what I did. Find the
Matlab script from Dr. Chan's book that reads and prepares the data,
i.e. `TU_mom.m`, then find the point the data is all ready,

```
clear;
load('inputDataOHLCDaily_20120511', 'syms', 'tday', 'cl');
..
idx=strmatch('TU', syms, 'exact');
tday=tday(:, idx);
cl=cl(:, idx);
..
``

Now at this point you have `tday,cl`, all prepared, with the same
dimensions. We can create a data matrix out of these and write them to
disk, insert these in the script,

```
A = [tday cl];
save('/tmp/out','A');
exit;
```

and run it. Now from a seperate Python script,

```
from scipy import io as spio
import numpy as np
import pandas as pd

y = spio.loadmat('out.mat')['A']
df = pd.DataFrame(y, columns=['Date','Close'])
df.to_csv('/tmp/out.csv',index=None)
```

This gives you a CSV file.

## LICENSE

Thhe code is licensed under GPL v3. See COPYING for details.
