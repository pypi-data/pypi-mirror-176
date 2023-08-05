from math import *
import numpy as np
from scipy.interpolate import interp1d
import sys
from scipy import optimize
from scipy.optimize import fmin
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rc('font', family='serif')
mpl.rcParams.update({'font.size': 12})
mpl.rcParams.update({'legend.labelspacing':0.25, 'legend.fontsize': 12})
mpl.rcParams.update({'errorbar.capsize': 4})


## Function which computes a distance from the Galactic centre

def R (D, gl, gb, Rsun):

    if (abs(gb) > pi / 2.0) or (abs(gl) > 2*pi):
        print ('gl and gb must be in radians', gl, gb)
        sys.exit(0)

    res = sqrt ( Rsun**2.0 + (D*cos(gb))**2.0 - 2.0 * D * Rsun * cos(gb)*cos(gl))

    return res

## Function which computes height above the galactic plane
def z (D, gl, gb):

    if abs(gb) > pi / 2.0:
        print ('gb must be in radians', gb)
        sys.exit(0)

    res = D * sin (gb)

    return res

## Function which computes Galactic prior
## hz is the typical height above the Galactic plane
## hr is the typical radius
def fD (D, gl, gb, hz, hr, Rsun):

    Rv = R (D, gl, gb, Rsun)
    zv = z (D, gl, gb)

    #hz = 0.33
    #hr = 1.70

    res = D**2 * Rv**1.9 * exp(-abs(zv) / hz - Rv / hr)

    return res

## Conditional probability to measure parallax if distance is fixed
## More details can be found in Igoshev, Verbunt & Cator (2016) A&A, 591, A123, 10
## and in Igoshev, Perets & Hallakoun (2022) ArXiv: 2209.09915
def g (D, varpi, sigma_varpi):

    res = 1.0 / sqrt(2.0 * pi) / sigma_varpi * exp (- (1.0 / D - varpi)**2.0 / 2.0 / sigma_varpi**2.0)

    return res

## Prior for transversal velocities based on two independant Gaussians
def prior_vt (vt, sigma):

    res = vt / sigma**2.0 * exp(-vt**2.0 / 2.0 / sigma**2.0)

    return res


def diff (theta, meas, vt, D, verbose=False):

    mu_alpha_ap, sigma_mualpha, mu_delta_ap, sigma_mudelta, varpi, sigma_varpi, gl, gb = meas

    #print (meas))

    res = pow(mu_alpha_ap - vt *sin(theta) / (4.74 * D), 2.0) / (2.0*sigma_mualpha ** 2) + pow(mu_delta_ap - vt *cos(theta) / (4.74 * D), 2.0) / (2.0*sigma_mudelta ** 2)

    if verbose:
        print ('theta = ', theta, ' res = ', res)


    return res

def diff1 (theta, meas, vt, D, add):

    mu_alpha_ap, sigma_mualpha, mu_delta_ap, sigma_mudelta, varpi, sigma_varpi, gl, gb = meas

    res = pow(mu_alpha_ap - vt *sin(theta) / (4.74 * D), 2.0) / (2.0*sigma_mualpha ** 2) + pow(mu_delta_ap - vt *cos(theta) / (4.74 * D), 2.0) / (2.0*sigma_mudelta ** 2)

    ksi = vt / (4.74 * D) / sqrt(mu_alpha_ap ** 2.0 + mu_delta_ap ** 2.0)

    return res-add

## Procedure to optimise and integrate over angles theta
## For technical details, see Appendix A in Igoshev & Perets (2022) ArXiv: 2209.09915

