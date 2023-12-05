import numpy as np
from scipy.linalg import solve
import plotly.graph_objects as go

class EuropeanOptionFD:
    def __init__(self, S_max, K, T, r, sigma, M, N, option_type='call'):
        self.S_max = S_max
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.M, self.N = M, N
        self.dt = self.T / self.N
        self.dS = self.S_max / self.M
        self.s = np.linspace(0, self.S_max + self.dS, self.M+1)
        self.t = np.linspace(0, self.T + self.dt, self.N+1)
        self.j_values = np.arange(0, self.M + 1)
        self.i_values = np.arange(0, self.N + 1)
        self.option_type = option_type
        self.grid = np.zeros(shape=(self.N + 1, self.M + 1))
        

    def payoff(self,j,i):
        if self.option_type == 'call':
            return np.maximum(0, self.dS * j - self.K* np.exp(-self.r * self.dt * i))
        elif self.option_type == 'put':
            return np.maximum(0, self.K*np.exp(-self.r * self.dt * i) - self.dS * j)

    def alpha(self, j):
        return 0.5 * self.dt * (self.sigma**2 * j**2 + self.r * j)

    def beta(self, j):
        return 1.0 - self.dt * (self.sigma**2 * j**2 + self.r)

    def gamma(self, j):
        return 0.5 * self.dt * (self.sigma**2 * j**2 - self.r * j)

    
    def solve_fd(self):
        self.grid[0, :] = self.payoff(self.j_values,0)
        self.grid[:, -1] = self.payoff(self.M, self.i_values)
        self.grid[:, 0] = self.payoff(0, self.i_values)
        for i in self.i_values[1:] :
            for j in self.j_values[1:-1]:
                self.grid[i, j] = self.alpha(j) * self.grid[i-1, j-1] + \
                                  self.beta(j) * self.grid[i-1, j] + \
                                  self.gamma(j) * self.grid[i-1, j+1]

    def delta_greek(self, i, j):
        return (self.grid[i, j + 1] - self.grid[i, j - 1]) / (2 * self.dS)

    def gamma_greek(self, i, j):
        return (self.grid[i, j + 1] - 2 * self.grid[i, j] + self.grid[i, j - 1]) / (self.dS ** 2)

    def theta_greek(self, i, j):
        return -(self.grid[i + 1, j] - self.grid[i, j]) / self.dt
    
    def compute_greeks(self):
        self.delta_grid = np.zeros_like(self.grid)
        self.gamma_grid = np.zeros_like(self.grid)
        self.theta_grid = np.zeros_like(self.grid)
        for i in range(1, self.N-1):
            for j in range(1, self.M-1):
                self.delta_grid[i, j] = self.delta_greek(i, j)
                self.gamma_grid[i, j] = self.gamma_greek(i, j)
                self.theta_grid[i, j] = self.theta_greek(i, j)
                
def main():
    S_max = int(input('Enter S_max: '))
    K = int(input('Enter K: '))
    T = int(input('Enter T: '))
    r = float(input('Enter r: '))
    sigma = float(input('Enter sigma: '))
    M = int(input('Enter M: '))
    stability_condition = sigma**2 * M**2
    print('Stability condition: N>', stability_condition)
    N = int(input('Enter N : '))
    
    option_type = input('Enter option type: ')
    eu_option = EuropeanOptionFD(150, 100, 1, 0.08, 0.2, 100,2000, option_type=option_type)
    eu_option.solve_fd()
    # Create a surface plot
    fig = go.Figure(data=[go.Surface(z=eu_option.grid)])

    # Set plot title and labels
    fig.update_layout(title='Option Price', autosize=False,
                      width=500, height=500,
                      margin=dict(l=65, r=50, b=65, t=90),
                      scene=dict(xaxis_title='Stock Price',
                                 yaxis_title='Time Step',
                                 zaxis_title='Option Price'))

    # Show the plot
    fig.show()
    
    eu_option.compute_greeks()
    # Create a surface plot
    fig_delta = go.Figure(data=[go.Surface(z=eu_option.delta_grid)])
    fig_delta.update_layout(title='Delta', autosize=False,
                        width=500, height=500,
                        margin=dict(l=65, r=50, b=65, t=90),
                        scene=dict(xaxis_title='Stock Price',
                                     yaxis_title='Time Step',
                                     zaxis_title='Delta'))
    fig_delta.show()
    
    fig_gamma = go.Figure(data=[go.Surface(z=eu_option.gamma_grid)])
    fig_gamma.update_layout(title='Gamma', autosize=False,
                        width=500, height=500,
                        margin=dict(l=65, r=50, b=65, t=90),
                        scene=dict(xaxis_title='Stock Price',
                                     yaxis_title='Time Step',
                                     zaxis_title='Gamma'))
    fig_gamma.show()
    
    fig_theta = go.Figure(data=[go.Surface(z=eu_option.theta_grid)])
    fig_theta.update_layout(title='Theta', autosize=False,
                        width=500, height=500,
                        margin=dict(l=65, r=50, b=65, t=90),
                        scene=dict(xaxis_title='Stock Price',
                                     yaxis_title='Time Step',
                                     zaxis_title='Theta'))
    fig_theta.show()
    
    
if __name__ == '__main__':
    main()