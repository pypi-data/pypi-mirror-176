#!/usr/bin/env python
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

"""
Script for plotting cross sections generated by FEFF found in xmu.dat files.
"""

__author__ = "Alan Dozier"
__credits__ = "Anubhav Jain, Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "1.0.2"
__maintainer__ = "Alan Dozier"
__email__ = "adozier@uky.edu"
__date__ = "April 7, 2013"

import argparse

from pymatgen.io.feff.outputs import Xmu
from pymatgen.util.plotting import pretty_plot


def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(
        description="""
    Convenient DOS Plotter for Feff runs.
    Author: Alan Dozier
    Version: 1.0
    Last updated: April, 2013"""
    )

    parser.add_argument("filename", metavar="filename", type=str, nargs=1, help="xmu file to plot")
    parser.add_argument(
        "filename1",
        metavar="filename1",
        type=str,
        nargs=1,
        help="feff.inp filename to import",
    )

    plt = pretty_plot(12, 8)
    color_order = ["r", "b", "g", "c", "k", "m", "y"]

    args = parser.parse_args()
    xmu = Xmu.from_file(args.filename[0], args.filename1[0])

    data = xmu.as_dict()

    plt.title(data["calc"] + " Feff9.6 Calculation for " + data["atom"] + " in " + data["formula"] + " unit cell")
    plt.xlabel("Energies (eV)")
    plt.ylabel("Absorption Cross-section")

    x = data["energies"]
    y = data["scross"]
    tle = "Single " + data["atom"] + " " + data["edge"] + " edge"
    plt.plot(x, y, color_order[1 % 7], label=tle)

    y = data["across"]
    tle = data["atom"] + " " + data["edge"] + " edge in " + data["formula"]
    plt.plot(x, y, color_order[2 % 7], label=tle)

    plt.legend()
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize=15)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
