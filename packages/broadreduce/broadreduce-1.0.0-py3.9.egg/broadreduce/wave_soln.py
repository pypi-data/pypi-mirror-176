import os
import numpy as np
from matplotlib import pyplot as plt

from .utils import normalize

from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter

from astropy.modeling import models, fitting
from astropy.modeling.models import custom_model


def subtract_continuum(xs, sky_flux, degree=6, iterations=5):
    """
        Subtract the continuum from a spectra using iterative polynomial subtraction.
    """
    flux_subbed = np.copy(sky_flux)
    fit_mask = np.ones(len(xs)) == 1

    # Iteratively fit a 1D polynomial, subtract the polynomial,
    # then mask out positively-valued residuals.
    for n in range(iterations):
        fit = np.poly1d(np.polyfit(xs[fit_mask], flux_subbed[fit_mask], deg=degree))
        flux_subbed -= fit(xs)
        fit_mask = flux_subbed < 0

    return flux_subbed


def trim_duplicates(guesses):
    """
        Trim the duplicates of guesses for line peaks from an array. For those that are all nearby,
        use the mean of those nearby ones as the guess.
    """
    guesses_trimmed = []
    for i in range(len(guesses)):
        guess = guesses[i]
        nearby = [guess]

        for j in range(len(guesses)):
            if j == i:
                continue
            if abs(guesses[j] - guess) < 10:
                nearby.append(guesses[j])

        nearby_avg = np.round(np.mean(nearby), 4)
        if nearby_avg not in guesses_trimmed:
            guesses_trimmed.append(nearby_avg)
    return guesses_trimmed


def slice_plot(x, y, t, i, theta):
    plt.scatter(x, y, s=2, color="black")
    plt.plot(x, t(x), color="red")
    plt.text(i, 0.95, "Good Amp: " + str(theta[0]))
    plt.text(i, 0.90, "Good Mean: " + str(theta[1]))
    plt.text(i, 0.85, "Good Stddev: " + str(theta[2]))
    plt.text(i, 0.78, "Good " + r'$R^2$' + ": " + str(theta[3]))
    plt.show()


def adjust_for_binning(coeffs, binning=4):
    coeffs = coeffs[::-1]
    new_coeffs = []
    print(coeffs)
    for i in range(len(coeffs)):
        this_val = coeffs[i] * (binning ** i)
        new_coeffs.append(this_val)
    return new_coeffs[::-1]


def wavesolve(spec_x, spec_y, guesses, params=None,
              slice_width=100, max_stddev=50, max_rsqr=1, y_min=0.09, guess_threshold=25,
              fit_order=3, plot_results=True, plot_slices=False, plot_dir="pngs/"):
    """
        Get the polynomial coefficients for a given arc frame.
        This is the naive solution, which will then be tweaked for individual sky frames.

        :param spec_x: x values for the arc spectrum. Likely just a numpy arange of integers
        :param spec_y: flux values for the y spectrum
        :param guesses: A 2xN array containing:
            1 - The naive locations in x for the emission peaks
            2 - The associated wavelengths
        :param slice_width: The width, in array length, to slice up the spectrum in order to
                            look for Gaussian peaks.
        :param max_stddev: The maximum allowable standard deviation for a Gaussian fit.
        :param max_rsqr: The maximum allowable reduced r-squared value for a Gaussian fit
        :param y_min: The minimum allowable flux strength (after normalization) of a line.
        :param guess_threshold: The maximum allowable distance (in pixels) that a guess will be
                                considered matching a found Gaussian peak.
        :param fit_order: The order of the polynomial fit to the lines. int, optional
        :param plot_slices: Whether or not to save the individual slices for debugging purposes.
    """

    x_guesses, wavelengths = guesses

    x_chunks = np.arange(0, len(spec_x), int(slice_width / 4))

    fitter = fitting.LevMarLSQFitter()

    gaussian_means = []

    # Split spectra up into chunks and look for Gaussians
    for i in x_chunks:
        x_slice = np.copy(spec_x[i: i + slice_width])
        y_slice = np.copy(spec_y[i: i + slice_width])

        y_max = np.max(y_slice)

        if y_max < y_min:
            continue

        # Normalize the individual slice to be in the range of 0-1
        y_slice -= np.min(y_slice)
        y_slice /= np.max(y_slice)

        # Fit a gaussian model to the available data in the slice, and get the R^2 statistic
        gauss_model = models.Gaussian1D(amplitude=0.5, mean=i + slice_width / 2, stddev=5)
        t = fitter(gauss_model, x_slice, y_slice)
        t_amp, t_mean, t_stddev = t.amplitude.value, t.mean.value, t.stddev.value
        t_rsqr = np.sum((y_slice - t(x_slice)) ** 2)

        # Now we run quality assurance
        # good_fit is realistically the only one that actually matters
        # The remaining parameters are just for plotting and debugging purposes
        good_fit = True
        amp_check, mean_check, stddev_check, rsqr_check = True, True, True, True

        if t_rsqr > max_rsqr:
            good_fit = False
            rsqr_check = False

        # The mean needs to be within the slice
        if t_mean < i or t_mean > i + slice_width:
            good_fit = False
            mean_check = False

        # The amplitude should be very close to 1 if there is a detected line
        if t_amp > 1.1 or t_amp < 0.9:
            good_fit = False
            amp_check = False

        # The standard deviation of the line should be reasonable
        if t_stddev > max_stddev:
            good_fit = False
            stddev_check = False

        if good_fit:
            gaussian_means.append(t_mean)

        if plot_slices:
            slice_plot(x_slice, y_slice, t, i, [amp_check, mean_check, stddev_check, rsqr_check])

    # Now that we have all of the line guesses, we need to trim off duplicates
    gaussian_means = trim_duplicates(gaussian_means)

    x_good, l_good = [], []
    # Now we look for good guesses
    for n in gaussian_means:
        residuals = np.abs(x_guesses - n)
        residual_min = np.min(residuals)

        if residual_min < guess_threshold:
            x_good.append(n)
            l_good.append(wavelengths[np.argmin(residuals)])

    # Fit a polynomail to the available xs and wavelengths
    coeffs = np.polyfit(x_good, l_good, deg=fit_order)

    if plot_results:
        if not os.path.isdir(plot_dir):
            os.makedirs(plot_dir)

        fig, ax = plt.subplots(1, 2, facecolor="white")

        fig.set_figheight(6)
        fig.set_figwidth(12)

        poly = np.poly1d(coeffs)

        ax[0].plot(spec_x, poly(spec_x), color="black", label="Polynomial Fit, order=" + str(fit_order))
        ax[0].scatter(x_good, l_good, color="Red", label="individual")
        ax[0].legend()

        ax[1].scatter(x_good, poly(x_good) - l_good, color="Red")
        ax[1].axhline(0, color="black", alpha=0.4)

        ax[0].set_xlabel("Position [pix]")
        ax[0].set_ylabel("Wavelength [angstrom]")
        ax[0].set_xticks(np.arange(0, 2250, 250))
        ax[0].grid()

        ax[1].set_xlabel("Position [pix]")
        ax[1].set_ylabel("Residuals [angstrom]")

        plt.tight_layout()
        plt.savefig(plot_dir + "wavesoln_fit.png", dpi=150)

        plt.figure(figsize=(12, 3), facecolor="white")
        plt.plot(spec_x, spec_y, color="black", lw=5)
        for n in gaussian_means:
            plt.axvline(n, color="red")

        plt.tight_layout()
        plt.savefig(plot_dir + "naive_soln.png", dpi=150)

    return coeffs


