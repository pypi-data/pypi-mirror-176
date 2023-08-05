# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

"""
This module defines classes for reading/manipulating/writing the main sections
of FEFF input file(feff.inp), namely HEADER, ATOMS, POTENTIAL and the program
control tags.

XANES and EXAFS input files, are available, for non-spin case at this time.
"""

from __future__ import annotations

import re
import warnings

import numpy as np
from monty.io import zopen
from monty.json import MSONable
from tabulate import tabulate

from pymatgen.core.lattice import Lattice
from pymatgen.core.periodic_table import Element
from pymatgen.core.structure import Molecule, Structure
from pymatgen.io.cif import CifParser
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.util.io_utils import clean_lines
from pymatgen.util.string import str_delimited

__author__ = "Alan Dozier, Kiran Mathew"
__credits__ = "Anubhav Jain, Shyue Ping Ong"
__copyright__ = "Copyright 2011, The Materials Project"
__version__ = "1.0.3"
__maintainer__ = "Alan Dozier"
__email__ = "adozier@uky.edu"
__status__ = "Beta"
__date__ = "April 7, 2013"

# **Non-exhaustive** list of valid Feff.inp tags
VALID_FEFF_TAGS = (
    "CONTROL",
    "PRINT",
    "ATOMS",
    "POTENTIALS",
    "RECIPROCAL",
    "REAL",
    "MARKER",
    "LATTICE",
    "TITLE",
    "RMULTIPLIER",
    "SGROUP",
    "COORDINATES",
    "EQUIVALENCE",
    "CIF",
    "CGRID",
    "CFAVERAGE",
    "OVERLAP",
    "EXAFS",
    "XANES",
    "ELNES",
    "EXELFS",
    "LDOS",
    "ELLIPTICITY",
    "MULTIPOLE",
    "POLARIZATION",
    "RHOZZP",
    "DANES",
    "FPRIME",
    "NRIXS",
    "XES",
    "XNCD",
    "XMCD",
    "XNCDCONTROL",
    "END",
    "KMESH",
    "PRINT",
    "EGRID",
    "DIMS",
    "AFOLP",
    "EDGE",
    "COMPTON",
    "DANES",
    "FPRIME",
    "MDFF",
    "HOLE",
    "COREHOLE",
    "S02",
    "CHBROAD",
    "EXCHANGE",
    "FOLP",
    "NOHOLE",
    "RGRID",
    "SCF",
    "UNFREEZEF",
    "CHSHIFT",
    "DEBYE",
    "INTERSTITIAL",
    "CHWIDTH",
    "EGAP",
    "EPS0",
    "EXTPOT",
    "ION",
    "JUMPRM",
    "EXPOT",
    "SPIN",
    "LJMAX",
    "LDEC",
    "MPSE",
    "PLASMON",
    "RPHASES",
    "RSIGMA",
    "PMBSE",
    "TDLDA",
    "FMS",
    "DEBYA",
    "OPCONS",
    "PREP",
    "RESTART",
    "SCREEN",
    "SETE",
    "STRFACTORS",
    "BANDSTRUCTURE",
    "RPATH",
    "NLEG",
    "PCRITERIA",
    "SYMMETRY",
    "SS",
    "CRITERIA",
    "IORDER",
    "NSTAR",
    "ABSOLUTE",
    "CORRECTIONS",
    "SIG2",
    "SIG3",
    "MBCONV",
    "SFCONV",
    "RCONV",
    "SELF",
    "SFSE",
    "MAGIC",
    "TARGET",
    "STRFAC",
)


