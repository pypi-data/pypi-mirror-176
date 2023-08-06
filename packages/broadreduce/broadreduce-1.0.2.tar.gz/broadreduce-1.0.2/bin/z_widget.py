import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from yaml import load

import broadreduce
import numpy as np

from astropy.io import fits
from astropy.table import Table
from astropy.modeling.models import custom_model
from astropy.modeling import models, fitting

from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter
from scipy.stats import chisquare
from scipy.ndimage import gaussian_filter1d

import pickle
import argparse


# LOAD IN ALL INFORMATION FROM USER ARGUMENTS #######################################################

parser = argparse.ArgumentParser(description="Widget to find redshifts from the Ca H+K lines")

parser.add_argument("BROUTPUT", type=str, help="BroadReduce FITS Output File.")
parser.add_argument("PARAMS", type=str, help="BroadReduce FITS Output File.")
parser.add_argument("METADATA", type=str, help="BroadReduce FITS Output File.")

args = parser.parse_args()
args_dict = args.__dict__

in_filename = args_dict["BROUTPUT"]

polysubbed_frames, headers = [], []


with open(args_dict["PARAMS"], 'rb') as handle:
    params = pickle.load(handle)
with open(args_dict["METADATA"], 'rb') as handle:
    metadata = pickle.load(handle) 
flat_slits = metadata["FLAT_SLITS"]

with fits.open(in_filename) as HDUList:
    for hdu in HDUList[1:]:
        headers.append(hdu.header)
        polysubbed_frames.append(hdu.data)

# Load in the Ca H+K Template
caHK_template = Table.read("tem_alpha.dat", format="ascii")
template_x, template_y = caHK_template["l"], caHK_template["y_final"]
template_y = broadreduce.gaussian_filter(template_y, 11)
template_y /= np.max(template_y)


def load_spec(index):
    global deltas_interp
    binned_xs, spec_1D, = broadreduce.collapse_1D(polysubbed_frames[index], 
                                                        flat_slits[1], 
                                                        params=params, det=params["DETECTOR"])[:2]
    xs = np.poly1d(metadata["WSOLS"][index])(binned_xs)
    deltas = xs[1:] - xs[:-1]
    deltas_interp = interp1d(xs[1:], deltas)

    return xs, spec_1D


# GENERATE PLOT WIDGET  ######################################################################

working_index, z_coarse, z_fine = 0, 0., 0.
coma_z = 0.0231
global deltas_interp


fig, ax = plt.subplots(figsize=(12, 4)) #, label="Redshift Widget")

binned_xs, spec_1D = load_spec(0)

# global spec
spec_line = ax.plot(binned_xs, spec_1D / np.max(spec_1D), color="grey")
template_line = ax.plot(template_x, template_y, color="red", alpha=0.2)

ax.set_xlabel("Wavelength [Angstrom]")
ax.set_ylabel("Normalized Flux")
ax.set_ylim(-0.5, 1)
ax.set_xlim(3600, 4250)

intrinsic_1 = ax.axvline(3969, color="black", alpha=0.1, label="Intrinsic Ca H+K")
intrinsic_2 = ax.axvline(3934, color="black", alpha=0.1)

ax.axvline(3969 * 1.03, color="red", alpha=0.1, label="Ca H+K (At Coma)")
ax.axvline(3934 * 1.03, color="red", alpha=0.1)

line1 = ax.axvline(3969 * 1.0231, color="red", ls="dashed", alpha=1)
line2 = ax.axvline(3934 * 1.0231, color="red", ls="dashed", alpha=1)

text1 = ax.text(ax.get_xlim()[0] + 40, ax.get_ylim()[1] * 1.10, "n/a")
text2 = ax.text(ax.get_xlim()[0] + 40, ax.get_ylim()[1] * 1.02, "n/a")

text3 = ax.text(ax.get_xlim()[0] + 200, ax.get_ylim()[1] * 1.10, "n/a")
text4 = ax.text(ax.get_xlim()[0] + 200, ax.get_ylim()[1] * 1.02, "n/a")



# ADD INTERACTIVE WIDGETS ######################################################################

z_coarse_ax = fig.add_axes([0.90, 0.25, 0.0225, 0.63])
z_coarse_slider = Slider(
    ax=z_coarse_ax, label='Z (Coarse)', valmin=-0.1, valmax=0.1, valinit=z_coarse, orientation="vertical")

