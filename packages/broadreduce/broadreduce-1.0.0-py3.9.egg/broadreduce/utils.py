import os
from statistics import mode
import broadreduce

import numpy as np
from astropy.io import fits
import pathlib as path
from numpy import arange, outer, poly1d, nansum, nanmax
from scipy.signal import savgol_filter
from scipy.ndimage.filters import gaussian_filter

from astropy.visualization import ZScaleInterval
from astropy.modeling import models, fitting
from matplotlib import pyplot as plt

import pickle


def img_from_file(filename, index=0):
    with fits.open(filename) as HDUList:
        data = HDUList[index].data
    return data


def quickplot_spectra(data, contrast=1, make_figure=True, show=True, slits=None, outfile=None, colorbar=False):
    """ Quickly plot an easily viewable spectra for debugging and testing purposes. """
    zscale = ZScaleInterval(contrast=contrast)
    scale = zscale.get_limits(data)
    if make_figure:
        fig = plt.figure(facecolor="white")
    plt.imshow(data, vmin=scale[0], vmax=scale[1], cmap="Greys_r")
    if colorbar:
        plt.colorbar()
    plt.tight_layout()

    if slits is not None:
        xs = arange(0, data.shape[1], 1)
        print(len(xs))
        for slitgroup in slits:
            for slit in slitgroup:
                polyslit = poly1d(slit)
                plt.plot(xs, polyslit(xs))
    if outfile is not None:
        plt.savefig(outfile, dpi=200)
    elif show:
        plt.show()


def slit_profile(img, padding=10, norm=True, plot_profile=False, ylim=None):
    slit_prof = np.nansum(img, axis=1)
    xs = np.arange(padding, len(slit_prof) - (padding), 1)
    slit_prof = slit_prof[padding: -padding]
    if norm:
        slit_prof /= np.nanmax(slit_prof)
    
    if plot_profile:
        plt.figure()
        plt.plot(xs, slit_prof / np.nanmax(slit_prof), color="black", lw=2)

        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])

        plt.xlabel("Position [pix]", fontsize=15)
        plt.ylabel("Normalized Flux Sum", fontsize=15)
        plt.tight_layout()
        plt.show()

    return slit_prof


def spectra_lims(data, contrast):
    zscale = ZScaleInterval(contrast=contrast)
    scale = zscale.get_limits(data)

    return scale


def get_line_val(linregress_obj, x):
    return linregress_obj.slope * x + linregress_obj.intercept


def get_polyfit_line(polyfit_obj, x):
    # Assumes a 1 degree polynomial
    return polyfit_obj[1] + (x * polyfit_obj[0])


def check_and_make_dirs(directories):
    """ Make directories (one or multiple) """
    if type(directories) == str:
        directories = [directories]

    for directory in directories:
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)


def obtain_files(instring):
    """ Gather a list of files for processing. """
    p = path.Path(instring).expanduser()
    parts = p.parts[p.is_absolute():]
    generator = path.Path(p.root).glob(str(path.Path(*parts)))
    files = [str(n) for n in generator]
    return files


def smooth(spectrum, window_length, polyorder=2):
    return savgol_filter(spectrum, window_length=window_length, polyorder=polyorder)


def fit_1d(line, a, b):
    return (line - a) + b


def normalize(arr):
    arr_out = np.copy(arr)
    arr_out -= np.nanmin(arr_out)
    arr_out /= np.nanmax(arr_out)
    return arr_out


def display_all_images(objfile, outdir=None, det=1, transpose=True, colorbar=False):
    images = np.genfromtxt(objfile, dtype='str', comments="#")
    
    if outdir is not None:
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
    
    for img in images:
        img, img_type = img
        with fits.open(img) as HDUList:
            data = HDUList[det].data
            if transpose:
                data = np.transpose(data)
            
            zscale = ZScaleInterval(contrast=0.5)
            scale = zscale.get_limits(data)
            fig = plt.figure(facecolor="white")
            fig.set_figheight(3)
            fig.set_figwidth(10)
            plt.imshow(data, vmin=scale[0], vmax=scale[1], cmap="Greys_r")
            
            plt.text(10, 50, img + "    " + str(img_type), color="white", backgroundcolor="black")
            
            if colorbar:
                plt.colorbar()
            plt.tight_layout()
            
            if outdir is None:
                plt.show()
            else:
                plt.savefig(outdir + img.split("/")[-1] + ".png", dpi=150)


def save_params(out_dict, filename="params.pickle"):
    with open(filename, 'wb') as handle:
        pickle.dump(out_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_params(filename):
    with open(filename, 'rb') as handle:
        out_dict = pickle.load(handle)
    return(out_dict)


class DMTPipeError(Exception):
    def __init__(self, message="General DMTPipe Error"):
        self.message = message
        super().__init__("Error with DMTPipe: " + self.message)


def create_diagnostic_plots(br, transpose=True):
    science_files, arc_files, flat_files = broadreduce.gen_front_matter(br.datafile, params=br.params, 
                                                                        verbose=False)
    
    frametypes = ["science", "arcs", "flats"]

    outdir = br.params["PLOTTING_DIR"] + "diagnostics/"
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    
    for index, fileset in enumerate([science_files, arc_files, flat_files]):
        for f in fileset:
            with fits.open(f) as HDUList:
                fig, ax = plt.subplots(4,1, figsize=(6, 10), facecolor="white")


                for i in range(1, len(HDUList)):
                    data = HDUList[i].data
                    if transpose:
                        data = np.transpose(data)
                        
                    zscale = ZScaleInterval(contrast=0.7)
                    lims = zscale.get_limits(data)
                    
                    slitprof = np.nansum(data, axis=1).astype(float)
                    slitprof = broadreduce.normalize(slitprof[20:-20])
                    slitprof = broadreduce.gaussian_filter(slitprof, 3)
                    ys = np.arange(20, len(slitprof) + 20)
                    
                    ax[i-1].imshow(data, vmin=lims[0], vmax=lims[1], cmap="Greys")
                    ax[i-1].plot(slitprof * 300, ys, color="red")
                    
                    xlim, ylim = ax[i-1].get_xlim(), ax[i-1].get_ylim()
                    
                    # print("Detector: " + str(i))
                    ax[i-1].text(xlim[1] * 0.90, ylim[1] + 100, "Det: " + str(i), fontsize=10, color="red")
                    
                plt.suptitle(f.split("/")[-1] + "  " + HDUList[0].header["TARGNAME"] + " \n" + frametypes[index])

                plt.tight_layout()
                plt.savefig(outdir + f.split("/")[-1].split(".")[0] + ".png", dpi=100)