class Header(MSONable):
    """
    Creates Header for the FEFF input file.

    Has the following format::

        * This feff.inp file generated by pymatgen, materialsproject.org
        TITLE comment:
        TITLE Source: CoO19128.cif
        TITLE Structure Summary: (Co2 O2)
        TITLE Reduced formula: CoO
        TITLE space group: P1,   space number: 1
        TITLE abc: 3.297078 3.297078 5.254213
        TITLE angles: 90.0 90.0 120.0
        TITLE sites: 4
        * 1 Co     0.666666     0.333332     0.496324
        * 2 Co     0.333333     0.666667     0.996324
        * 3 O     0.666666     0.333332     0.878676
        * 4 O     0.333333     0.666667     0.378675
    """

    def __init__(
        self, struct: Structure | Molecule, source: str = "", comment: str = "", spacegroup_analyzer_settings=None
    ):
        """
        Args:
            struct: Structure or Molecule object. If a Structure, SpaceGroupAnalyzer is used to
                determine symmetrically-equivalent sites. If a Molecule, there is no symmetry
                checking.
            source: User supplied identifier, i.e. for Materials Project this
                would be the material ID number
            comment: Comment for first header line
            spacegroup_analyzer_settings: keyword arguments passed to SpacegroupAnalyzer
                (only used for Structure inputs)
        """
        self.spacegroup_analyzer_settings = spacegroup_analyzer_settings or {}
        self.periodic = False
        self.struct = struct
        self.source = source
        # if Structure, check symmetry
        if isinstance(self.struct, Structure):
            self.periodic = True
            sym = SpacegroupAnalyzer(struct, **self.spacegroup_analyzer_settings)
            data = sym.get_symmetry_dataset()
            self.space_number = data.get("number")
            self.space_group = data.get("international")
        # for Molecule, skip the symmetry check
        elif isinstance(self.struct, Molecule):
            self.periodic = False
            self.space_number = None
            self.space_group = None
        else:
            raise ValueError("'struct' argument must be a Structure or Molecule!")
        self.comment = comment or "None given"

    @staticmethod
    def from_cif_file(cif_file, source="", comment=""):
        """
        Static method to create Header object from cif_file

        Args:
            cif_file: cif_file path and name
            source: User supplied identifier, i.e. for Materials Project this
                would be the material ID number
            comment: User comment that goes in header

        Returns:
            Header Object
        """
        r = CifParser(cif_file)
        structure = r.get_structures()[0]
        return Header(structure, source, comment)

    @property
    def structure_symmetry(self):
        """
        Returns space number and space group

        Returns:
            Space number and space group list
        """
        return self.space_group, self.space_number

    @property
    def formula(self):
        """
        Formula of structure
        """
        return self.struct.composition.formula

    @staticmethod
    def from_file(filename):
        """
        Returns Header object from file
        """
        hs = Header.header_string_from_file(filename)
        return Header.from_string(hs)

    @staticmethod
    def header_string_from_file(filename="feff.inp"):
        """
        Reads Header string from either a HEADER file or feff.inp file
        Will also read a header from a non-pymatgen generated feff.inp file

        Args:
            filename: File name containing the Header data.

        Returns:
            Reads header string.
        """
        with zopen(filename, "r") as fobject:
            f = fobject.readlines()
            feff_header_str = []
            ln = 0

            # Checks to see if generated by pymatgen
            try:
                feffpmg = f[0].find("pymatgen")
                if feffpmg == -1:
                    feffpmg = False
            except IndexError:
                feffpmg = False

            # Reads pymatgen generated header or feff.inp file
            if feffpmg:
                nsites = int(f[8].split()[2])
                for line in f:
                    ln += 1
                    if ln <= nsites + 9:
                        feff_header_str.append(line)
            else:
                # Reads header from header from feff.inp file from unknown
                # source
                end = 0
                for line in f:
                    if (line[0] == "*" or line[0] == "T") and end == 0:
                        feff_header_str.append(line.replace("\r", ""))
                    else:
                        end = 1

        return "".join(feff_header_str)

    @staticmethod
    def from_string(header_str):
        """
        Reads Header string and returns Header object if header was
        generated by pymatgen.
        Note: Checks to see if generated by pymatgen, if not it is impossible
            to generate structure object so it is not possible to generate
            header object and routine ends

        Args:
            header_str: pymatgen generated feff.inp header

        Returns:
            Structure object.
        """
        lines = tuple(clean_lines(header_str.split("\n"), False))
        comment1 = lines[0]
        feffpmg = comment1.find("pymatgen")
        if feffpmg == -1:
            feffpmg = False
        if feffpmg:
            comment2 = " ".join(lines[1].split()[2:])

            source = " ".join(lines[2].split()[2:])
            basis_vec = lines[6].split(":")[-1].split()
            # a, b, c
            a = float(basis_vec[0])
            b = float(basis_vec[1])
            c = float(basis_vec[2])
            lengths = [a, b, c]
            # alpha, beta, gamma
            basis_ang = lines[7].split(":")[-1].split()
            alpha = float(basis_ang[0])
            beta = float(basis_ang[1])
            gamma = float(basis_ang[2])
            angles = [alpha, beta, gamma]

            lattice = Lattice.from_parameters(*lengths, *angles)

            natoms = int(lines[8].split(":")[-1].split()[0])

            atomic_symbols = []
            for i in range(9, 9 + natoms):
                atomic_symbols.append(lines[i].split()[2])

            # read the atomic coordinates
            coords = []
            for i in range(natoms):
                toks = lines[i + 9].split()
                coords.append([float(s) for s in toks[3:]])

            struct = Structure(lattice, atomic_symbols, coords, False, False, False)

            h = Header(struct, source, comment2)

            return h

        raise ValueError("Header not generated by pymatgen, cannot return header object")

    def __str__(self):
        """
        String representation of Header.
        """

        def to_s(x):
            return f"{x:0.6f}"

        output = [
            "* This FEFF.inp file generated by pymatgen",
            "".join(["TITLE comment: ", self.comment]),
            "".join(["TITLE Source:  ", self.source]),
            f"TITLE Structure Summary:  {self.struct.composition.formula}",
            f"TITLE Reduced formula:  {self.struct.composition.reduced_formula}",
        ]

        if self.periodic:
            output += [
                f"TITLE space group: ({self.space_group}), space number:  ({self.space_number})",
                f"TITLE abc:{' '.join([to_s(i).rjust(10) for i in self.struct.lattice.abc])}",
                f"TITLE angles:{' '.join([to_s(i).rjust(10) for i in self.struct.lattice.angles])}",
            ]

        output.append(f"TITLE sites: {self.struct.num_sites}")

        for i, site in enumerate(self.struct):
            if isinstance(self.struct, Structure):
                coords = [to_s(j).rjust(12) for j in site.frac_coords]
            elif isinstance(self.struct, Molecule):
                coords = [to_s(j).rjust(12) for j in site.coords]
            output.append(
                " ".join(
                    [
                        "*",
                        str(i + 1),
                        site.species_string,
                        " ".join(coords),
                    ]
                )
            )
        return "\n".join(output)

    def write_file(self, filename="HEADER"):
        """
        Writes Header into filename on disk.

        Args:
            filename: Filename and path for file to be written to disk
        """
        with open(filename, "w") as f:
            f.write(str(self) + "\n")


