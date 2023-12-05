
## Pricing Algorithm
 
This algorithm calculates the price of a financial derivative using the Thomas algorithm.
  It solves a system of equations represented by a tridiagonal matrix.
 
 
The algorithm iterates over each row of the tridiagonal matrix and solves the system of equations using the Thomas algorithm.
 
 
We have:
$$\frac{1}{2}\sigma^{2}S^{2}\frac{\partial^{2}V}{\partial S^{2}} + rS\frac{\partial V}{\partial S} = rV + \frac{\partial V}{\partial \tau}$$

We also have the following discrete derivatives:
$$\frac{\partial V}{\partial t} = \frac{G_{i+1,j}-G_{i,j}}{dt}$$
$$\frac{\partial V}{\partial S} = \frac{G_{i,j+1}-G_{i,j-1}}{2 dS}$$
$$\frac{\partial^{2} V}{\partial S^{2}} = \frac{G_{i,j+1}-2G_{i,j}+G_{i,j-1}}{dS^{2}}$$

Thus, we get:
$$\frac{1}{2}\sigma^{2}S_{j}^{2} \frac{G_{i,j+1}-2G_{i,j}+G_{i,j-1}}{dS^{2}} + rS_{j} \frac{G_{i,j+1}-G_{i,j-1}}{2 dS} = rG_{i,j} + \frac{G_{i+1,j}-G_{i,j}}{dt}$$
Which leads to:

$$G_{i+1,j} = dt \left( \frac{1}{2}\sigma^{2}S_{j}^{2} \frac{G_{i,j+1}-2G_{i,j}+G_{i,j-1}}{dS^{2}} + rS_j \frac{G_{i,j+1}-G_{i,j-1}}{2 dS} - rG_{i,j} \right) + G_{i,j}$$

We can rewrite this equation as:
$$G_{i+1,j} = \alpha G_{i,j+1} + \beta G_{i,j} + \gamma G_{i,j-1}$$

With:
$$\alpha = \frac{1}{2}dt \left( \frac{1}{dS^{2}}\sigma^{2}S_{j}^{2} + \frac{rS_j}{dS} \right)$$
$$\beta = 1 - dt \left( \frac{1}{dS^{2}}\sigma^{2}S_{j}^{2} + r \right)$$
$$\gamma = \frac{1}{2}dt \left( \frac{1}{dS^{2}}\sigma^{2}S_{j}^{2} - \frac{rS_j}{dS} \right)$$

Therefore for example, if we're working on a call option, starting from $G_{0,j} = max(S_j - K, 0)$, we can calculate $G_{i,j}$ for all i and j.

