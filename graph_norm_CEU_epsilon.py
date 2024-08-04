#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portfolio optimization code for the paper:

D. Petturiti and B. Vantaggi. 
The impact of ambiguity on dynamic portfolio selection in the 
epsilon-contaminated binomial market model. 
European Journal of Operational Research, 314(3):1029–1039, 2024.
"""
"""
EXPLANATION OF THE CODE:
Plots the graph of normalized CEU as a function of epsilon.
"""

import CEU_portfolio as ceu
import numpy as np
import matplotlib.pyplot as plt

##############################################################################  
# Model paramenters
T = [1, 2, 3, 5, 10, 15, 20]
V0 = 10
r = 0.05
gamma = 2
u = 2
d = 0.5
p = 0.5
##############################################################################  

plt.figure(figsize=(10, 6))
plt.xlabel(r'$\epsilon$')
plt.ylabel('Normalized optimal CEU')
plt.title(r'CEU behavior ($p=$'+str(p)+', $V_0=$'+str(V0)+', $u=$'+str(u)+', $d=$'+str(d)+', $r=$'+str(r)+', $\gamma=$'+str(gamma)+')')

for t in T:
    print('Computing T = ', t)
    epsilon = []
    current = 0.0
    while current < 1:
        epsilon.append(current)
        current += 0.01
    opt_val = []
    for e in epsilon:
        opt_val.append(ceu.CEU_port_nonlin(p, V0, u, d, r, gamma, e, t)[1])
    x = np.array(epsilon)
    y = np.array(opt_val)
    y = (y - y.min()) / (y.max() - y.min())
    plt.plot(x, y, label='$T=$'+str(t))
plt.legend()
plt.savefig('norm_CEU_epsilon.png', dpi=300)
    