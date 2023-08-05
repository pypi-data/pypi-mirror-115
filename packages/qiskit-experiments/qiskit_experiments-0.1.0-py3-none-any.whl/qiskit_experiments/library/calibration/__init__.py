# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
=======================================================================
Calibration Experiments (:mod:`qiskit_experiments.library.calibration`)
=======================================================================

.. currentmodule:: qiskit_experiments.library.calibration

.. warning::
    The calibrations interface is still in active development. It may have
    breaking API changes without deprecation warnings in future releases until
    otherwise indicated.

Calibrating qubit setups is the task of finding the pulse shapes and parameter
values that maximizes the fidelity of the resulting quantum operations. This
therefore requires experiments which are analyzed to extract parameter values.
Furthermore, the resulting parameter values and schedules must be managed. The
calibration module in Qiskit experiments allows users to run calibration
experiments and manage the resulting schedules and parameter values.

The following experiments are designed to calibrate parameter values. Some experiments such
as :class:`QubitSpectroscopy` can both be seen as characterization and calibrations
experiments. Such experiments can be found in the
:mod:`qiskit_experiments.library.characterization`
module.

.. autosummary::
    :toctree: ../stubs/
    :template: autosummary/experiment.rst

    DragCal
    Rabi
    FineAmplitude
    FineXAmplitude
    FineSXAmplitude

Calibration analysis
====================
.. autosummary::
    :toctree: ../stubs/
    :template: autosummary/analysis.rst

    OscillationAnalysis
    DragCalAnalysis
    FineAmplitudeAnalysis

Calibrations management
=======================

See :mod:`qiskit_experiments.calibration_management`.
"""

from .drag import DragCal
from .rabi import Rabi, EFRabi
from .fine_amplitude import FineAmplitude, FineXAmplitude, FineSXAmplitude

from .analysis.oscillation_analysis import OscillationAnalysis
from .analysis.drag_analysis import DragCalAnalysis
from .analysis.fine_amplitude_analysis import FineAmplitudeAnalysis
