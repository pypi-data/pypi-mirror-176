import numpy as np
import os
from pathlib import Path

from astropy.io import fits
from astropy.table import Table

from tqdm import tqdm

import time
import pickle

import warnings
warnings.filterwarnings("ignore")

import broadreduce

from scipy.ndimage.filters import gaussian_filter

class DMTPipeError(Exception):
    pass


class BroadReduce():
    def __init__(self, datafile, params=None):
        default_params = {"VERBOSE": True, 
                          "DETECTOR": 0,
                          "TEMP_DIR": "test_dir_1/",
                          "PLOTTING_DIR": "pngs/",
                          "SOLAR_SPEC_FN": "../bass2000spec.ascii", 
                          "SMOOTHING": 30,
                          "PROCESS_RAW": True, 
                          "CLEAN_COSMIC_RAYS": True,
                          "MAKE_MASTERS": True,
                          "PREBIN_FRAMES": True,
                          "FIND_SLITS": True,
                          "GEN_YDIST": True,
                          "GEN_SKYMODEL": True,
                          "WAVELENGTH_SOLN": True,
                          "SUBTRACT_SKY": True,
                          "RECTIFY_FRAMES": True,
                          "SUBTRACT_POLY": True,
                          "COLLAPSE_1D": True,
                          "DELETE_TEMPFILES": True,

                          "SKY_MOD_SMOOTHING": 5,
                          
                          "INSTR": "LRISBLUE",
                          "CHIPFLIP": False,
                          "X_OVERSCAN": [1092, 1150],
                          "X_GOOD": [0, 4500],
                          "GAPSIZE": 100,
                          "MILL2DET": (10.26, 3990),
                          "DX_PIXELS": 5.74,
                          "X_GUESSES": [125, 212, 300, 415, 540, 1680, 1750],
                          "WAVELENGTHS": [3256, 3302.75, 3345.57, 3403.652, 3467.0, 4046.563, 4077.831],
                          
                          "PREBINNING": 1,
                          "FINAL_BINNING": [10, 5],

                          "DSUB": 1,
                          "SAMPLING": 1,
                          "INTERPTYPE": "linear"}
        
        self.datafile = datafile
        self.params = default_params
        
        self.metadata = {"IMAGES": [], "TARGNAMES": [], "RAS": [], "DECS": [], "HEADERS": []}
        
        # Populate the default parameters with user-adjusted parameters
        if params is not None:
            for n in params:
                self.params[n] = params[n]
                
        # These will be generated from the datafile
        self.science_files = []
        self.arc_files = []
        self.flat_files = []
        self.temp_science_files = []
        
        self.masterflat_fn = "flat_master"
        self.masterarc_fn = "arc_master"

        # Containers for the slits (this needs to be improved but for now it's acceptable)
        self.flat_slits = None
        self.flat_slitprofiles = None
        
        # These are all the results of the corrections
        self.ydist = None
        self.sky_models = []
        self.skysub_frames = []
        self.rectified_frames = []
        self.polysubbed_frames = []
        self.final_frames = []
        self.regions = []
        self.gauss_models = []

        # These are the containers for the wavelength solutions
        self.naive_soln = None
        self.tweaked_solns = []
    
    # Pipeline methods ###########################################################################

    def data_info(self):
        """Generate a simple printout of all the files
        """
        self.science_files, self.arc_files, self.flat_files = broadreduce.gen_front_matter(self.datafile, params=self.params, 
                                                                        verbose=self.params["VERBOSE"])

        frametypes = ["science", "arcs", "flats"]
        for i, filelist in enumerate([self.science_files, self.arc_files, self.flat_files]):
            for f in filelist:
                with fits.open(f) as HDUList:
                    print("Frame Type:", frametypes[i])
                    HDUList.info()
                    print()


    def process_raw(self):
        """
            Process all raw files in the directory.
        """
        for i in range(len(self.science_files)):
            outim = "sci_raw_" + str(i)
            broadreduce.rawprocess(self.params["TEMP_DIR"], self.science_files[i], outim, self.params)
        for i in range(len(self.arc_files)):
            outim = "arc_raw_" + str(i)
            broadreduce.rawprocess(self.params["TEMP_DIR"], self.arc_files[i], outim, self.params)
        for i in range(len(self.flat_files)):
            outim = "flat_raw_" + str(i)
            broadreduce.rawprocess(self.params["TEMP_DIR"], self.flat_files[i], outim, self.params)
    
    
    def remove_cosmic_rays(self):
        """ Remove cosmic rays from all science frames """
        files = os.listdir(self.params["TEMP_DIR"])
        for f in tqdm(files, desc="Cleaning files."):
            if not f.startswith("sci"):
                continue
            imin = self.params["TEMP_DIR"] + f
            broadreduce.identify_cosmic_rays(imin, imout=imin, plot_results=False, verbose=False,
                                        plotting_dir=self.params["PLOTTING_DIR"])
    
    
    def make_masters(self):
        """ Generate (and then clean) the master frames for science images """
        if self.params["VERBOSE"]:
            print("---- Generating and cleaning master flat and arc frames")
        broadreduce.generate_master(self.params["TEMP_DIR"], "flat_raw*", "flat_master", show_spectra=False)
        broadreduce.identify_cosmic_rays(self.params["TEMP_DIR"] + "flat_master", plot_results=True, verbose=True,
                                    plotting_dir=self.params["PLOTTING_DIR"])

        broadreduce.generate_master(self.params["TEMP_DIR"], "arc_raw*", "arc_master", show_spectra=False)
        broadreduce.identify_cosmic_rays(self.params["TEMP_DIR"] + "arc_master", plot_results=True, verbose=True,
                                    plotting_dir=self.params["PLOTTING_DIR"])
    
    
    def prebin_frames(self, axis=0, ):
        """ Bin all available frames, so the masters and all science frames. """
        if self.params["VERBOSE"]:
            print("---- Binning frames in wavelength direction by", self.params["PREBINNING"])

        # Bin science files
        for file in broadreduce.obtain_files(self.params["TEMP_DIR"] + "sci_raw_*"):
            broadreduce.bin_array(file, self.params["TEMP_DIR"] + "binned_" + file.split("/")[-1], bin_width=self.params["PREBINNING"], 
                                  axis=0, plot_results=False)
        # Bin master arcs and master flats
        broadreduce.bin_array(self.params["TEMP_DIR"] + "arc_master", self.params["TEMP_DIR"] + "binned_arc_master", 
                              bin_width=self.params["PREBINNING"], axis=0, plot_results=False)
        broadreduce.bin_array(self.params["TEMP_DIR"] + "flat_master", self.params["TEMP_DIR"] + "binned_flat_master",
                              bin_width=self.params["PREBINNING"], axis=0, plot_results=False)

    
    def get_slit_edges(self):
        """ Obtain slit edges (both inner and outer) in both integer form and in poly1D objects. """
        if self.params["VERBOSE"]:
            time.sleep(0.2)
            print("---- Getting inner and outer slit edges")
            time.sleep(0.2)
        
        slit_edges_flat, edge_profiles_flat = broadreduce.find_slit_edges(self.params["TEMP_DIR"] + self.masterflat_fn, det=self.params["DETECTOR"],
                                                                      threshold=10, gap=100, plot_results=True, params=self.params)
        inner_edges_flat, inner_profiles_flat = broadreduce.find_inner_edges(self.params["TEMP_DIR"] + self.masterflat_fn, 
                                                                         slit_edges_flat, threshold=10, gap=100, det=self.params["DETECTOR"],
                                                                         plot_results=True, plot_individual=False, params=self.params)
        self.flat_slits = [slit_edges_flat, inner_edges_flat]
        self.flat_slitprofiles = [edge_profiles_flat, inner_profiles_flat]

    
    def generate_distmap(self, imin="flat_master"):
        if self.params["VERBOSE"]:
            time.sleep(0.2)
            print("---- Generating distortion map from the master flat:", imin)
            time.sleep(0.2)
        # Make sure we can actually generate 
        if self.flat_slits is None:
            raise DMTPipeError(message="No slits available to generate distortion map")
        
        self.ydist = broadreduce.calc_ydist(self.params["TEMP_DIR"], imin, 
                                        self.flat_slits[0], self.flat_slitprofiles[0], params=self.params, 
                                        x_width=151, fit_degree=2,
                                        plot_results=True, diagnostic_plots=False, plot_limits=[-2, 2])
    
    
    def generate_skymodels(self, temp_science_files):
        if self.params["VERBOSE"]:
            time.sleep(0.2)
            print("---- Generating sky models for science files")
            time.sleep(0.2)
        for i in range(len(temp_science_files)):
            filename = temp_science_files[i]
            self.sky_models.append(broadreduce.model_sky(self.params["TEMP_DIR"], filename.split("/")[-1], self.ydist,
                                   self.flat_slits[0], self.flat_slitprofiles[0], self.flat_slitprofiles[1], 
                                   params=self.params, padding=10,
                                   plot_results=True, sci_frame_index=i))
    
    def get_naive_wsol(self):
        if self.params["VERBOSE"]:
            time.sleep(0.2)
            print("---- Getting a naive wavelength solution using the sky frames:", self.masterarc_fn)
            time.sleep(0.2)
        # Get central slit of master arc
        
        inner_slits = self.flat_slits[1]
        print(inner_slits)
        centre = int((inner_slits[1] + inner_slits[0]) / 2)
        
        with fits.open(self.params["TEMP_DIR"] + self.masterarc_fn) as HDUList:
            head = HDUList[0].header
            data = HDUList[2].data
            
            data_slice = data[centre - 20 :centre + 20,:]

            # Get, clean, and normalize 1D spectrum
            arc_1D = np.sum(data_slice, axis=0)
            arc_1D = broadreduce.gaussian_filter(arc_1D, sigma=5).astype(float)
            arc_1D = broadreduce.normalize(arc_1D)
    
        spec_x = np.arange(0, len(arc_1D), 1)
        
        wsol_dir = self.params["PLOTTING_DIR"] + "wsols/"
        if not os.path.isdir(wsol_dir):
            os.makedirs(wsol_dir)

        print(len(spec_x), len(arc_1D))

        # Get wavelength solution
        self.naive_soln = broadreduce.wavesolve(spec_x, arc_1D, [self.params["X_GUESSES"], self.params["WAVELENGTHS"]],
                                            params=self.params, plot_slices=False, plot_results=True, plot_dir=wsol_dir)
        if self.params["VERBOSE"]:
            print("  Naive Solution Found. Params: ", self.naive_soln)
        
    
    def get_tweaked_solns(self):
        """ Tweak the solutions for the science frames """
        if self.params["VERBOSE"]:
            time.sleep(0.2)
            print("---- Getting tweaked solutions for the sky frames --------")
            time.sleep(0.2)
        
        # Load in the solar spectrum
        solar_spec = Table.read(self.params["SOLAR_SPEC_FN"], format='ascii')
        solar_x, solar_y = np.array(solar_spec["col1"], dtype=float), np.array(solar_spec["col2"], dtype=float)

        solar_y = broadreduce.gaussian_filter(solar_y, self.params["SMOOTHING"])
        solar_y = broadreduce.normalize(solar_y)

        if self.params["VERBOSE"]:
            print("---- Successfully loaded solar spectrum from", self.params["SOLAR_SPEC_FN"])

        sky_mod_filenames = broadreduce.obtain_files(self.params["TEMP_DIR"] + "skymod_*")
        
        # Prep the plotting directory for wavelength solutions
        wsol_dir = self.params["PLOTTING_DIR"] + "wsols/"
        if not os.path.isdir(wsol_dir):
            os.makedirs(wsol_dir)

        # Go through the sky models and tweak the sky wavelength solutions
        for i in range(0, len(self.science_files)):
            sky_model = self.params["TEMP_DIR"] + "skymod_1D_" + str(i) + ".dat"
            sky_x, sky_y = np.loadtxt(sky_model)
            sky_y = broadreduce.subtract_continuum(sky_x, sky_y)
            sky_y = broadreduce.normalize(sky_y)
            sky_y = gaussian_filter(sky_y, self.params["SKY_MOD_SMOOTHING"])

            try:
                tweak = broadreduce.tweak_sky_polynomial(sky_x, sky_y, solar_x, solar_y, 
                                                     guess_init=np.copy(self.naive_soln),
                                                     plot_fn=wsol_dir + "wsol_" + str(i) + ".png")
                if self.params["VERBOSE"]:
                    print("  Tweaked Params for", sky_model, " | ", tweak)
                self.tweaked_solns.append(tweak)

            except:
                if self.params["VERBOSE"]:
                    print("Failed to get a tweaked solution for", sky_model)
                continue

    def subtract_skyframes(self):
        """ For each combo of science frames and sky models, subtract them all and 
            add them to skysub_frames
        """
        for i, tempfile in enumerate(self.temp_science_files):
            sci_frame = broadreduce.img_from_file(tempfile, index=self.params["DETECTOR"] + 1)
            # Subtract the sky model
            sci_frame_subtracted = sci_frame - self.sky_models[i]
            self.skysub_frames.append(sci_frame_subtracted)
    
    def rectify_frames(self):
        if self.params["VERBOSE"]:
            print("---- Rectifying sky-subtracted frames")
            time.sleep(0.2)

        for frame in self.skysub_frames:
            # Note that rectify requires just the outer slits, not the outer AND inner slits
            rectified = broadreduce.rectify(frame, self.ydist, det=self.params["DETECTOR"], 
                                        slits=self.flat_slits[0], plot_results=True)
            self.rectified_frames.append(rectified)
    
    def subtract_polynomial(self):
        if self.params["VERBOSE"]:
            print("---- Subtracting polynomial across the detector")
            time.sleep(0.2)

        for frame in self.rectified_frames:
            polysubbed = broadreduce.residual_polynomial(frame, slits=self.flat_slits, det=self.params["DETECTOR"], deg=1, padding=15,)
            self.polysubbed_frames.append(polysubbed)

    def gen_2D_spec(self):
        if self.params["VERBOSE"]:
            print("---- Generating fully binned 2D spectra")
            time.sleep(0.2)

        for i, frame in enumerate(self.polysubbed_frames):
            self.final_frames.append(broadreduce.heavy_bin(frame, self.flat_slits[1], detector=self.params["DETECTOR"], padding=10,
                                wavelength_binning=self.params["FINAL_BINNING"][0], 
                                spatial_binning=self.params["FINAL_BINNING"][1], 
                                targname=self.metadata["TARGNAMES"][i],))
                                # outfile=self.params["TEMP_DIR"] + "2D_SPEC_" +str(i) +  ".fits")
    

    def gen_data_products(self):

        outfile = fits.HDUList()

        for i in range(len(self.polysubbed_frames)):
            try:
                outfile.append(fits.ImageHDU(data = self.polysubbed_frames[i], 
                                            header=self.metadata["HEADERS"][i], name=self.metadata["TARGNAMES"][i]))
            except:
                print("Failed to generate data product for:", self.metadata["TARGNAMES"][i], i)
                continue

        outfile.writeto(self.params["TEMP_DIR"] + "DATA_PRODUCTS.fits", overwrite=True)

        self.metadata["WSOLS"] = self.tweaked_solns
        self.metadata["FLAT_SLITS"] = self.flat_slits

        with open(self.params["TEMP_DIR"] + 'params.br', 'wb') as handle:
            pickle.dump(self.params, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.params["TEMP_DIR"] + 'metadata.br', 'wb') as handle:
            pickle.dump(self.metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def print_output_message(self, t_init, t_final):
        print("\n")

        out_message = "---- Congrats! BroadReduce has finished running -----------"
        border = ""
        for n in range(len(out_message)):
            border += "-"
        messages = []
        messages.append("---- Total Time Elapsed: " +  str(np.round(time.time() - t_init, 2)) + " seconds. ")
        messages.append("---- Total Science Frames: " + str(len(self.science_files)) + " ")
        messages.append("---- Files in: " + str(self.params["TEMP_DIR"]) + "  ")
        messages.append("---- Plots in: " + str(self.params["PLOTTING_DIR"]) + "  ")
        for i, message in enumerate(messages):
            for n in range(len(border) - len(message)):
                messages[i] += "-"

        print(border)
        print(out_message)
        for message in messages:
            print(message)
        print(border)

    def delete_tempfiles(self):
        """ Delete all raw files from the tempdir directory"""
        if self.params["VERBOSE"]:
            print("---- Deleting all temporary files from:", self.params["TEMP_DIR"])
        rm_files = []

        files = Path(self.params["TEMP_DIR"]).rglob('*_raw_*')
        for f in files:
            rm_files.append(f)
        
        for f in rm_files:
            os.remove(f)
            
    # MAIN PIPELINE ##############################################################################
    
    def pipe(self):
        """ The default pipeline """
        t_init = time.time()
        # Gather all files, and generate the necessary directories
        self.science_files, self.arc_files, self.flat_files = broadreduce.gen_front_matter(self.datafile, params=self.params, 
                                                                        verbose=self.params["VERBOSE"])
        all_files = np.concatenate([self.science_files, self.arc_files, self.flat_files])
        
        for fn in self.science_files:
            with fits.open(fn) as HDUList:
                head = HDUList[0].header
                self.metadata["IMAGES"].append(fn)
                self.metadata["TARGNAMES"].append(head["TARGNAME"])
                self.metadata["RAS"].append(head["RA"])
                self.metadata["DECS"].append(head["DEC"])
                self.metadata["HEADERS"].append(head)
#         # Interpolate over bad columns for science frames
#         for i in range(len(self.science_files[:])):
#             broadreduce.fitbadcol(self.params["TEMP_DIR"], self.science_files[i], "sci_badcolfixed" + str(i),  "LRISBLUE")
        
        # Process all raw files
        if self.params["PROCESS_RAW"]:
            self.process_raw()
        
        # Remove cosmic rays from science frames
        if self.params["CLEAN_COSMIC_RAYS"]: 
            self.remove_cosmic_rays()
                
        # Combine frames into a single frame
        if self.params["MAKE_MASTERS"]: 
            self.make_masters()
        
        # Bin in the wavelength direction
        if self.params["PREBIN_FRAMES"]:
            self.prebin_frames()
        
        self.masterflat_fn = "binned_flat_master" if self.params["PREBIN_FRAMES"] else "flat_master"
        self.masterarc_fn = "binned_arc_master" if self.params["PREBIN_FRAMES"] else "arc_master"

        # Get slits
        if self.params["FIND_SLITS"]:
            self.get_slit_edges()
        
        # Determine y-distortion
        if self.params["GEN_YDIST"]:
            self.generate_distmap(imin=self.masterflat_fn)      

        # Get the list of binned science files that we are going to process, taking pre-binning into account
        if self.params["PREBIN_FRAMES"]:
            self.temp_science_files = broadreduce.obtain_files(self.params["TEMP_DIR"] + "binned_sci_*")
        else:
            self.temp_science_files = broadreduce.obtain_files(self.params["TEMP_DIR"] + "sci_raw_*")

        # Determine the sky model for our science files
        if self.params["GEN_SKYMODEL"]:
            self.generate_skymodels(self.temp_science_files)
        
        # Get wavelength solutions, first for the initial naive arc frames and then
        # for the individual science frames.
        if self.params["WAVELENGTH_SOLN"]:
            self.get_naive_wsol()
        
            if len(self.sky_models) > 0:
                self.get_tweaked_solns()
                time.sleep(0.2)

        # Subtract sky, get central spectrum, and rectify
        if self.params["SUBTRACT_SKY"]:
            self.subtract_skyframes()

        if self.params["RECTIFY_FRAMES"]:
            self.rectify_frames()

        if self.params["SUBTRACT_POLY"]:
            self.subtract_polynomial()

        if self.params["FINAL_BIN"]:
            self.gen_2D_spec()

        if self.params["DELETE_TEMPFILES"]:
            self.delete_tempfiles()

        self.gen_data_products()
        self.print_output_message(t_init, time.time())
