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
Optimization code that finds the optimal final wealth relying on the following parameters
* T: Time horizon (in periods)
* epsilon: Ambiguity parameter in [0,1)
* p: Real-world probability of an "up" move over a single period
* u: "up" move coefficient
* d: "down" move coefficient
* gamma: CRRA relative risk aversion parameter
* V0: Initial positive wealth
* r: Risk-free interest rate over a single period

IMPORTANT: The code requires the bonmin solver, whose path should be inserted
in the variable optimizer_path.
"""

import pyomo.environ as pyo
import scipy.special
import numpy as np

tolerance = 0

optimizer_path = 'PATH_TO_BONMIN'

##############################################################################
# NON-LINEAR PROGRAMMING SOLUTION
##############################################################################
# Portfolio optimization with non-linear programming
def CEU_port_nonlin(p, V0, u, d, r, gamma, epsilon, T):
    # Create a PyOmo model
    model = pyo.ConcreteModel()

    # Indices of optimization variables
    N = list(range(1,T + 2))
    
    # Risk-neutral probability
    q = ((1 + r) - d) / (u - d)
    
    # Utility function
    def u(x):
        if gamma == 1:
            return pyo.log(x)
        return x ** (1 - gamma) / (1 - gamma)

    # Generate the P probabilities
    P = {}
    for i in N:
        k = T - (i - 1)
        P[i] = scipy.special.comb(T, k) * p**k * (1-p)**(T - k)

    # Generate the Q probabilities
    Q = {}
    for i in N:
        k = T - (i - 1)
        Q[i] = scipy.special.comb(T, k) * q**k * (1-q)**(T - k)
    
    
    # Generate the permuted P probabilities
    PP = {}
    for i in N:
        for j in N:
            if i == j:
                PP[i,j] = (1 - epsilon) * P[j] + epsilon
            else:
                PP[i,j] = (1 - epsilon) * P[j]
    
    model.N = pyo.Set(initialize=N)

    model.PP = pyo.Param(model.N, model.N, initialize=PP)
    model.Q = pyo.Param(model.N, initialize=Q, mutable=True)
    model.V = pyo.Var(model.N, within=pyo.NonNegativeReals, bounds=(tolerance, np.Infinity), initialize=tolerance)
    model.C = pyo.Var()

    def ConstrRule(model, i):
        return sum(model.PP[i, j] * u(model.V[j]) for j in model.N) >= model.C

    model.c = pyo.Constraint(model.N, rule=ConstrRule)

    model.d = pyo.Constraint(expr=sum(model.Q[i] * model.V[i] for i in model.N) - V0*((1+r)**T) == 0)

    model.o = pyo.Objective(expr = model.C, sense=pyo.maximize)

    status = pyo.SolverFactory(optimizer_path).solve(model)
    pyo.assert_optimal_termination(status)
    
    # Extract the optimal solution
    V=[]
    
    for i in model.N:
        V.append(pyo.value(model.V[i]))
    
    # Create an array and revert the order
    V = np.array(V)[::-1]
        
    # Return the optimal solution and the optimal CEU value
    return (V, pyo.value(model.o))


##############################################################################
# COMBINATORIAL SOLUTION
##############################################################################
# CRRA utility function
def U(x, gamma):
    if (gamma > 0 and gamma < 1) or gamma > 1:
        return (x ** (1 - gamma)) / (1 - gamma)
    if gamma == 1:
        return np.log(x)

# Prime derivative of CRRA utility function
def U_p(x, gamma):
    if x < 0:
        print('*** ERROR ***')
        return
    if (gamma > 0 and gamma < 1) or gamma > 1:
        return x ** (- gamma)
    if gamma == 1:
        return 1 / x
    
# Inverse of prime derivative of CRRA utility function
def U_p_inv(x, gamma):
    if x < 0:
        print('*** ERROR ***')
        return
    if (gamma > 0 and gamma < 1) or gamma > 1:
        return x ** (-1 / gamma)
    if gamma == 1:
        return 1 / x
    
# Compute the power set of a set
def powerset(s):
    x = len(s)
    masks = {1 << i for i in range(x)}
    for i in range(1 << x):
        yield {ss for mask, ss in zip(masks, s) if i & mask}

# Compute lambda_first 
def lambda_first(T, first, A, I, Q, P_pi, gamma, r, V0):
    Atot = 0
    for i in I:
        Atot += A[i]
    tot = 0
    for k in range(T + 1):
        ind1 = 1 if k == first else 0
        tot += Q[k] * U_p_inv((1 / P_pi[first, k]) * (Q[k] + ind1 * Atot - (0 if not k in I else A[k])), gamma)

    return U_p(((1 + r) ** T * V0) / tot, gamma)

# Establish if lambdas are good
def good_lambdas(I, lambdas):
    for i in I:
        if lambdas[i] < 0:
            return False
    return True

# Establish if the final wealth is good
def good_V(T, first, V):
    for k in range(T + 1):
        if V[first] - V[k] > 0.000000001:
            return False
    return True
        
# Portfolio optimization with combinatorial optimization
def CEU_port_comb(p, V0, u, d, r, gamma, epsilon, T):
    # Risk-neutral probability
    q = ((1 + r) - d) / (u - d)
    
    # Create the index set
    Theta = set(range(T + 1))
    
    # Generate P probabilities
    P = np.zeros(T + 1)
    for k in range(T + 1):
        P[k] = scipy.special.comb(T, k) * p**k * (1-p)**(T - k)
    
    # Generate Q probabilities
    Q = np.zeros(T + 1)
    for k in range(T + 1):
        Q[k] = scipy.special.comb(T, k) * q**k * (1-q)**(T - k)
    
    # Generate the extreme points of the epsilon-contamination
    P_pi = np.zeros((T + 1, T + 1))
    for i in range(T + 1):
        P_pi[i, :] = (1 - epsilon) * P
        P_pi[i, i] += epsilon


    CEUS = []
    VS = []
    for first in range(T + 1):
        Theta_p = Theta.difference({first})
        # Generate the powerser of Theta'
        ps = list(powerset(Theta_p))
        for I in ps:
        
            A = {}
            for i in I:
                tot1 = P_pi[first, first]
                for k in I:
                    tot1 += P_pi[first, k]
                    tot2 = tot1 - P_pi[first, i]
                    I_p = I.difference({i})
                    tot3 = 0
                    for k in I_p:
                        tot3 += P_pi[first, k] * (Q[first] / P_pi[first, first] - Q[k] / P_pi[first, k])
            
                A[i] = (P_pi[first, i] / tot1) * ((Q[i] / P_pi[first, i] - Q[first] / P_pi[first, first]) * tot2 + tot3)
        
            lambdas = {}
            lambdas[first] = lambda_first(T, first, A, I, Q, P_pi, gamma, r, V0)
        
            for i in I:
                lambdas[i] = A[i] * lambdas[first]
        

            tot_lambdas = 0
            for i in I:
                tot_lambdas += lambdas[i]
        
            V = np.zeros(T + 1)
            for k in range(T + 1):
                if k == first:
                    V[k] = U_p_inv((1 / P_pi[first, first]) * (Q[first] * lambdas[first] + tot_lambdas), gamma)
                else:
                    V[k] = U_p_inv((1 / P_pi[first, k]) * (Q[k] * lambdas[first] - (0 if not k in I else lambdas[k])), gamma) 
        
            if good_lambdas(I, lambdas) and good_V(T, first, V):
                CEU = np.dot(P_pi[first,:], U(V, gamma))
                VS.append(V)
                CEUS.append(CEU)
        
    if len(CEUS) == 0:
        print('\n\n *** EMPTY ***\n\n')
        return None
        
    max_CEU = max(CEUS)  
    i_max = np.argmax(CEUS)
    V_max = VS[i_max]
            
    return (V_max, max_CEU)