class Atoms(MSONable):
    """
    Atomic cluster centered around the absorbing atom.
    """

    def __init__(self, struct, absorbing_atom, radius):
        """
        Args:
            struct (Structure): input structure
            absorbing_atom (str/int): Symbol for absorbing atom or site index
            radius (float): radius of the atom cluster in Angstroms.
        """
        if struct.is_ordered:
            self.struct = struct
            atom_sym = get_absorbing_atom_symbol_index(absorbing_atom, struct)[0]
            self.pot_dict = get_atom_map(struct, atom_sym)
        else:
            raise ValueError("Structure with partial occupancies cannot be converted into atomic coordinates!")

        self.absorbing_atom, self.center_index = get_absorbing_atom_symbol_index(absorbing_atom, struct)
        self.radius = radius
        self._cluster = self._set_cluster()

    def _set_cluster(self):
        """
        Compute and set the cluster of atoms as a Molecule object. The site
        coordinates are translated such that the absorbing atom (aka central
        atom) is at the origin.

        Returns:
            Molecule
        """
        center = self.struct[self.center_index].coords
        # this method builds a supercell containing all periodic images of
        # the unit cell within the specified radius, excluding the central atom
        sphere = self.struct.get_neighbors(self.struct[self.center_index], self.radius)

        symbols = [self.absorbing_atom]
        coords = [[0, 0, 0]]
        for site_dist in sphere:
            site_symbol = re.sub(r"[^aA-zZ]+", "", site_dist[0].species_string)
            symbols.append(site_symbol)
            coords.append(site_dist[0].coords - center)
        return Molecule(symbols, coords)

    @property
    def cluster(self):
        """
        Returns the atomic cluster as a Molecule object.
        """
        return self._cluster

    @staticmethod
    def atoms_string_from_file(filename):
        """
        Reads atomic shells from file such as feff.inp or ATOMS file
        The lines are arranged as follows:

        x y z   ipot    Atom Symbol   Distance   Number

        with distance being the shell radius and ipot an integer identifying
        the potential used.

        Args:
            filename: File name containing atomic coord data.

        Returns:
            Atoms string.
        """
        with zopen(filename, "rt") as fobject:
            f = fobject.readlines()
            coords = 0
            atoms_str = []

            for line in f:
                if coords == 0:
                    find_atoms = line.find("ATOMS")
                    if find_atoms >= 0:
                        coords = 1
                if coords == 1 and "END" not in line:
                    atoms_str.append(line.replace("\r", ""))

        return "".join(atoms_str)

    @staticmethod
    def cluster_from_file(filename):
        """
        Parse the feff input file and return the atomic cluster as a Molecule
        object.

        Args:
            filename (str): path the feff input file

        Returns:
            Molecule: the atomic cluster as Molecule object. The absorbing atom
                is the one at the origin.
        """
        atoms_string = Atoms.atoms_string_from_file(filename)
        line_list = [l.split() for l in atoms_string.splitlines()[3:]]
        coords = []
        symbols = []
        for l in line_list:
            if l:
                coords.append([float(i) for i in l[:3]])
                symbols.append(l[4])
        return Molecule(symbols, coords)

    def get_lines(self) -> list[list[str | int]]:
        """
        Returns a list of string representations of the atomic configuration
        information(x, y, z, ipot, atom_symbol, distance, id).

        Returns:
            list[list[str | int]]: lines sorted by the distance from the absorbing atom.
        """
        lines = [
            [
                f"{self._cluster[0].x:f}",
                f"{self._cluster[0].y:f}",
                f"{self._cluster[0].z:f}",
                0,
                self.absorbing_atom,
                "0.0",
                0,
            ]
        ]
        for i, site in enumerate(self._cluster[1:]):
            site_symbol = re.sub(r"[^aA-zZ]+", "", site.species_string)
            ipot = self.pot_dict[site_symbol]
            lines.append(
                [
                    f"{site.x:f}",
                    f"{site.y:f}",
                    f"{site.z:f}",
                    ipot,
                    site_symbol,
                    f"{self._cluster.get_distance(0, i + 1):f}",
                    i + 1,
                ]
            )

        # sort by distance from absorbing atom
        return sorted(lines, key=lambda line: float(line[5]))

    def __str__(self):
        """
        String representation of Atoms file.
        """
        lines_sorted = self.get_lines()
        # TODO: remove the formatting and update the unittests
        lines_formatted = str(
            tabulate(
                lines_sorted,
                headers=["*       x", "y", "z", "ipot", "Atom", "Distance", "Number"],
            )
        )
        atom_list = lines_formatted.replace("--", "**")
        return "".join(["ATOMS\n", atom_list, "\nEND\n"])

    def write_file(self, filename="ATOMS"):
        """
        Write Atoms list to file.

        Args:
           filename: path for file to be written
        """
        with zopen(filename, "wt") as f:
            f.write(str(self) + "\n")


