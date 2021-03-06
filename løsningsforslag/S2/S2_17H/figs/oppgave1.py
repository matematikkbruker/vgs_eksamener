# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 13:16:53 2017
"""

import numpy as np
import matplotlib.pyplot as plt

def K(x):
    return 680*x*x + (736/x)


x = np.linspace(0.1, 2, num = 500)

plt.style.use('seaborn-ticks')
plt.rc('text', usetex = False)
plt.plot(x, K(x), label = r'K(x)', linewidth = 2.5)
plt.xlim([0.2, 2])
plt.ylim([0, 5000])

plt.grid(True)
plt.legend(loc = 'best')
plt.show()
    