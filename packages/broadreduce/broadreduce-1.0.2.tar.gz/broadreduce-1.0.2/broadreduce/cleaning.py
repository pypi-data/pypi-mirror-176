import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

from .utils import *


def identify_cosmic_rays(imin, nsigma=10, imout=None, verbose=True, plot_results=True, plotting_dir="pngs/"):
    """
        Use the detectors to remove cosmic rays for each file
        This will automatically overwrite the input image, so use the files made in
            your processing directory.

        imin: input filename
        imout: output filename (if None, will overwrite imin)
        ngisma: the number of sigmas above the median for a pixel to be considered a cosmic ray
        plot_results: print out results to pngs/cleaning/

    """
    if verbose:
        print("  Cleaning", imin)

    with fits.open(imin) as HDUList:
        images = []
        for i in range(1, len(HDUList)):
            data = HDUList[i].data
            images.append(data)
        images = np.asarray(images)
        median_image = np.median(images, axis=0)
        std = sigma_clipped_stats(median_image)[2]

        for i in range(1, len(HDUList)):
            data = HDUList[i].data
            #             print(data.shape)
            mask = (data > median_image + nsigma *std)

            data_masked = np.copy(data)
            data_masked[mask] = np.nan

            # Go through each column, interpolate, and fill nans
            ys = np.arange(0, len(data_masked[:, 0]), 1)
            for j in range(len(data_masked[0])):
                row = data_masked[:, j]
                indices = np.isnan(row)
                indices = np.logical_or(indices, np.roll(indices, -1))
                indices = np.logical_or(indices, np.roll(indices, 1))

                nan_indices = [n[0] for n in np.argwhere(indices)]

                row_ys, row_nonans = ys[~indices], row[~indices]
                try:
                    interp = interp1d(row_ys, row_nonans, bounds_error=False, fill_value=np.nan)
                except ValueError:
                    print("Valuerror", j, "interpolation failed while cleaning cosmic rays.")

                for index in nan_indices:
                    row[index] = float(interp(index))

                data_masked[:, j] = row
            HDUList[i].data = data_masked

            if plot_results:
                check_and_make_dirs(plotting_dir + "cleaning/")
                combined = np.concatenate((data, data_masked), axis=0)
                quickplot_spectra(combined,
                                  outfile=plotting_dir + "cleaning/" + imin.split("/")[-1].split(".")[0] + "_" +
                                          str(i) + "_cleaned.png")

        if imout is None:
            return [HDUList[i].data for i in range(1, len(HDUList))]
            # HDUList.writeto(imin, overwrite=True)
        else:
            HDUList.writeto(imout, overwrite=True)


def generate_master(processing_dir, files, outname, show_spectra=False, plotting_dir="pngs/"):
    """
        Generate a combined master image for a set of exposures.
        Should only be used for arcs and flats (for now, I think), but for now it seems to work really damn good.
            Also takes care of dead pixels!
    """

    files = obtain_files(processing_dir + files)

    outfile = fits.HDUList()
    outfile.append(fits.PrimaryHDU())
    # Generate a master flat image (kind of a bad way to do it but whatever it's not horrific - I think)
    for i in range(1, 5):
        det_flat = []
        for filename in files:
            with fits.open(filename) as HDUList:
                det_flat.append(np.copy(HDUList[i].data))
        this_flat = np.median(det_flat, axis=0)

        outfile.append(fits.ImageHDU(data=this_flat))
    outfile.writeto(processing_dir + outname, overwrite=True)

    if show_spectra:
        check_and_make_dirs([plotting_dir + outname + "/"])
        with fits.open(processing_dir + outname) as HDUList:
            for i in range(1, len(HDUList)):
                quickplot_spectra(HDUList[i].data, show=False)
                plt.tight_layout()
                plt.savefig(plotting_dir + outname + "/det_" + str(i + 1) + ".png", dpi=200)
