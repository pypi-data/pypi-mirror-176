import wave
import numpy as np
from astropy.io import fits

from .utils import *
from scipy.ndimage.filters import gaussian_filter


def bin_individual(data, bin_width, axis=0, method=np.sum, transpose=True):
    newshape_x = int((data.shape[axis]) / bin_width)

    # Create new container array
    new_arr = np.zeros((newshape_x, data.shape[not bool(axis)]))

    # Go through our slices, sum things along the y axis, and add them to the new array
    for j in range(new_arr.shape[axis]):
        new_arr[j] = method(data[bin_width * j: bin_width *j + bin_width], axis=axis)

    # Re-transpose at the end
    if transpose:
        new_arr = np.transpose(new_arr)

    return new_arr


def bin_array(imin, imout, bin_width=2, method=np.sum, axis=0, plot_results=False, plotting_dir="pngs/"):
    """
        Bin all frames along the wavelength direction.
        This assumes that the data was transposed earlier in rawprocess, so it will
        retranspose it.

        filename: input filename
        bin_width: the width of the bin to rebin into
        method: which method to use in rebinning, default is numpy.sum
        axis: the axis
    """

    with fits.open(imin) as HDUList:

        for i in range(1, len(HDUList)):
            # At this point the data will need to be transposed back and retransposed at the end
            data = np.transpose(HDUList[i].data)

            new_arr = bin_individual(data, bin_width, axis=axis, method=method)
            HDUList[i].data = new_arr

            if plot_results:
                check_and_make_dirs([plotting_dir + "binning/"])
                quickplot_spectra(np.transpose(data),
                                  outfile=plotting_dir + "binning/" + imin.split("/")[-1].split(".")[0] + str
                                  (i) + "_unbinned.png")
                quickplot_spectra(new_arr,
                                  outfile=plotting_dir + "binning/" + imin.split("/")[-1].split(".")[0] + str
                                  (i) + "_binned.png")
        HDUList.writeto(imout, overwrite=True)



def heavy_bin(frame, inner_slits=None, region=None, detector=1, wavelength_binning=10, 
              spatial_binning=5, padding=15, outfile=None, targname="", method=np.sum):
    if region is None:
        frame_slice = frame[inner_slits[0] + padding:inner_slits[1] - padding, :]
    else:
        frame_slice = frame[region[0] + padding: region[1] - padding, :]
    
    
    binned = bin_individual(frame_slice, bin_width=spatial_binning, transpose=False, method=method)
    binned = bin_individual(np.transpose(binned), bin_width=wavelength_binning, transpose=True, method=method)
    
    spec_1D = np.sum(binned, axis=0) 
    spec_1D = gaussian_filter(spec_1D, 1)
    
    if outfile is not None:
        out = fits.HDUList()
        out.append(fits.ImageHDU(data=binned))
        out[0].header["TARGNAME"] = targname
        out.writeto(outfile, overwrite=True)
        
    return binned