class Tags(dict):
    """
    FEFF control parameters.
    """

    def __init__(self, params=None):
        """
        Args:
            params: A set of input parameters as a dictionary.
        """
        super().__init__()
        if params:
            self.update(params)

    def __setitem__(self, key, val):
        """
        Add parameter-val pair. Warns if parameter is not in list of valid
        Feff tags. Also cleans the parameter and val by stripping leading and
        trailing white spaces.

        Arg:
            key: dict key value
            value: value associated with key in dictionary
        """
        if key.strip().upper() not in VALID_FEFF_TAGS:
            warnings.warn(key.strip() + " not in VALID_FEFF_TAGS list")
        super().__setitem__(
            key.strip(),
            Tags.proc_val(key.strip(), val.strip()) if isinstance(val, str) else val,
        )

    def as_dict(self):
        """
        Dict representation.

        Returns:
            Dictionary of parameters from fefftags object
        """
        tags_dict = dict(self)
        tags_dict["@module"] = type(self).__module__
        tags_dict["@class"] = type(self).__name__
        return tags_dict

    @staticmethod
    def from_dict(d):
        """
        Creates Tags object from a dictionary.

        Args:
            d: Dict of feff parameters and values.

        Returns:
            Tags object
        """
        i = Tags()
        for k, v in d.items():
            if k not in ("@module", "@class"):
                i[k] = v
        return i

    def get_string(self, sort_keys=False, pretty=False):
        """
        Returns a string representation of the Tags. The reason why this
        method is different from the __str__ method is to provide options
        for pretty printing.

        Args:
            sort_keys: Set to True to sort the Feff parameters alphabetically.
                Defaults to False.
            pretty: Set to True for pretty aligned output. Defaults to False.

        Returns:
            String representation of Tags.
        """
        keys = list(self)
        if sort_keys:
            keys = sorted(keys)
        lines = []
        for k in keys:
            if k == "IONS":
                for t in self[k]:
                    lines.append(["ION", f"{t[0]} {t[1]:.4f}"])
            elif isinstance(self[k], dict):
                if k in ["ELNES", "EXELFS"]:
                    lines.append([k, self._stringify_val(self[k]["ENERGY"])])
                    beam_energy = self._stringify_val(self[k]["BEAM_ENERGY"])
                    beam_energy_list = beam_energy.split()
                    if int(beam_energy_list[1]) == 0:  # aver=0, specific beam direction
                        lines.append([beam_energy])
                        lines.append([self._stringify_val(self[k]["BEAM_DIRECTION"])])
                    else:
                        # no cross terms for orientation averaged spectrum
                        beam_energy_list[2] = str(0)
                        lines.append([self._stringify_val(beam_energy_list)])
                    lines.append([self._stringify_val(self[k]["ANGLES"])])
                    lines.append([self._stringify_val(self[k]["MESH"])])
                    lines.append([self._stringify_val(self[k]["POSITION"])])
            else:
                lines.append([k, self._stringify_val(self[k])])
        if pretty:
            return tabulate(lines)

        return str_delimited(lines, None, " ")

    @staticmethod
    def _stringify_val(val):
        """
        Convert the given value to string.
        """
        if isinstance(val, list):
            return " ".join(map(str, val))

        return str(val)

    def __str__(self):
        return self.get_string()

    def write_file(self, filename="PARAMETERS"):
        """
        Write Tags to a Feff parameter tag file.

        Args:
            filename: filename and path to write to.
        """
        with zopen(filename, "wt") as f:
            f.write(f"{self}\n")

    @staticmethod
    def from_file(filename="feff.inp"):
        """
        Creates a Feff_tag dictionary from a PARAMETER or feff.inp file.

        Args:
            filename: Filename for either PARAMETER or feff.inp file

        Returns:
            Feff_tag object
        """
        with zopen(filename, "rt") as f:
            lines = list(clean_lines(f.readlines()))
        params = {}
        eels_params = []
        ieels = -1
        ieels_max = -1
        for i, line in enumerate(lines):
            m = re.match(r"([A-Z]+\d*\d*)\s*(.*)", line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                val = Tags.proc_val(key, val)
                if key not in ("ATOMS", "POTENTIALS", "END", "TITLE"):
                    if key in ["ELNES", "EXELFS"]:
                        ieels = i
                        ieels_max = ieels + 5
                    else:
                        params[key] = val
            if ieels >= 0:
                if ieels <= i <= ieels_max:
                    if i == ieels + 1:
                        if int(line.split()[1]) == 1:
                            ieels_max -= 1
                    eels_params.append(line)

        if eels_params:
            if len(eels_params) == 6:
                eels_keys = [
                    "BEAM_ENERGY",
                    "BEAM_DIRECTION",
                    "ANGLES",
                    "MESH",
                    "POSITION",
                ]
            else:
                eels_keys = ["BEAM_ENERGY", "ANGLES", "MESH", "POSITION"]
            eels_dict = {"ENERGY": Tags._stringify_val(eels_params[0].split()[1:])}
            for k, v in zip(eels_keys, eels_params[1:]):
                eels_dict[k] = str(v)
            params[str(eels_params[0].split()[0])] = eels_dict

        return Tags(params)

    @staticmethod
    def proc_val(key, val):
        """
        Static helper method to convert Feff parameters to proper types, e.g.
        integers, floats, lists, etc.

        Args:
            key: Feff parameter key
            val: Actual value of Feff parameter.
        """
        list_type_keys = list(VALID_FEFF_TAGS)
        del list_type_keys[list_type_keys.index("ELNES")]
        del list_type_keys[list_type_keys.index("EXELFS")]
        boolean_type_keys = ()
        float_type_keys = ("S02", "EXAFS", "RPATH")

        def smart_int_or_float(numstr):
            if numstr.find(".") != -1 or numstr.lower().find("e") != -1:
                return float(numstr)
            return int(numstr)

        try:
            if key.lower() == "cif":
                m = re.search(r"\w+.cif", val)
                return m.group(0)

            if key in list_type_keys:
                output = []
                toks = re.split(r"\s+", val)

                for tok in toks:
                    m = re.match(r"(\d+)\*([\d\.\-\+]+)", tok)
                    if m:
                        output.extend([smart_int_or_float(m.group(2))] * int(m.group(1)))
                    else:
                        output.append(smart_int_or_float(tok))
                return output
            if key in boolean_type_keys:
                m = re.search(r"^\W+([TtFf])", val)
                if m:
                    return m.group(1) in ["T", "t"]
                raise ValueError(key + " should be a boolean type!")

            if key in float_type_keys:
                return float(val)

        except ValueError:
            return val.capitalize()

        return val.capitalize()

    def diff(self, other):
        """
        Diff function. Compares two PARAMETER files and indicates which
        parameters are the same and which are not. Useful for checking whether
        two runs were done using the same parameters.

        Args:
            other: The other PARAMETER dictionary to compare to.

        Returns:
            Dict of the format {"Same" : parameters_that_are_the_same,
            "Different": parameters_that_are_different} Note that the
            parameters are return as full dictionaries of values.
        """
        similar_param = {}
        different_param = {}
        for k1, v1 in self.items():
            if k1 not in other:
                different_param[k1] = {"FEFF_TAGS1": v1, "FEFF_TAGS2": "Default"}
            elif v1 != other[k1]:
                different_param[k1] = {"FEFF_TAGS1": v1, "FEFF_TAGS2": other[k1]}
            else:
                similar_param[k1] = v1
        for k2, v2 in other.items():
            if k2 not in similar_param and k2 not in different_param:
                if k2 not in self:
                    different_param[k2] = {"FEFF_TAGS1": "Default", "FEFF_TAGS2": v2}
        return {"Same": similar_param, "Different": different_param}

    def __add__(self, other):
        """
        Add all the values of another Tags object to this object
        Facilitates the use of "standard" Tags
        """
        params = dict(self)
        for k, v in other.items():
            if k in self and v != self[k]:
                raise ValueError("Tags have conflicting values!")
            params[k] = v
        return Tags(params)


class Potential(MSONable):
    """
    FEFF atomic potential.
    """

    def __init__(self, struct, absorbing_atom):
        """
        Args:
            struct (Structure): Structure object.
            absorbing_atom (str/int): Absorbing atom symbol or site index
        """
        if struct.is_ordered:
            self.struct = struct
            atom_sym = get_absorbing_atom_symbol_index(absorbing_atom, struct)[0]
            self.pot_dict = get_atom_map(struct, atom_sym)
        else:
            raise ValueError("Structure with partial occupancies cannot be converted into atomic coordinates!")

        self.absorbing_atom, _ = get_absorbing_atom_symbol_index(absorbing_atom, struct)

    @staticmethod
    def pot_string_from_file(filename="feff.inp"):
        """
        Reads Potential parameters from a feff.inp or FEFFPOT file.
        The lines are arranged as follows:

          ipot   Z   element   lmax1   lmax2   stoichometry   spinph

        Args:
            filename: file name containing potential data.

        Returns:
            FEFFPOT string.
        """
        with zopen(filename, "rt") as f_object:
            f = f_object.readlines()
            ln = -1
            pot_str = ["POTENTIALS\n"]
            pot_tag = -1
            pot_data = 0
            pot_data_over = 1

            sep_line_pattern = [
                re.compile("ipot.*Z.*tag.*lmax1.*lmax2.*spinph"),
                re.compile("^[*]+.*[*]+$"),
            ]

            for line in f:
                if pot_data_over == 1:
                    ln += 1
                    if pot_tag == -1:
                        pot_tag = line.find("POTENTIALS")
                        ln = 0
                    if pot_tag >= 0 and ln > 0 and pot_data_over > 0:
                        try:
                            if len(sep_line_pattern[0].findall(line)) > 0 or len(sep_line_pattern[1].findall(line)) > 0:
                                pot_str.append(line)
                            elif int(line.split()[0]) == pot_data:
                                pot_data += 1
                                pot_str.append(line.replace("\r", ""))
                        except (ValueError, IndexError):
                            if pot_data > 0:
                                pot_data_over = 0

        return "".join(pot_str).rstrip("\n")

    @staticmethod
    def pot_dict_from_string(pot_data):
        """
        Creates atomic symbol/potential number dictionary
        forward and reverse

        Arg:
            pot_data: potential data in string format

        Returns:
            forward and reverse atom symbol and potential number dictionaries.
        """
        pot_dict = {}
        pot_dict_reverse = {}
        begin = 0
        ln = -1

        for line in pot_data.split("\n"):
            try:
                if begin == 0 and line.split()[0] == "0":
                    begin += 1
                    ln = 0
                if begin == 1:
                    ln += 1
                if ln > 0:
                    atom = line.split()[2]
                    index = int(line.split()[0])
                    pot_dict[atom] = index
                    pot_dict_reverse[index] = atom
            except (ValueError, IndexError):
                pass
        return pot_dict, pot_dict_reverse

    def __str__(self):
        """
        Returns a string representation of potential parameters to be used in
        the feff.inp file,
        determined from structure object.

                The lines are arranged as follows:

          ipot   Z   element   lmax1   lmax2   stoichiometry   spinph

        Returns:
            String representation of Atomic Coordinate Shells.
        """
        central_element = Element(self.absorbing_atom)
        ipotrow = [[0, central_element.Z, central_element.symbol, -1, -1, 0.0001, 0]]
        for el, amt in self.struct.composition.items():
            # if there is only one atom and it is the absorbing element, it should
            # be excluded from this list. Otherwise the error `No atoms or overlap
            # cards for unique pot X` will be encountered.
            if el == central_element and amt == 1:
                continue
            ipot = self.pot_dict[el.symbol]
            ipotrow.append([ipot, el.Z, el.symbol, -1, -1, amt, 0])
        ipot_sorted = sorted(ipotrow, key=lambda x: x[0])
        ipotrow = str(
            tabulate(
                ipot_sorted,
                headers=[
                    "*ipot",
                    "Z",
                    "tag",
                    "lmax1",
                    "lmax2",
                    "xnatph(stoichometry)",
                    "spinph",
                ],
            )
        )
        ipotlist = ipotrow.replace("--", "**")
        ipotlist = "".join(["POTENTIALS\n", ipotlist])

        return ipotlist

    def write_file(self, filename="POTENTIALS"):
        """
        Write to file.

        Args:
            filename: filename and path to write potential file to.
        """
        with zopen(filename, "wt") as f:
            f.write(str(self) + "\n")


class Paths(MSONable):
    """
    Set FEFF scattering paths('paths.dat' file used by the 'genfmt' module).
    """

    def __init__(self, atoms, paths, degeneracies=None):
        """
        Args:
            atoms (Atoms): Atoms object
            paths (list(list)): list of paths. Each path is a list of atom indices in the atomic
                cluster(the molecular cluster created by Atoms class).
                e.g. [[0, 1, 2], [5, 9, 4, 1]] -> 2 paths: one with 3 legs and the other with 4 legs.
            degeneracies (list): list of degeneracies, one for each path. Set to 1 if not specified.
        """
        self.atoms = atoms
        self.paths = paths
        self.degeneracies = degeneracies or [1] * len(paths)
        assert len(self.degeneracies) == len(self.paths)

    def __str__(self):
        lines = ["PATH", "---------------"]
        # max possible, to avoid name collision count down from max value.
        path_index = 9999
        for i, legs in enumerate(self.paths):
            lines.append(f"{path_index} {len(legs)} {self.degeneracies[i]}")
            lines.append("x y z ipot label")
            for l in legs:
                coords = self.atoms.cluster[l].coords.tolist()

                tmp = f"{coords[0]:.6f} {coords[1]:.6f} {coords[2]:.6f}"
                element = str(self.atoms.cluster[l].specie.name)
                # the potential index for the absorbing atom(the one at the cluster origin) is 0
                potential = 0 if np.linalg.norm(coords) <= 1e-6 else self.atoms.pot_dict[element]
                tmp = f"{tmp} {potential} {element}"
                lines.append(tmp)
            path_index -= 1
        return "\n".join(lines)

    def write_file(self, filename="paths.dat"):
        """
        Write paths.dat.
        """
        with zopen(filename, "wt") as f:
            f.write(str(self) + "\n")


class FeffParserError(Exception):
    """
    Exception class for Structure.
    Raised when the structure has problems, e.g., atoms that are too close.
    """


def get_atom_map(structure, absorbing_atom=None):
    """
    Returns a dict that maps each atomic symbol to a unique integer starting
    from 1.

    Args:
        structure (Structure)
        absorbing_atom (str): symbol

    Returns:
        dict
    """
    unique_pot_atoms = sorted({site.specie.symbol for site in structure})

    # if there is only a single absorbing atom in the structure,
    # it should be excluded from this list
    if absorbing_atom:
        if len(structure.indices_from_symbol(absorbing_atom)) == 1:
            unique_pot_atoms.remove(absorbing_atom)

    atom_map = {}
    for i, atom in enumerate(unique_pot_atoms):
        atom_map[atom] = i + 1
    return atom_map


def get_absorbing_atom_symbol_index(absorbing_atom, structure):
    """
    Return the absorbing atom symbol and site index in the given structure.

    Args:
        absorbing_atom (str/int): symbol or site index
        structure (Structure)

    Returns:
        str, int: symbol and site index
    """
    if isinstance(absorbing_atom, str):
        return absorbing_atom, structure.indices_from_symbol(absorbing_atom)[0]
    if isinstance(absorbing_atom, int):
        return str(structure[absorbing_atom].specie), absorbing_atom
    raise ValueError("absorbing_atom must be either specie symbol or site index")
