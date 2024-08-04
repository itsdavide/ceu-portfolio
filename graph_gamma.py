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
Plots the graph of epsilon_star as a function of gamma for several time horizons
"""

import numpy as np
import matplotlib.pyplot as plt
import CEU_portfolio as ceu

##############################################################################  
# Model paramenters
T = 4
u = 2
d = 1/2
S0 = 100
p = 0.8
epsilon = 1 / 50
r = 0.05
q = ((1 + r) - d) / (u - d)
gamma = 1
V0 = 100
############################################################################## 


def epsilon_star(p, q, V0, u, d, r, gamma, T):
    best_CEU = -100000
    for e in range(0, 100):
        CEU = ceu.CEU_port_comb(p, V0, u, d, r, gamma, e / 100.00, T)[1]
        if abs(CEU - best_CEU) < 0.0000001:
            return e / 100.00
        best_CEU = CEU
    return e /100.00

            
Times = [1, 2, 3, 4, 5]

Gammas = np.arange(0.25, 4.25, 0.25)

p = 0.8

plt.figure(figsize=(10, 6))
plt.xlabel('$\gamma$')
plt.ylabel('$\epsilon^*$')
plt.title('$\epsilon^*$ ($V_0$='+str(V0)+', $u=$'+str(u)+', $d=$'+str(d)+', $r=$'+str(r)+ ', $p=$'+str(p)+')')

for T in Times:
    print('*** T =', T, '***')
    e_star = []
    for g in Gammas:
        e = epsilon_star(p, q, V0, u, d, r, g, T)
        e_star.append(e)
        print('Gamma = g', g, 'epsilon_* = ', e)
    
    plt.plot(Gammas, e_star, label='$T =$'+ str(T))
plt.legend()
plt.savefig('gamma.png', dpi=300)