z_fine_ax = fig.add_axes([0.96, 0.25, 0.0225, 0.63])
z_fine_slider = Slider(ax=z_fine_ax, label='Z (fine)', valmin=-0.005, valmax=0.005, valinit=z_coarse, orientation="vertical")

index_ax = fig.add_axes([0.7, 0.025, 0.25, 0.04])
index_slider = Slider(ax=index_ax, label="Working Index", valmin=0, valmax=len(polysubbed_frames), valstep=1)

binning_ax = fig.add_axes([0.1, 0.025, 0.05, 0.04])
binning_box = TextBox(ax=binning_ax, label="Binning", initial=params["FINAL_BINNING"][0]) #, textalignment='center')

binning_button_ax = fig.add_axes([0.17, 0.025, 0.05, 0.04])
binning_button = Button(ax=binning_button_ax, label="Binning")

titletext = ax.text(ax.get_xlim()[0] + 40, ax.get_ylim()[1] * 0.9, metadata["TARGNAMES"][0], 
        bbox=dict(facecolor='white', edgecolor='red'))

template_y_ax = fig.add_axes([0.3, 0.025, 0.15, 0.025])
template_y_slider = Slider(ax=template_y_ax, label='Template Y', valmin=-0.2, valmax=0.2, valinit=0)


# This method updates the spectra, called on object changes and binning changes
def update_spectra(val):
    global deltas_interp
    try:
        binned_xs, spec_1D, spec_2D = broadreduce.collapse_1D(polysubbed_frames[index_slider.val], 
                                                            flat_slits[1], 
                                                            params=params, det=params["DETECTOR"],
                                                            wavelength_binning=int(binning_box.text))
        wsol = metadata["WSOLS"][index_slider.val]
        print(wsol)
        xs = np.poly1d(wsol)(binned_xs)
        deltas = xs[1:] - xs[:-1]
        deltas_interp = interp1d(xs[1:], deltas, bounds_error=False, fill_value="extrapolate")

    except (IndexError, ValueError):
        return

    try:
        spec_line[0].set(xdata=xs, ydata=spec_1D/np.max(spec_1D))
        titletext.set_text(metadata["TARGNAMES"][index_slider.val])
    except UnboundLocalError:
        pass

    fig.canvas.draw_idle()


# This method updates the Ca H+K lines
def update_lines(val):
    global deltas_interp

    z_tot= z_coarse_slider.val + z_fine_slider.val
    
    line1_val, line2_val = 3969 * (1 + z_tot), 3934 * (1 + z_tot)
    delta_lambda = deltas_interp(line2_val)
    delta_z = delta_lambda / 3934
    delta_v = 299792 * delta_lambda / 3934

    line1.set(xdata=(line1_val))
    line2.set(xdata=(line2_val))

    template_line[0].set(xdata=template_x * (1 + z_tot), ydata=template_y + template_y_slider.val)

    text1.set_text("z = " + str(np.round(z_tot, 4)) + r' $\pm$ ' + str(np.round(delta_z, 3)) )
    text2.set_text("z (rel Coma) = " + str(np.round(z_tot - coma_z, 4)) + r' $\pm$ ' + str(np.round(delta_z, 3)) )
    
    text3.set_text("v = " + str(np.round(z_tot * 299792, 3)) + r' $\pm$ ' + str(np.round(delta_v, 3)) + " km/s")
    text4.set_text("v (rel Coma) = " + str(np.round((z_tot - coma_z) * 299792, 3)) + r' $\pm$ ' +\
                str(np.round(delta_v, 3)) + " km/s")

    # text5.set_text(r'$\Delta z = $' + str(np.round(delta_lambda, 3)) + " angstrom")
    # text6.set_text(r'$\Delta z = $' + str(np.round(delta_v, 3)) + "km/s")


z_coarse_slider.on_changed(update_lines)
z_fine_slider.on_changed(update_lines)
template_y_slider.on_changed(update_lines)
index_slider.on_changed(update_spectra)
binning_box.on_submit(update_spectra)
binning_button.on_clicked(update_spectra)

# plt.tight_layout()
ax.legend(loc="lower left")
plt.subplots_adjust(left=0.10, bottom=0.2)
plt.show()

