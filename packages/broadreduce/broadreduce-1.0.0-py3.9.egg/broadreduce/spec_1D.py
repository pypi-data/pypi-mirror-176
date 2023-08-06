import wave
import numpy as np
from astropy.visualization import ZScaleInterval
from.binning import bin_individual
from .utils import *

from matplotlib import pyplot as plt
import broadreduce


def collapse_1D_old(processing_dir, imin, inner_slits, im_index, binning=5, padding=20, xpadding=10, plot_results=True):
    inner_slits = inner_slits[im_index]

    central_slit = imin[inner_slits[0] + padding:inner_slits[1] - padding, xpadding:-xpadding]
    central_slit_binned = bin_individual(np.transpose(central_slit), binning, axis=0)

    prof_1D = np.sum(central_slit, axis=0)
    prof_1D_smooth = smooth(prof_1D, window_length=51)

    slit_profile = np.sum(central_slit_binned, axis=1)

    prof_1D_binned = np.sum(central_slit_binned, axis=0)
    prof_1D_binned = smooth(prof_1D_binned, window_length=51)

    xs = np.arange(xpadding, central_slit.shape[1] + xpadding, 1)
    xs_binned = np.arange(xpadding, central_slit.shape[1] + xpadding, binning)

    if plot_results:
        fig, ax = plt.subplots(2 ,1, sharex=True, facecolor="white")
        fig.set_figheight(4)
        fig.set_figwidth(12)

        ax[0].plot(xs, prof_1D, color="black", alpha=0.5)
        ax[0].plot(xs, prof_1D_smooth, label="Bin size = 2", color="black", lw=3)

        # ax[0].plot(xs_binned[:len(prof_1D_binned)], prof_1D_binned / binning, label="Bin size = " + str(2 * binning))

        zscale = ZScaleInterval(contrast=0.5)
        scale = zscale.get_limits(central_slit)
        ax[1].imshow(central_slit, vmin=scale[0], vmax= scale[1], cmap="Greys_r")

        plt.xlabel("Xpos [pixel, uncorrected]")
        ax[0].set_ylabel("Summed Flux")
        ax[0].set_ylim(0, np.nanmax(prof_1D) * 1.1)
        ax[0].grid(alpha=0.3)
        ax[1].set_yticks([])
        ax[0].legend()
        plt.tight_layout()
        plt.subplots_adjust(wspace=0)
        plt.savefig("pngs/1DSpec_init.png", dpi=150)

        plt.figure(figsize=(5,5))

        plt.tight_layout()


def collapse_1D(spec_2D, slits, params, det=1, wavelength_binning=None, plot_results=False, plot_fn=None):
    
    # First get the regions and the gauss fit to the central portion of the slit profile
    regions, gauss_model = get_flux_region(spec_2D, slits, stddev_multiplier=1.2,
                                                       det=det, use_upper_half=True, 
                                                       plot_results=plot_results, plot_fn=plot_fn)
    binning = params["FINAL_BINNING"]

    if wavelength_binning is not None:
        binning[0] = wavelength_binning

    hb = broadreduce.heavy_bin(spec_2D, region=regions, detector=det, 
                               wavelength_binning=binning[0], spatial_binning=binning[1], outfile=None)

    binned_gauss = gauss_model.copy()
    binned_gauss.amplitude = 1
    binned_gauss.mean = hb.shape[0] / 2
    binned_gauss.stddev /= (binning[1])
    
    weights = binned_gauss(np.arange(hb.shape[0])) 
    
    # Weight the fully binned array
    for i in range(hb.shape[0]):
        hb[i] *= weights[i]
    
    spec_1D = np.sum(hb, axis=0)
    spec_1D = gaussian_filter(spec_1D, 1)
    
    inshape = spec_2D.shape
    xs = np.mgrid[:inshape[0], :inshape[1]][1]
    binned_xs = broadreduce.heavy_bin(xs, region=regions, 
                                      wavelength_binning=binning[0], spatial_binning=binning[1], outfile=None,
                                      method=np.median)[0]
    
    return binned_xs, spec_1D, hb


def get_flux_region(img, inner_slits, det=1, stddev_multiplier=1.5, use_upper_half=True,
                    plot_results=True, plot_fn=None):
        
    slit = np.copy(inner_slits)
    if use_upper_half:
        img = np.copy(img[:, int(img.shape[1] / 2):])
    
    slit_prof = slit_profile(img)
    

    xs = np.arange(0, len(slit_prof), 1)
    x_low, x_high = np.argmin(np.abs(xs - slit[0])), np.argmin(np.abs(xs - slit[1]))
    
    x_region = xs[x_low:x_high]
    prof_region = slit_prof[x_low:x_high]
    
    prof_region /= np.nanmax(prof_region)
    prof_region = gaussian_filter(prof_region, 5)
    prof_region /= np.nanmax(prof_region)

    prof_region[prof_region < 0] = 0
    
    gauss = models.Gaussian1D(amplitude=1, mean = np.sum(slit) / 2, stddev=(slit[1] - slit[0]) / 4)
    gauss.amplitude.fixed
    fitter = fitting.LevMarLSQFitter()
    
    g_out = fitter(gauss, x_region, prof_region)
    
    
    r_low = int(g_out.mean - stddev_multiplier * g_out.stddev)
    r_high = int(g_out.mean + stddev_multiplier * g_out.stddev)
    
    if plot_results:
        fig, ax = plt.subplots(1,2, facecolor="white")
        fig.set_figheight(5)
        fig.set_figwidth(11)
        
        ax[0].plot(slit_prof, lw=3, color="black")
        ax[0].axvline(slit[0], color="black", ls="dashed")
        ax[0].axvline(slit[1], color="black", ls="dashed")
        ax[0].fill_between([r_low, r_high],
                        [-200, -200], [200,200], color="Red", alpha=0.3)
        ax[0].set_ylim(-2, 1)

        ax[1].plot(x_region, prof_region, lw=3, color="black", label="Smoothed Slit Prof")
        ax[1].plot(x_region, gauss(x_region), label="Gaussian Fit")
        ax[1].fill_between([r_low, r_high],
                        [-200, -200], [200,200], color="Red", alpha=0.3, label="Fit region")
        ax[1].set_ylim(0, 1)
        ax[1].legend(loc="upper left")
        
        ax[0].set_ylabel("Normalized Flux")
        ax[0].set_xlabel("y [pix]")
        ax[1].set_xlabel("y [pix]")
        
        if plot_fn is None:
            plt.show()
        else:
            plt.savefig(plot_fn)

    return [int(g_out.mean - 1.5 * g_out.stddev * stddev_multiplier), int(g_out.mean + g_out.stddev * stddev_multiplier)], g_out

