import numpy as np
from astropy.io import fits
from astropy.modeling import models, fitting
from astropy.stats import sigma_clip
from tqdm import tqdm
from .utils import *
from matplotlib import pyplot as plt


def find_slit_edges(master_flat_name, edge_cut=50, threshold=20, gap=20, det=1, plot_results=False, params=None):
    """
        Obtain the slit edges for each detector using a simple thresholding method.

        edge_cut: how much to trim off the edges to avoid pesky edge spikes (should be between the edge of the
            image and the edge of the slit)
        threshold: value that the slit must rise over in order to be deemed a positive hit
        plot_results: save a bunch of debugging data to ./pngs/flats/

    """
    det_edges = None
    det_profiles = None
    hw = int(gap / 2)  # Halfwidth of gap

    with fits.open(master_flat_name) as HDUList:
    # Iterate over detectors
        data = HDUList[det].data

        xs, lows, highs = [], [], []

        hw = int(gap / 2)
        # Now take slices along the wavelength path, get a slit profile, and find the slit edges at each slice
        for j in range(hw, len(data[0]) - gap, gap):
            data_slice = data[:, j - hw:j + hw]

            slit_profile = np.median(data_slice, axis=1)[edge_cut:-edge_cut]
            good = np.argwhere(slit_profile[edge_cut:-edge_cut] > threshold)
            if len(good) > 0:
                low, high = good[0] + 2 * edge_cut, good[-1] + 2 * edge_cut
            else:
                low, high = 0, data.shape[0]

            xs.append(j)
            lows.append(int(low))
            highs.append(int(high))

        xs, lows, highs = np.array(xs), np.array(lows), np.array(highs)

        # Use the median for a simple judge of the slit edge
        det_edges = (int(np.median(lows)), int(np.median(highs)))

        # Sigma clip the gathered values, mask, and take a simple linear regression
        lows_sc = sigma_clip(lows, masked=True)
        xs_low = xs[~lows_sc.mask]
        lows = lows[~lows_sc.mask]
        # low_line = linregress(xs_low, lows)
        low_line = np.polyfit(xs_low, lows, deg=1)

        highs_sc = sigma_clip(highs, masked=True)
        xs_high = xs[~highs_sc.mask]
        highs = highs[~highs_sc.mask]
        # high_line = linregress(xs_high, highs)
        high_line = np.polyfit(xs_high, highs, deg=1)

        det_profiles = low_line, high_line

        if plot_results:
            if params is None:
                outdir = "pngs/slits/"
            else:
                outdir = params["PLOTTING_DIR"] + "slits/"

            if not os.path.isdir(outdir):
                os.makedirs(outdir)

            fig = plt.figure(figsize=(10, 6), facecolor="white")
            quickplot_spectra(data, show=False, make_figure=False)
            plt.axhline(low, color="red", ls="dotted")
            plt.axhline(high, color="red", ls="dotted")

            xs = np.arange(0, data.shape[1])
            plt.plot(xs, get_polyfit_line(low_line, xs), color="red")
            plt.plot(xs, get_polyfit_line(high_line, xs), color="red")

            plt.tight_layout()
            plt.savefig(outdir + "flatslit_" + str(det) + ".png", dpi=200)

    return det_edges, det_profiles


def find_inner_edges(master_flat_name, edges, threshold=20, gap=20, det=1, plot_results=False, plot_individual=False, params=None):
    """
        Find the inner edges for a frame.
    """
    inner_edges, inner_profiles = None, None
    hw = int(gap / 2)

    gaussian_width = 15
    limit_trim = 50

    with fits.open(master_flat_name) as HDUList:

        data_full = HDUList[det].data

        if data_full is None:
            print("No image at detector", det)
            return None

        this_edge = np.copy(edges)

        # Trim data in y, we have the edge data so we will add this back later
        data = data_full[this_edge[0] + limit_trim:this_edge[1] - limit_trim, :]

        xs, lows, highs = [], [], []
        for j in range(hw, len(data[0]) - gap, gap):

            # Take slice along wavelength path
            data_slice = data[:, j - hw:j + hw]
            hh = (int(data_slice.shape[0] / 2))

            # Since there are three slices, we will divide into halves

            def fit_slice(img_slice):
                # Now get the slice profile, and to better fit a Gaussian, subtract
                # the median and reverse the profile.
                # The guess for x_0 will be halfway along the axis
                slice_profile = np.sum(img_slice, axis=1)
                slice_profile -= np.median(slice_profile)
                slice_profile /= -np.max(np.abs(slice_profile))

                # Smooth the profile with a S-G filter to reduce noise interference
                slice_profile = smooth(slice_profile, 25)
                slice_profile = smooth(slice_profile, 25)

                maxguess = np.argmax(slice_profile)

                # Now do a gaussian fit, taking the argmax as the guess
                # This should capture almost all of it
                gaussian = models.Gaussian1D(amplitude=1, mean=maxguess,
                                                stddev=gaussian_width)
                gaussian.amplitude.min = 0
                fit_gauss = fitting.LevMarLSQFitter()
                g = fit_gauss(gaussian, np.arange(0, len(slice_profile)), slice_profile)

                slit_centre = int(g.mean.value)

                return slit_centre

            slice_upper = data_slice[0:hh]
            slice_lower = data_slice[hh:]

            lower_slice_location = fit_slice(slice_lower) + this_edge[0] + limit_trim + hh
            upper_slice_location = fit_slice(slice_upper) + this_edge[0] + limit_trim

            xs.append(j)
            lows.append(lower_slice_location)
            highs.append(upper_slice_location)


        xs, lows, highs = np.array(xs), np.array(lows), np.array(highs)

        # Use simple median for the edge estimate
        low_guess, high_guess = int(np.median(lows)), int(np.median(highs))
        inner_edges = (high_guess, low_guess)

        # Sigma clip the gathered values, mask, and take a simple linear regression
        lows_sc = sigma_clip(lows, masked=True)
        xs_low = xs[~lows_sc.mask]
        lows = lows[~lows_sc.mask]
        # low_line = linregress(xs_low, lows)
        low_line = np.polyfit(xs_low, lows, deg=1)

        highs_sc = sigma_clip(highs, masked=True)
        xs_high = xs[~highs_sc.mask]
        highs = highs[~highs_sc.mask]
        # high_line = linregress(xs_high, highs)
        high_line = np.polyfit(xs_high, highs, deg=1)

        inner_profiles = (high_line, low_line)

        if plot_results:

            if params is None:
                outdir = "pngs/slits/"
            else:
                outdir = params["PLOTTING_DIR"] + "slits/"

            xs = np.arange(0, data_full.shape[1])
            low_line_obj = np.poly1d(low_line)
            high_line_obj = np.poly1d(high_line)

            plt.figure(figsize=(10, 6), facecolor="white")
            plt.imshow(data_full)

            plt.axhline(this_edge[0], color="white")
            plt.axhline(this_edge[1], color="white")

            plt.plot(xs, low_line_obj(xs), color="red")
            plt.plot(xs, high_line_obj(xs), color="orange")

            # plt.axhline(low_guess, color="red")
            # plt.axhline(high_guess, color="orange")

            plt.savefig(outdir + "inner_flatslit" + str(det) + ".png", dpi=200)

    return inner_edges, inner_profiles


