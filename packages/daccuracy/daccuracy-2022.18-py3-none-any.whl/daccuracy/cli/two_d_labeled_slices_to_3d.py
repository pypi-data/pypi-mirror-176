# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import sys as sstm
from argparse import ArgumentParser as argument_parser_t
from argparse import RawDescriptionHelpFormatter
from pathlib import Path as path_t
from typing import Optional, Sequence, Tuple

import __main__ as main_package
import numpy as nmpy
import skimage.io as skio

import daccuracy.brick.input as inpt
import daccuracy.brick.measures as msre


array_t = nmpy.ndarray


DESCRIPTION = (
    "Relabel coherently a set of 2-dimensional images into a 3-dimensional image."
)


def _LabeledImage(folder: path_t, relabel: Optional[str], /) -> array_t:
    """"""
    output = None

    for document in sorted(folder.iterdir()):
        if not document.is_file():
            continue

        next_image = inpt.ImageAtPath(document, relabel, None, None, None, None)
        if next_image is None:
            continue
        if next_image.ndim != 2:
            print(f"{next_image.ndim}: Invalid image dimension. Expected=2. Ignoring.")
            continue

        if output is None:
            output = [next_image]
        else:
            previous_image = output[-1]

            n_previous_objects = nmpy.amax(previous_image).item()
            n_next_objects = nmpy.amax(next_image).item()
            next_2_previous_associations = msre.ObjectAssociations(
                n_next_objects, next_image, n_previous_objects, previous_image
            )
            unassociated = set(range(1, n_next_objects + 1)).difference(
                next_2_previous_associations.keys()
            )
            for new_label, next_label in enumerate(
                unassociated, start=n_previous_objects + 1
            ):
                next_2_previous_associations[next_label] = new_label

            new_image = nmpy.zeros_like(next_image)
            for next_label, previous_label in next_2_previous_associations.items():
                new_image[next_image == next_label] = previous_label
            output.append(new_image)

    return nmpy.dstack(output)


def _ArgumentParser() -> argument_parser_t:
    """"""
    output = argument_parser_t(
        prog=path_t(main_package.__file__).stem,
        description=DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )

    output.add_argument(
        "--2d",
        type=str,
        required=True,
        dest="input_path",
        metavar="Input_folder",
        help="Folder containing a set of labeled 2-dimensional images.",
    )
    output.add_argument(
        "--relabel",
        type=str,
        choices=("seq", "full"),
        default=None,
        dest="relabel",
        help="If present, this option instructs to relabel the 2-dimensional images with sequential labels (seq),"
        "or to fully relabel the non-zero regions of the 2-dimensional images with maximum connectivity (full).",
    )
    output.add_argument(
        "--3d",
        type=str,
        required=True,
        dest="output_path",
        metavar="Output_file",
        help="File to store the coherently labeled 3-dimensional image.",
    )

    return output


def _ProcessedArguments(
    arguments: Sequence[str], /
) -> Tuple[path_t, path_t, Optional[str]]:
    """"""
    parser = _ArgumentParser()
    arguments = parser.parse_args(arguments)

    input_path = path_t(arguments.input_path)
    output_path = path_t(arguments.output_path)
    relabel = arguments.relabel

    if not input_path.is_dir():
        print(f"{input_path}: Not a folder", file=sstm.stderr)
        sstm.exit(-1)
    if output_path.exists():
        print(f"{output_path}: Existing file or folder; Exiting", file=sstm.stderr)
        sstm.exit(-1)

    return input_path, output_path, relabel


def Main() -> None:
    """"""
    input_path, output_path, relabel = _ProcessedArguments(sstm.argv[1:])

    labeled = _LabeledImage(input_path, relabel)

    if output_path.exists():  # Re-test, just in case
        print(f"{output_path}: Existing file or folder; Exiting", file=sstm.stderr)
        sstm.exit(-1)

    skio.imsave(output_path, labeled)


if __name__ == "__main__":
    #
    Main()
