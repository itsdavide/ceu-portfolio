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
Plots the 3D graph of epsilon_star as a function of p and T.
"""

import CEU_portfolio as ceu
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm

# Compute the epsilon_star threshold
def epsilon_star(p, V0, u, d, r, gamma, T):
    best_CEU = -100000
    for e in range(0, 100):
        CEU = ceu.CEU_port_nonlin(p, V0, u, d, r, gamma, e / 100.00, T)[1]
        if abs(CEU - best_CEU) < 0.0000001:
            return e / 100.00
        best_CEU = CEU
    return e / 100.00

##############################################################################  
# Model paramenters
V0 = 10
r = 0.05
Times = list(range(1,11))
Probs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
Gammas = [1]
Us = [1.5]
##############################################################################

for g in Gammas:
    print()
    print('Gamma = ', g)
    for u in Us:
        x = []
        y = []
        z = []
        print('u = ', u)
        for p in Probs:
            e_star = []
            print()
            print('p = ', p)
            for T in Times:
                e = epsilon_star(p, V0, u, 1/u, r, g, T)
                e_star.append(e)
                print('T = ', T, 'epsilon_* = ', e)
                x.append(p)
                y.append(T)
                z.append(e)
                
        # Add the singular line obtained for q = p
        q = (1 + r - (1 / u)) / (u -  (1 / u))
        for T in Times:
            e = 0
            e_star.append(e)
            print('T = ', T, 'epsilon_* = ', e)
            x.append(q)
            y.append(T)
            z.append(e)
        Xs = np.array(x)
        Ys = np.array(y)
        Zs = np.array(z)
        
        
        # Plot the 3D epsilon_star surface as a function of p and T
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_trisurf(Xs, Ys, Zs, cmap=cm.jet, linewidth=0)

        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(6))
        ax.zaxis.set_major_locator(MaxNLocator(5))

        ax.set_xlabel('$p$')
        ax.set_ylabel('$T$')

        ax.set_title(r'$\epsilon^*$ ($V_0 = $' + str(V0) + r', $\gamma = $' + str(g) + ', $u = $' + str(u) + ', $d = 1/u$, $r =$' + str(r) + ')' )

        fig.tight_layout()

        fig.savefig('3D_g' + str(g) + '_u' + str(u) + 'd_1_u.png', dpi=300)




