
## Pricing Algorithm
 
This algorithm calculates the price of a financial derivative using finite differences.
  It solves a system of equations represented by a tridiagonal matrix.
 
 
The algorithm iterates over each row of the tridiagonal matrix and solves the system of equations.
 
 
We have:
$$\frac{1}{2}\sigma^{2}S^{2}\frac{\partial^{2}V}{\partial S^{2}} + rS\frac{\partial V}{\partial S} = rV - \frac{\partial V}{\partial t}$$

We also have the following discrete derivatives:
$$\frac{\partial V}{\partial t} = \frac{G_{i+1,j}-G_{i,j}}{dt}$$
$$\frac{\partial V}{\partial S} = \frac{G_{i,j+1}-G_{i,j-1}}{2 dS}$$
$$\frac{\partial^{2} V}{\partial S^{2}} = \frac{G_{i,j+1}-2G_{i,j}+G_{i,j-1}}{dS^{2}}$$

Thus, we get:
$$\frac{1}{2}\sigma^{2}S_{j}^{2} \frac{G_{i,j+1}-2G_{i,j}+G_{i,j-1}}{dS^{2}} + rS_{j} \frac{G_{i,j+1}-G_{i,j-1}}{2 dS} = rG_{i,j} - \frac{G_{i+1,j}-G_{i,j}}{dt}$$
Which leads to:

$$G_{i+1,j} = -dt \left( \frac{1}{2}\sigma^{2}S_{j}^{2} \frac{G_{i,j+1}-2G_{i,j}+G_{i,j-1}}{dS^{2}} + rS_j \frac{G_{i,j+1}-G_{i,j-1}}{2 dS} - rG_{i,j} \right) - G_{i,j}$$

We can rewrite this equation as:
$$G_{i+1,j} = \alpha G_{i,j+1} + \beta G_{i,j} + \gamma G_{i,j-1}$$

With:
$$\alpha = -\frac{1}{2}dt \left( \frac{1}{dS^{2}}\sigma^{2}S_{j}^{2} + \frac{rS_j}{dS} \right)$$
$$\beta = -1 + dt \left( \frac{1}{dS^{2}}\sigma^{2}S_{j}^{2} + r \right)$$
$$\gamma = -\frac{1}{2}dt \left( \frac{1}{dS^{2}}\sigma^{2}S_{j}^{2} - \frac{rS_j}{dS} \right)$$

Therefore, for each row, we get a tridiagonal matrix. We can now solve this system.

G is the matrix of the option price at each time step and each price step. We have:
$$G_{i,j} = V(S_{j},t_{i})$$
with:
$$S_{j} = j \times dS$$
$$t_{i} = i \times dt$$

Therefore for a given time step, we can calculate the price of the option at each price step. We can then iterate over each time step to get the price of the option at each time step and each price step.
We get the following tridiagonal system :

$$ G_{i+1} = A G_{i}$$

with:
$$A = \begin{pmatrix}
\beta_{1} & \gamma_{1} & 0 & 0 & \cdots & 0 & 0 & 0 \\
\alpha_{2} & \beta_{2} & \gamma_{2} & 0 & \cdots & 0 & 0 & 0 \\
0 & \alpha_{3} & \beta_{3} & \gamma_{3} & \cdots & 0 & 0 & 0 \\
\vdots  & \vdots  & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \cdots & \alpha_{N-2} & \beta_{N-2} & \gamma_{N-2} \\
0 & 0 & 0 & 0 & \cdots & 0 & \alpha_{N-1} & \beta_{N-1} \\

\end{pmatrix}$$
 
 We'll apply this development to an european put which is issued at time 0 and expires at time T, with a strike K. Its payoff at expiry is given by:
    $$max(Ke^{-rT}-S_{T},0)$$
The boundary conditions are:
    $$G_{i,0} = K e^{-r t_{i}}$$
    $$G_{i,N} = 0$$
    $$G_{T,j} = max(K-S_{j},0)$$
The final condition gives us the value of the option at expiry. We can then calculate the value of the option at each time step and each price step by inversing the matrix A. This is done in the script "pricing_eu_.py".
