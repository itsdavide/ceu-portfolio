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
Plots the 3D graph of epsilon_star as a function of p and r, together with
the contour plot.
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
Probs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
Rs = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
Gammas = [1]
Us = [2]
T = 5
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
            for r in Rs:
                e = epsilon_star(p, V0, u, 1/u, r, g, T)
                e_star.append(e)
                print('r = ', r, 'epsilon_* = ', e)
                x.append(p)
                y.append(r)
                z.append(e)

        # Adds the singular line
        print('Singular line:')
        for r in Rs:
            q = (1 + r - (1 / u)) / (u -  (1 / u))
            print('r = ', r, ' q = ', q)
            e = 0
            e_star.append(e)
            print('r = ', r, 'epsilon_* = ', e)
            x.append(q)
            y.append(r)
            z.append(e)
            
        Xs = np.array(x)
        Ys = np.array(y)
        Zs = np.array(z)

        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_trisurf(Xs, Ys, Zs, cmap=cm.jet, linewidth=0)

        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(6))
        ax.zaxis.set_major_locator(MaxNLocator(5))

        ax.set_xlabel('$p$')
        ax.set_ylabel('$r$')

        ax.set_title(r'$\epsilon^*$ ($V_0 = $' + str(V0) + r', $\gamma = $' + str(g) + ', $u = $' + str(u) + ', $d = 1/u$, $T =$' + str(T) + ')' )

        fig.tight_layout()

        fig.savefig('3D_g' + str(g) + '_u' + str(u) + 'd_1_u_rate.png', dpi=300)
        
        
        plt.clf()
        levels = np.arange(0, 1, 0.02)
        fig = plt.figure(figsize=(5,5))
        plt.title(r'Contour lines of $\epsilon^*$ interpolated surface')
        plt.xlabel('$p$')
        plt.ylabel('$r$')
        plt.yticks(Rs)
        plt.tricontour(Xs, Ys, Zs, zdir='z', cmap=cm.jet, levels=levels)
        plt.savefig('Epsilon-star-cl.png', dpi=300)
        





