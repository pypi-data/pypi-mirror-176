from astropy.io import fits
import numpy as np
from astropy.visualization import ZScaleInterval
from scipy.interpolate import interp1d
from tqdm import tqdm
from matplotlib import pyplot as plt

from .utils import *


def model_sky(processing_dir, imin, distmap, slit_edges, slit_profiles, inner_edges, params=None,
              dsub=1, interptype="linear", sampling=1, im_index=1, padding=20, verbose=True,
              plot_results=False, plotting_dir = "pngs/", sci_frame_index=0):
    """
    Models the sky using the Kelson method
    """
    # Set all parameters if available
    if params is not None:
        dsub = params["DSUB"]
        interptype = params["INTERPTYPE"]
        sampling = params["SAMPLING"]
        im_index = params["DETECTOR"]
        plotting_dir = params["PLOTTING_DIR"]

    # Load in image to process
    with fits.open(processing_dir + imin) as HDUList:
        hdr, img = HDUList[im_index + 1].header, HDUList[im_index + 1].data
        targname = HDUList[0].header["TARGNAME"]

    slit_edge = np.copy(slit_edges)
    # trace_eval = slit_profiles[im_index][1]
    # trace_eval = np.poly1d(trace_eval)

    inner_edge = np.copy(inner_edges)
    inner_low, inner_high = np.poly1d(inner_edge[0]), np.poly1d(inner_edge[1])

    # todo once the outer slits are better, we will stop generating at temp slit
    temp_bottom = np.poly1d([inner_edge[0][0], slit_edge[0]])
    temp_top = np.poly1d([inner_edge[0][0], slit_edge[1]])

    # ny is the spatial direction, nx the wavelength direction
    nx, ny = len(img[0]), slit_edge[1] - slit_edge[0] + 1
    # print("nx", nx, "ny", ny)

    x, y = np.arange(0, nx, dtype=np.float), np.arange(0, ny, dtype=np.float)

    # This is the subsampled x array
    xs = np.arange(0, nx, dsub)

    ysamples = int(ny / sampling)
    subarray = np.zeros((ysamples, len(xs)))
    line = np.arange(0, nx, dtype=np.float)

    masked_img = np.zeros(np.copy(img).shape)

    # Generate a masked array
    # I am comfortable working with nan pixels so this shouldn't be an issue
    for i in range(img.shape[1]):
        strip = np.copy(img[:, i])
        strip[0:int(temp_bottom(i)) + 20] = np.nan
        strip[int(temp_top(i) - 20):] = np.nan
        strip[int(inner_low(i)) - padding:int(inner_high(i)) + padding] = np.nan

        masked_img[:, i] = strip
    #     quickplot_spectra(img)
    # quickplot_spectra(masked_img)

    # Now go through xs
    line = np.arange(0, nx, dtype=np.float)

    forbidden_regions = []
    bottom = temp_bottom(xs)
    forbidden_regions.append((0, padding))
    forbidden_regions.append((int(np.min(inner_low(xs) - bottom) - padding),
                              int(np.min(inner_high(xs) - bottom) + padding)))
    forbidden_regions.append((ny - padding, ny))

    for i in tqdm(range(ysamples), desc="Filling subarray with sky samples"):
        y_i = i * sampling

        # Check and make sure that we can use this line by checking forbidden regions
        try:
            for n in forbidden_regions:
                if n[0] < y_i < n[1]:
                    raise IndexError
        except IndexError:
            subarray[i, :] = np.nan
            continue

        for j in range(nx):
            bottom = temp_bottom(j)

            try:
                line[j] = img[np.int(y_i + bottom) , j]
            except:
                continue
        # Find the new x-coord for this line
        try:
            x_thisline = x + distmap[int(y_i), :]
        except IndexError:
            # print("Issue with index:", y_i)
            continue
        # Now do a spline fit for the line
        spline = interp1d(x_thisline, line, kind=interptype, bounds_error=False, fill_value=0.)
        subarray[i, :] = spline(xs)

    # Now that we have a full subarray, we interpolate over and deproject
    ys = np.arange(0, subarray.shape[0], 1)

    skymodel_1D = np.nanmedian(subarray, axis=0)
    np.savetxt(params["TEMP_DIR"] + "skymod_1D_" + str(sci_frame_index) + ".dat", [xs, skymodel_1D])
    skymodel_1D_interp = interp1d(xs, skymodel_1D, bounds_error=False, fill_value=0)

    # Now deproject back onto the original grid using the collapsed skymodel
    skymodel = np.copy(img) * 0
    for i in tqdm(range(ny), desc="Deprojecting onto original grid"):
        try:
            x_thisline = x + distmap[i, :]
        except IndexError:
            # print("Index issue")
            continue
        model_thisline = skymodel_1D_interp(x_thisline)
        for j in range(len(x)):
            skymodel[int(i + temp_bottom(j)), j] = model_thisline[j]

    if plot_results:
        check_and_make_dirs(["pngs/"])

        fig, ax = plt.subplots(1 ,3, facecolor="white")
        fig.set_figwidth(12)
        fig.set_figheight(4)

        zscale = ZScaleInterval(contrast=0.5)
        scale = zscale.get_limits(img)

        ax[0].imshow(img, vmin=scale[0], vmax=scale[1])
        ax[1].imshow(skymodel, vmin=scale[0], vmax=scale[1])
        ax[2].imshow(img - skymodel, vmin=scale[0], vmax=scale[1])

        plt.suptitle(imin + " -- " + targname)

        for n in range(len(ax)):
            ax[n].set_xticks([])
            ax[n].set_yticks([])

        plt.tight_layout()
        plt.savefig(plotting_dir + "skymodel" + str(sci_frame_index) + ".png", dpi=150)
    return skymodel


def residual_polynomial(frame, slits, deg=3, det=1, padding=15):
    """
        Subtract a polynomial from across the frame 
    """
    
    # This is the output data frame
    poly_subbed = np.zeros(frame.shape)

    # Obtain region to fit polynomial
    outer_slits, inner_slits = slits
    
    region_1 = [outer_slits[0] + padding, inner_slits[0] - padding]
    region_2 = [inner_slits[1] + padding, outer_slits[1] - padding]
    
    # Fullrange spans the whole detection. Valid is just the outer slits without a trace
    fullrange = np.arange(outer_slits[0], outer_slits[1], 1)
    valid = np.concatenate((np.arange(region_1[0], region_1[1], 1), np.arange(region_2[0], region_2[1], 1)))
    
    # Iterate through slices and get polynomials
    for x in tqdm(range(frame.shape[1]), desc="Fitting polynomials"):
        y_slice = np.copy(frame[:, x])
        
        # Fit polynomial only to the valid regions for residual fitting.
        y_slice_tofit = y_slice[valid]
        poly_coeffs = np.polyfit(valid, y_slice_tofit, deg=deg)
        poly = np.poly1d(poly_coeffs)
        
        # Subtract from the FULL y-range the polynomial.
        y_slice_subbed = np.copy(y_slice)
        y_slice_subbed[outer_slits[0]:outer_slits[1]] -= poly(fullrange)
        
        poly_subbed[:, x] = y_slice_subbed
    
    return poly_subbed

