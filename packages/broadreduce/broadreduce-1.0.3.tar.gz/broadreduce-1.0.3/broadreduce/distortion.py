import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from matplotlib import pyplot as plt

from scipy.interpolate import interp1d
from tqdm import tqdm
from .utils import *

import broadreduce

def ydist_diagnostic_plot(img_slice, spectrum_centre, x1, x2, xl,
                          ys, ys_good, shifts_good, shifts_interpolated,
                          imin, top, bottom, centre_y, plotting_dir):
    """
        Create a diagnostic plot for the ydist calculation.
        NOTE: This is a purely internal plotting routing and should NEVER
            be used outside of the calc_ydist() method.
    """

    spectrum_top = img_slice[top]
    spectrum_top -= np.nanmedian(spectrum_top)

    spectrum_bottom = img_slice[bottom]
    spectrum_bottom -= np.nanmedian(spectrum_bottom)

    lims = spectra_lims(img_slice, contrast=1)

    check_and_make_dirs([plotting_dir + "ydists/"])

    fig, ax = plt.subplots(1, 3, facecolor="white")

    fig.set_figheight(8)
    fig.set_figwidth(13)
    ax[0].imshow(img_slice, cmap="Greys_r", vmin=lims[0], vmax=lims[1])
    ax[0].set_title("Slice [" + str(x1) + "," + str(x2) + "]")

    ax[1].plot(xl, spectrum_centre, color="black", lw=3, label="centre (template)")
    ax[1].plot(xl, spectrum_top, color="red", lw=1, alpha=0.7, label="top")
    ax[1].plot(xl, spectrum_bottom, color="blue", lw=1, alpha=0.7, label="bottom")
    ax[1].legend()

    ax[1].set_title("1D Line Spectrum")

    ax[2].plot(ys_good, shifts_good)
    ax[2].plot(ys, shifts_interpolated)
    ax[2].axhline(0, color="black")
    ax[2].set_ylim(-3, 3)

    ax[2].set_title("Shifts")
    plt.tight_layout()
    plt.savefig(plotting_dir + "ydists/" + imin.split("/")[-1].split(".")[0] + "_" + str(x1) + "_" + str(x2) + ".png",
                dpi=200)


