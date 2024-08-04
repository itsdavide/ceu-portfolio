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
Computes the optimal portfolio for the market calibrated META stock with both
the non-linear programming problem and the combinatorial problem.
"""
import CEU_portfolio as ceu

##############################################################################
# Calibrated data on META stock
T = 5
epsilon = 0.02
p = 0.5528455284552846
u = 1.0291516607967388
d = 0.9716740866218196
gamma = 2
V0 = 1000
r = 0.00019822675964520364
##############################################################################

# Optimal final wealth with non-linear programming
V_opt, CEU_opt = ceu.CEU_port_nonlin(p, V0, u, d, r, gamma, epsilon, T)

print('*** NON-LINEAR PROGRAMMING SOLUTION ***')
print('*** Optimal final wealth (as a function of the number k of "up" moves) ***')
for k in range(len(V_opt) - 1, -1, -1):
    print('V_T[', k, '] = {:.4f}'.format(V_opt[k]))
print('CEU_opt:', CEU_opt)

print()
# Optimal final wealth with combinatorial optimization
V_opt, CEU_opt = ceu.CEU_port_comb(p, V0, u, d, r, gamma, epsilon, T)

print('*** COMBINATORIAL OPTIMIZATION SOLUTION ***')
print('*** Optimal final wealth (as a function of the number k of "up" moves) ***')
for k in range(len(V_opt) - 1, -1, -1):
    print('V_T[', k, '] = {:.4f}'.format(V_opt[k]))
print('CEU_opt:', CEU_opt)