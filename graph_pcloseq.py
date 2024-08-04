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
Plots epsilon_star as a function of T for values of p close to q.
"""

import CEU_portfolio as ceu
import matplotlib.pyplot as plt

##############################################################################  
# Model paramenters
V0 = 10
r = 0.05
gamma = 2
u = 2
d = 0.5
############################################################################## 

def epsilon_star(p, V0, u, d, r, gamma, T):
    best_CEU = -100000
    for e in range(0, 100):
        CEU = ceu.CEU_port_nonlin(p, V0, u, d, r, gamma, e / 100.00, T)[1]
        if abs(CEU - best_CEU) < 0.0000001:
            return e / 100.00
        best_CEU = CEU
    return e / 100.00


plt.figure(figsize=(10, 6))
plt.xlabel(r'$T$')
plt.ylabel(r'$\epsilon^*$')
plt.title(r'$\epsilon^*$ ($V_0=$'+str(V0)+r', $u=$'+str(u)+r', $d=$'+str(d)+r', $r=$'+str(r)+r', $\gamma=$'+str(gamma)+')')
            

Times = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

q = (1 + r - d) / (u - d) 

Probs = [- 0.01, 0.01, -0.02, 0.02, -0.03, 0.03]

for p in Probs:
    e_star = []
    print()
    print('p = ', p)
    for T in Times:
        e = epsilon_star(q + p, V0, u, d, r, gamma, T)
        e_star.append(e)
        print('T = ', T, 'epsilon_* = ', e)
    if p > 0:
        plt.plot(Times, e_star, label='$p = q + $'+ str(p)) 
    else:
        plt.plot(Times, e_star, label='$p = q - $'+ str(abs(p))) 
plt.legend()
plt.savefig('pcloseq.png', dpi=300)

