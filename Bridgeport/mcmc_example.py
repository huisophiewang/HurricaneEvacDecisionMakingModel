import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import norm


 


def calc_posterior_analytical(data, x, mu_0, sigma_0):
    sigma = 1.
    n = len(data)
    mu_post = (mu_0 / sigma_0**2 + data.sum() / sigma**2) / (1. / sigma_0**2 + n / sigma**2)
    print mu_post
    sigma_post = (1. / sigma_0**2 + n / sigma**2)**-1
    print sigma_post
    return norm(mu_post, np.sqrt(sigma_post)).pdf(x)

if __name__ == '__main__':
    sns.set_style('white')
    sns.set_context('talk')
    np.random.seed(123)
    data = np.random.randn(20)
    print data
    
#     ax = plt.subplot()
#     sns.distplot(data, kde=False, ax=ax)
#     _ = ax.set(title='Histogram of observed data', xlabel='x', ylabel='# observations');
#     sns.plt.show()
    
    ax = plt.subplot()
    x = np.linspace(-1, 1, 500)
    posterior_analytical = calc_posterior_analytical(data, x, 0., 1.)
    ax.plot(x, posterior_analytical)
    ax.set(xlabel='mu', ylabel='belief', title='Analytical posterior');
    sns.despine()
    sns.plt.show()


    