def find_theta_max (meas, vt, D):

    mu_alpha_ap, sigma_mualpha, mu_delta_ap, sigma_mudelta, varpi, sigma_varpi, gl, gb = meas

    theta0 = atan(mu_alpha_ap / mu_delta_ap) + pi

    diff0 = diff (theta0, meas, vt, D)

    theta01 = atan(mu_alpha_ap / mu_delta_ap)

    diff01 = diff (theta01, meas, vt, D)

    if diff0 > diff01:
        theta0 = theta01
        diff0 = diff01

    #print ('Init est: ', diff0,  exp(-diff0), ' at ', theta0)

    if diff0 < 300:

        res = fmin(diff, theta0, args=(meas, vt, D), xtol=1e-8, disp=False)

        #print ('minimun: ', res)

        theta0 = res[0]

        diff0 = diff (theta0, meas, vt, D)

        theta1 = optimize.newton(diff1, theta0, args=(meas, vt, D, diff0+8.0))

        diff1v = diff (theta1, meas, vt, D)

        #print (theta0, diff0)            
        #print (theta1, diff1v)

        df = abs(theta1 - theta0) / 10.0

        #print ('Df is: ', df)

        sumv = 0

        for i in range (-10, 11):
            theta = theta0 + df * i

            sumv += exp( - diff (theta, meas, vt, D)) * df

            #print (i, theta, exp( - diff (theta, meas, vt, D)) * df)

    else:

        sumv = 0.0

    ksi = vt / (4.74 * D) / sqrt(mu_alpha_ap ** 2.0 + mu_delta_ap ** 2.0)

    mult = exp (-(mu_alpha_ap - ksi * mu_alpha_ap)**2.0 / (2.0 * sigma_mualpha**2.0) - (mu_delta_ap - ksi * mu_delta_ap)**2.0 / (2.0 * sigma_mudelta ** 2.0)  )

    theta_ = atan(mu_alpha_ap / mu_delta_ap) + pi

    diff_ = diff (theta_, meas, vt, D)


    sumv = sumv / mult


    #print ('Final res: ', sumv)


    return sumv


def compl_post (vt, meas, Rsun, hz, hr, sigma):

    mu_alpha_ap, sigma_mualpha, mu_delta_ap, sigma_mudelta, varpi, sigma_varpi, gl, gb = meas

    ## Catching possible errors related to the cases when proper motion is not well measured

    if (abs(mu_alpha_ap / sigma_mualpha) < 6) or (abs(mu_delta_ap / sigma_mudelta) < 6):
        print ('Error: code works reliably when proper motion is well-measured i.e. pmra / pmra_error > 6 and pmdec / pmdec_error > 6')
        sys.exit(1)

    D = vt / ( 4.74 * sqrt(mu_alpha_ap ** 2.0 + mu_delta_ap ** 2.0))

    fDv = fD (D, gl, gb, hz, hr, Rsun)
    gv = g (D, varpi, sigma_varpi)

    kappa = find_theta_max (meas, vt, D)

    prior_v = prior_vt (vt, sigma)

    res = fDv * gv * prior_v * kappa

    return res



def  compute_posterior (meas, Rsun = 8.34, hz = 0.33, hr = 1.70, min_vt = 10, max_vt = 2500, n_step = 100, sigma = 1000):

    vtl = []
    pvtl = []

    step = abs(max_vt - min_vt) / float(n_step)

    ## Let us try to catch errors here
    if (min_vt < 0) or (max_vt < 0):
        print ('Error: vt can only be positive.')
        print ('Please set min_vt and max_vt at values greater than 0')
        return [0,0,0,0,0]
    if n_step <= 0:
        print ('Error: n_step has to be positive and integer')
        return [0,0,0,0,0]

    if abs(Rsun - 8.5) > 3:
        print ('Warning: Rsun value is weird: ', Rsun)
        print ('Recommended value is 8.34 kpc')

    if hz <= 0:
        print ('Error: exponential hight hz can only be positive')
        return [0,0,0,0,0]

    if hr <= 0:
        print ('Error: exponential radius hr can only be positive')
        return [0,0,0,0,0]
    if sigma <= 0:
        print ('Error: velocity prior parameter sigma must be positive')
        return [0,0,0,0,0]


    

    for i in range (0, n_step):

        vt = min_vt + step * i

        vtl.append  (vt)
        pvtl.append (compl_post (vt, meas, Rsun, hz, hr, sigma))

    pvtl = np.asarray (pvtl) / np.max(pvtl)

    cumsump = np.cumsum(pvtl) / np.sum(pvtl)

    idx025 = (np.abs(cumsump - 0.025)).argmin()
    idx50  = (np.abs(cumsump - 0.5)).argmin()
    idx975 = (np.abs(cumsump - 0.975)).argmin()

    return [vtl, pvtl, idx025, idx50, idx975]




