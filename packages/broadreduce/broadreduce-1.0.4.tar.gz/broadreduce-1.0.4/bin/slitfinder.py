#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from yaml import load

import sys
import broadreduce
import numpy as np

from astropy.io import fits
from astropy.table import Table
from astropy.modeling.models import custom_model
from astropy.modeling import models, fitting
from astropy.visualization import ZScaleInterval

from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter
from scipy.stats import chisquare
from scipy.ndimage import gaussian_filter1d

import pickle
import argparse


def print_output(val):
    global lines
    global lineprofs
    sorted_indices = np.argsort(lines)

    print([(lines[sorted_indices[0]], lines[sorted_indices[3]]), (lines[sorted_indices[1]], lines[sorted_indices[2]])])
    print([(lineprofs[sorted_indices[0]], lineprofs[sorted_indices[3]]), (lineprofs[sorted_indices[1]], lineprofs[sorted_indices[2]])])

# LOAD IN ALL INFORMATION FROM USER ARGUMENTS #######################################################

parser = argparse.ArgumentParser(description="Widget to find slits from a flat frame")

parser.add_argument("FLATFILE", type=str, help="Flat file image.")
parser.add_argument("--det", type=int, help="Detector.")

args = parser.parse_args()
args_dict = args.__dict__

in_filename = args_dict["FLATFILE"]

if args_dict["det"] is None:
    det = 1
else:
    det = args_dict["det"]

# Load in the data
with fits.open(in_filename) as HDUList:
    data = HDUList[det].data


# GENERATE PLOT WIDGET  ######################################################################

lines, lineprofs = [], []


zscale = ZScaleInterval(contrast=0.5)
lims = zscale.get_limits(data)

fig, ax = plt.subplots(figsize=(12, 4)) #, label="Redshift Widget")
ax.imshow(data, vmin=lims[0], vmax=lims[1], cmap="Greys_r")

xs = np.arange(0, data.shape[1], 10)
line = plt.plot(xs, np.ones(len(xs)) * 100, color="red")

# ADD INTERACTIVE WIDGETS ######################################################################

c_ax = fig.add_axes([0.90, 0.35, 0.0225, 0.63])
c_slider = Slider(ax=c_ax, label='c', valmin=-10, valmax=data.shape[0], valinit=0, orientation="vertical")

m_ax = fig.add_axes([0.96, 0.35, 0.0225, 0.63])
m_slider = Slider(ax=m_ax, label='m)', valmin=-0.05, valmax=0.05, valinit=0, orientation="vertical")

add_line_ax = fig.add_axes([0.86, 0.21, 0.12, 0.05])
add_line_button = Button(ax=add_line_ax, label="Add Line to List")

print_ax = fig.add_axes([0.86, 0.15, 0.12, 0.05])
print_button = Button(ax=print_ax, label="Print Formatted")

reset_ax = fig.add_axes([0.86, 0.09, 0.12, 0.05])
reset_button = Button(ax=reset_ax, label="Reset")

# This method updates the Ca H+K lines
def update_line(val):
    xs = np.arange(0, data.shape[1], 10)
    ys = m_slider.val * xs + c_slider.val

    line[0].set(xdata=xs, ydata=ys)

def add_line(val):
    global lines, lineprofs
    c, m = np.round(c_slider.val, 1), np.round(m_slider.val, 3)
    lines.append(c)
    lineprofs.append([m,c])

    print(lines)
    print(lineprofs)
    print()

def reset(val):
    global lines, lineprofs
    lines = []
    lineprofs = []

    print(lines)
    print(lineprofs)
    print()


c_slider.on_changed(update_line)
m_slider.on_changed(update_line)
add_line_button.on_clicked(add_line)
print_button.on_clicked(print_output)
reset_button.on_clicked(reset)

# plt.tight_layout()
plt.subplots_adjust(left=0.01, bottom=0.2)
plt.show()