def tweak_sky_polynomial(x_sky, y_sky, l_mod, f_mod, guess_init, config=None, 
                         plot_results=True, plot_fn='tweaked_wsol.png'):
    """ Tweak the sky polynomial using a given solar spectrum around the Ca H+K lines


    :param x_sky: The x-values for the sky (likely just a np.arange)
    :type x_sky: array_like
    :param y_sky: The flux values for the sky, same length as x_sky
    :type y_sky: array_like
    :param l_mod: The wavelengths for the solar model
    :type l_mod: array_like
    :param f_mod: The corresponding fluxes for the solar model
    :type f_mod: array_like
    :param guess_init: The initial guesses for the sky model (obtained from the sky lines)
    :type guess_init: array_like
    :param config: Optional broadreduce config parameters, defaults to None
    :type config: dict, optional
    :param plot_results: Plot results from the tweaking, defaults to True
    :type plot_results: bool, optional
    :param plot_fn: The filename to save plotting results, defaults to 'tweaked_wsol.png'
    :type plot_fn: str, optional
    :return: The coefficients of the tweaked wavelength solution
    :rtype: array_like
    """
    
    # Assume that the sky model hasn't been normalized yet
    y_sky = normalize(y_sky)
    
    @custom_model
    def mod_test(x, a=0., b=0., yshift=0., yscale=1.):
        """ This is the model to tweak the wavelength solution by fitting a section of the solar spectrum
            to a given sky model region, correcting for the shift and pixel scale

        :param x: _description_
        :type x: _type_
        :param a: The parameter that changes the shift, defaults to 0
        :type a: float, optional
        :param b: The parameter that changes the pixel scale, defaults to 0
        :type b: float, optional
        :param yshift: Parameter to move the sky model up or down, defaults to 0
        :type yshift: int, optional
        :param yscale: Parameter to shift the sky model in y, defaults to 1
        :type yscale: int, optional
        :return: The sky model in y
        :rtype: _type_
        """
        theta = np.copy(guess_init)
        theta[3] += a
        theta[2] += b
        
        l_init = np.poly1d(theta)
        l_sky = l_init(x_sky)
        return interp1d(l_sky, y_sky)(x) * yscale + yshift
    
    m_init = mod_test()
    fit = fitting.LevMarLSQFitter()
    m = fit(m_init, l_mod, f_mod)
    
    adjusted_theta = np.copy(guess_init)
    adjusted_theta[3] += m.a.value
    adjusted_theta[2] += m.b.value
    
    if plot_results:
        plt.figure(figsize=(10, 5), facecolor="white")

        plt.plot(l_mod, m(l_mod), label="Adjusted sky mod", lw=3, color="black")
        plt.plot(l_mod, f_mod, label="Bass2000 Solar Spectrum", lw=3, color="red")

        plt.text(np.min(l_mod), 0.95, "Tweaks")

        plt.text(np.min(l_mod), 0.9, r'$a_0 $' + " += " + str(m.a.value))
        plt.text(np.min(l_mod), 0.85, r'$a_1 $' + " += " + str(m.b.value))
        
        plt.xlabel("Wavelength [Angstrom]")
        plt.ylabel("Normalized Flux")
        
        plt.legend(loc='lower right')
        plt.tight_layout()

        plt.savefig(plot_fn, dpi=200)
    
    return adjusted_theta
