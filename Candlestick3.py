import numpy
import matplotlib.pyplot as plt
import pandas as pd
import sys

A = float(sys.argv[1])
B = float(sys.argv[2])
C = float(sys.argv[3])
D = float(sys.argv[4])
E = float(sys.argv[5])
F = float(sys.argv[6])
G = float(sys.argv[7])
H = float(sys.argv[8])
I = float(sys.argv[9])
J = float(sys.argv[10])
K = float(sys.argv[11])
L = float(sys.argv[12])
M = str(sys.argv[13])

prices = pd.DataFrame({'open': [A, E, I],
                       'close': [B, F, J],
                       'high': [C, G, K],
                       'low': [D, H, L]},
                       index=pd.date_range(start='2022-11-04', end='2022-11-07', periods=3))

plt.style.use('dark_background')
plt.figure()
plt.axis('off')

width = .4
width2 = .05

#define up and down prices
up = prices[prices.close>=prices.open]
down = prices[prices.close<prices.open]

#define colors to use
col1 = 'green'
col2 = 'red'

#plot up prices
plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)

#plot down prices
plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

#rotate x-axis tick labels
plt.xticks(rotation=45, ha='right')

#display candlestick chart
#plt.show()

plt.savefig(M)
