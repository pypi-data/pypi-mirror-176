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

# Run from project folder with: python -m daccuracy.test.test-input

from pathlib import Path as path_t

import matplotlib.pyplot as pypl
import numpy as nmpy
import skimage.io as skio

from daccuracy.brick.image import DetectionWithTolerance


BASE_FOLDER = path_t(__file__).parent
path_components = ("detection", "detection-1.png")
ground_truth = skio.imread(BASE_FOLDER.joinpath(*path_components))

assert nmpy.array_equal(ground_truth, DetectionWithTolerance(ground_truth, 0.0))

pypl.matshow(ground_truth)
pypl.gca().set_title(f"Original (max={nmpy.amax(ground_truth)})")

cum_tol = nmpy.zeros_like(ground_truth)
for tolerance_ in range(5):
    current_tol = DetectionWithTolerance(ground_truth, tolerance_)
    cum_tol += current_tol > 0

    pypl.matshow(current_tol)
    pypl.gca().set_title(f"With tolerance {tolerance_} (max={nmpy.amax(current_tol)})")

pypl.matshow(cum_tol)
pypl.gca().set_title("Summed Tolerance Images")

pypl.show()
