# ceu-portfolio
Optimization code for the paper:
    
D. Petturiti and B. Vantaggi. _The impact of ambiguity on dynamic portfolio selection in the epsilon-contaminated binomial market model_. **European Journal of Operational Research**, 314(3):1029–1039, 2024.

# Requirements
The code has been tested on Python 3.10 with the following libraries:
* **matplotlib** 3.7.1
* **numpy** 1.26.4
* **pandas** 1.5.3
* **pyomo** 6.6.1
* **scipy** 1.10.1
* **yfinance** 0.2.40

Reference to the library **pyomo** is here: http://www.pyomo.org/

Reference to the library **yfinance** is here: https://pypi.org/project/yfinance/

The code necessitates of the **bonmin** solver that can be downloaded here: https://www.coin-or.org/Bonmin/

The **bonmin** solver should be located in a folder and the path to that folder should be inserted in the variable **optimizer_path** in the top of file **CEU_portfolio.py**

# File inventory
**CEU_portfolio.py**: Optimization code that finds the optimal final wealth (either as a non-linear programming problem or as a combinatorial problem) relying on the following parameters
* _T_: Time horizon (in periods)
* _epsilon_: Ambiguity parameter in [0,1)
* _p_: Real-world probability of an "up" move over a single period
* _u_: "up" move coefficient
* _d_: "down" move coefficient
* _gamma_: CRRA relative risk aversion parameter
* _V0_: Initial positive wealth
* _r_: Risk-free interest rate over a single period

**graph_3D_epsilon_star_p_r.py**: Plots the 3D graph of epsilon_star as a function of p and r, together with the contour plot. 

**graph_3D_epsilon_star_p_T.py**: Plots the 3D graph of epsilon_star as a function of p and T.

**graph_gamma.py**: Plots the graph of epsilon_star as a function of gamma for several time horizons.

**graph_norm_CEU_epsilon.py**: Plots the graph of normalized CEU as a function of epsilon.

**graph_pcloseq.py**: Plots epsilon_star as a function of T for values of p close to q.

**META_calibration**: Market calibration for the META stock.

**META_CEU_portfolio.py**: Computes the optimal portfolio for the market calibrated META stock with both
the non-linear programming problem and the combinatorial problem.