def calc_ydist(processing_dir, imin, edges, trace_eval,
               params=None, dsub=0.5, im_index=1, fit_degree=2, x_width=251, 
               plot_results=False, diagnostic_plots=False, plot_limits=[-3, 3], plotting_dir="pngs/"):
    """
        Generate a y-distortion map for an input image using cross-correlation.

        processing_dir: the processing directory that input images will be
            pulled from, and images will be saved to.
        imin: The input image (either a filename or a numpy ndarray)
        edges: The outer slit edges (an array)
        trace_eval: The trace evaluation, which is a numpy polyfit object
        params: User parameters if none are provided
        dsub: The stepsize in the finely sampled array
        im_index: The index of the HDUList to get the distortion map for
        x_width: The width of the columns that the array is split into when doing
                cross correlation
        fit_degree: The degree of the polynomial to fit when drawing from
                the finely-sampled array.
    """

    if params is not None:
        dsub = params["DSUB"]
        im_index = params["DETECTOR"]
        plotting_dir = params["PLOTTING_DIR"]
        verbose = params["VERBOSE"]

    slit_edge = np.copy(edges)

    # Get wavelength image
    if type(imin) is not np.ndarray:
        with fits.open(processing_dir + imin) as HDUList:
            hdr = HDUList[im_index + 1].header
            img = HDUList[im_index + 1].data
    else:
        img = imin

    trace_eval = trace_eval[0]  # Just take one of the lines and assume the rest is fine
    trace_eval = np.poly1d(trace_eval)

    # quickplot_spectra(img)

    nx = len(img[0])  # This is the wavelength axis
    ny = slit_edge[1] - slit_edge[0] + 1  # This is the physical axis

    x, y = np.arange(0, nx, dtype=np.float), np.arange(0, ny, dtype=np.float)  # define x and y axes

    line_loc = np.arange(0, nx, x_width)

    nlines = len(line_loc)
    # Create container arrays
    dist_xyval = np.zeros((nlines, ny))
    im_dist = np.zeros((ny, nx))

    dx = 0
    for i in tqdm(range(nlines), desc="Fitting line tilts"):

        # Get the image slice
        img_slice = img[:, line_loc[i]:line_loc[i] + x_width]

        # Get the regions in x
        x1 = line_loc[i]
        x2 = line_loc[i] + len(img_slice[0])

        # Create container arrays
        xl = np.arange(x1, x2, dtype=np.float)
        xls = np.arange(x1, x2, dsub)
        xlc = np.arange(x1, x2, 0.05)

        top = int(trace_eval(line_loc[i])) + 10
        bottom = int(trace_eval(line_loc[i]) + ny) - 10
        centre_y = int(trace_eval(line_loc[i]) + ny / 2)

        # spectrum_centre = np.median(img_slice[centre_y - 2:centre_y + 3], axis=0)
        spectrum_centre = img_slice[centre_y]
        spectrum_centre -= np.nanmedian(spectrum_centre)

        ys = np.arange(top, top + ny, dtype=int)
        shifts = np.arange(0, ny, dtype=np.float)

        # Then for each y value get spectrum and correlate
        for j in range(len(ys[::])):
            try:
                row = ys[j]
            except IndexError:
                print("Index Error on line", j)
                continue
            try:
                this_line = img_slice[row]
                this_line -= np.nanmedian(this_line)
            except IndexError:
                print("Index Error on line", j)
                continue

            cc = np.correlate(spectrum_centre, this_line, "same")
            # do spline fit to get subpixel maximum
            f = interp1d(xl, cc, kind='cubic', bounds_error=False,
                         fill_value=0.)
            ccs = f(xlc)

            max_pos = xlc[np.argmax(ccs)] - (x2 - x1) / 2 - x1
            shifts[j] = max_pos

        # Reject extremely bad values using sigma clipping
        stats = sigma_clipped_stats(shifts)
        good_indices = np.abs(shifts) < 3 * stats[2]
        # print(np.sum(good_indices))

        ys_good, shifts_good = ys[good_indices], shifts[good_indices]

        # Generate a polynomial fit
        shifts_fit = np.poly1d(np.polyfit(ys_good, shifts_good, deg=1))
        shifts_interpolated = shifts_fit(ys)

        dist_xyval[i] = shifts_interpolated

        if plot_results and diagnostic_plots:
            ydist_diagnostic_plot(img_slice, spectrum_centre, x1, x2, xl,
                                  ys, ys_good, shifts_good, shifts_interpolated,
                                  imin, top, bottom, centre_y, plotting_dir)

    # populate ydist image
    ydist_image = np.ndarray((len(ys), img.shape[1]))

    xs = np.arange(0, img.shape[1])
    x_centres = line_loc + (x_width / 2)
    dist_xyval = np.transpose(dist_xyval)

    # Now go through each y value, construct a interp1d object, and populate the final array
    # We will use linear extrapolation for simplicity
    for i in tqdm(range(len(ys)), desc="Interpolating to get final distortion map."):
        y_slice = dist_xyval[i]

        # interp = interp1d(x_centres, y_slice, fill_value="extrapolate", bounds_error=False)
        # todo: instead of interpolation object, we fit with a polynomial

        fit = np.polyfit(x_centres, y_slice, deg=fit_degree)
        fit = np.poly1d(fit)

        ydist_image[i] = fit(xs)

    if plot_results:
        check_and_make_dirs([plotting_dir + "ydists/"])
        plt.figure(figsize=(10, 4), facecolor="white")
        plt.imshow(ydist_image, vmin=plot_limits[0], vmax=plot_limits[1])
        plt.xlabel("Wavelength")
        plt.ylabel("Spatial")
        plt.colorbar()
        plt.savefig(plotting_dir + "ydists/" + imin.split("/")[-1].split(".")[0] + "_dist_xyval.png", dpi=200)

    return ydist_image


def rectify(arr, ydist, slits, det=1, plot_results=False):
    """ Rectify an array according to a y-distortion map

    :param arr: The 2D array to be rectified
    :type arr: arr_like
    :param ydist: The y-distortion map 
    :type ydist: arr_like
    :param slits: The input slits to know which regions to clean up the array
    :type slits: arr_like
    :param det: The detector (to get the right slit), defaults to 1
    :type det: int, optional
    :param plot_results: Plot the rectification results, defaults to False
    :type plot_results: bool, optional
    :return: The rectified array
    :rtype: arr_like
    """
    slits = np.copy(slits)
    # This value "centres" a larger ydist onto the sliced up image
    # This should be acceptable so long as the ydist is of order 1 pixel at extrema
    y_cent = int((ydist.shape[0] - abs(slits[1] - slits[0])) / 2)

    # Set up the x array and iteration parameters
    xs = np.arange(0, arr.shape[1], 1)
    start = slits[0] - y_cent

    rectified = np.copy(arr)

    # Go through and rectify each row
    for i in tqdm(range(start, slits[1]), desc="Applying shifts"):
        # This is the corresponding index for the y-distortion map
        j = i - start

        row = arr[i]
        # Create shifted x values (where the true locations of the values in the row are)
        xs_shift = np.copy(xs) - ydist[j]
        # Generate interpolation object of the shifted row
        interp = interp1d(xs_shift, row, kind="linear",
                          bounds_error=False, fill_value="extrapolate")
        # Sample for the rectified array
        rectified[i] = interp(xs)

    if plot_results:
        broadreduce.quickplot_spectra(ydist, colorbar=True)
        broadreduce.quickplot_spectra(arr)
        broadreduce.quickplot_spectra(rectified)
    return rectified
