# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
contains the HDF5ConfigHandler
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "08/03/2021"


from .config import HDF5Config
from nxtomomill import utils
from nxtomomill.utils import Format
from nxtomomill.io.utils import filter_str_def
from typing import Union
import logging
import os

_logger = logging.getLogger(__name__)


SETTABLE_PARAMETERS_UNITS = {
    "energy": "kev",
    "x_pixel_size": "m",
    "y_pixel_size": "m",
}

SETTABLE_PARAMETERS_TYPE = {
    "energy": float,
    "x_pixel_size": float,
    "y_pixel_size": float,
}

SETTABLE_PARAMETERS = SETTABLE_PARAMETERS_UNITS.keys()


def _extract_param_value(key_values):
    """extract all the key / values elements from the str_list. Expected
    format is `param_1_name param_1_value param_2_name param_2_value ...`

    :param str str_list: raw input string as `param_1_name param_1_value
                         param_2_name param_2_value ...`
    :return: dict of tuple (param_name, param_value)
    :rtype: dict
    """
    if len(key_values) % 2 != 0:
        raise ValueError(
            "Expect a pair `param_name, param_value` for each " "parameters"
        )

    def pairwise(it):
        it = iter(it)
        while True:
            try:
                yield next(it), next(it)
            except StopIteration:
                # no more elements in the iterator
                return

    res = {}
    for name, value in pairwise(key_values):
        if name not in SETTABLE_PARAMETERS:
            raise ValueError("parameters {} is not managed".format(name))
        if name in SETTABLE_PARAMETERS_TYPE:
            type_ = SETTABLE_PARAMETERS_TYPE[name]
            if type_ is not None:
                res[name] = type_(value)
                continue
        res[name] = value
    return res


class HDF5ConfigHandler:
    """Class to handle inputs to HDF5Config.
    And insure there is no opposite Information
    """

    def __init__(self, argparse_options, raise_error=True):
        self._argparse_options = argparse_options
        self._config = None
        self.build_configuration(raise_error=raise_error)

    @property
    def configuration(self) -> Union[None, HDF5Config]:
        return self._config

    @property
    def argparse_options(self):
        return self._argparse_options

    def build_configuration(self, raise_error) -> bool:
        """
        :param bool raise_error: raise error if encounter some errors. Else
                                 display a log message
        :return: True if the settings are valid
        """
        if self.argparse_options is None:
            err = "No argparse options provided"
            if raise_error:
                raise ValueError(err)
            else:
                _logger.error(err)
            return False

        options = self.argparse_options
        if options.config is not None:
            # check no other option are provided
            duplicated_inputs = []
            for opt in (
                "set_params",
                "align_titles",
                "proj_titles",
                "ref_titles",
                "dark_titles",
                "init_zserie_titles",
                "init_titles",
                "init_zserie_titles",
                "x_pixel_size_key",
                "y_pixel_size_key",
                "acq_expo_time_keys",
                "rot_angle_keys",
                "valid_camera_names",
                "z_trans_keys",
                "y_trans_keys",
                "x_trans_keys",
                "is_xrd_ct_format",
                "request_input",
                "raises_error",
                "ignore_sub_entries",
                "entries",
                "debug",
                "overwrite",
                "single_file",
                "file_extension",
                "field_of_view",
                "sample_detector_distance",
            ):
                if getattr(options, opt):
                    duplicated_inputs.append(opt)
            if len(duplicated_inputs) > 0:
                err = "You provided a configuration file and inputs " "for {}".format(
                    duplicated_inputs
                )
                if raise_error:
                    raise ValueError(err)
                else:
                    _logger.error(err)
                return False

        if options.config:
            config = HDF5Config.from_cfg_file(options.config)
        else:
            config = HDF5Config()
        # check input and output file
        if config.input_file is None:
            config.input_file = options.input_file
        elif options.input_file is not None and config.input_file != options.input_file:
            raise ValueError(
                "Two different input files provided from "
                "command line and from the configuration file"
            )
        if config.input_file is None:
            err = "No input file provided"
            if raise_error:
                raise ValueError(err)
            else:
                _logger.error(err)

        if config.output_file is None:
            config.output_file = options.output_file
        elif (
            options.output_file is not None
            and config.output_file != options.output_file
        ):
            raise ValueError(
                "Two different output files provided from "
                "command line and from the configuration file"
            )
        if config.output_file is None:
            input_file, input_file_ext = os.path.splitext(config.input_file)
            if config.file_extension is None:
                err = "If no outputfile provided you should provide the " "extension"
                if raise_error:
                    raise ValueError(err)
                else:
                    _logger.error(err)
            config.output_file = input_file + config.file_extension.value
        # set parameter from the arg parse options
        # key is the name of the argparse option.
        # value is a tuple: (name of the setter in the HDF5Config,
        # function to format the input)
        # TODO: map all values
        conv = utils.get_tuple_of_keys_from_cmd

        def conv_str_to_bool(bstr):
            return bstr in ("True", True)

        def conv_log_level(bool_debug):
            if bool_debug is True:
                return "debug"
            else:
                return "warning"

        def conv_xrd_ct_to_format(str_bool):
            if str_bool in ("True", True):
                return Format.XRD_CT
            elif str_bool in ("False", False):
                return Format.STANDARD
            else:
                return None

        mapping = {
            "valid_camera_names": ("valid_camera_names", conv),
            "overwrite": ("overwrite", conv_str_to_bool),
            "file_extension": ("file_extension", filter_str_def),
            "single_file": ("single_file", conv_str_to_bool),
            "debug": ("log_level", conv_log_level),
            "entries": ("entries", conv),
            "ignore_sub_entries": ("sub_entries_to_ignore", conv),
            "raises_error": ("raises_error", conv_str_to_bool),
            "field_of_view": ("field_of_view", filter_str_def),
            "request_input": ("request_input", conv_str_to_bool),
            "is_xrd_ct_format": ("format", conv_xrd_ct_to_format),
            "x_trans_keys": ("x_trans_keys", conv),
            "y_trans_keys": ("y_trans_keys", conv),
            "z_trans_keys": ("z_trans_keys", conv),
            "rot_angle_keys": ("rotation_angle_keys", conv),
            "sample_detector_distance": ("sample_detector_distance", conv),
            "acq_expo_time_keys": ("exposition_time_keys", conv),
            "x_pixel_size_key": ("x_pixel_size_paths", conv),
            "y_pixel_size_key": ("y_pixel_size_paths", conv),
            "init_titles": ("init_titles", conv),
            "init_zserie_titles": ("zserie_init_titles", conv),
            "dark_titles": ("dark_titles", conv),
            "ref_titles": ("flat_titles", conv),
            "proj_titles": ("projections_titles", conv),
            "align_titles": ("alignment_titles", conv),
            "set_params": ("param_already_defined", _extract_param_value),
        }
        for argparse_name, (config_name, format_fct) in mapping.items():
            argparse_value = getattr(options, argparse_name)
            if argparse_value is not None:
                value = format_fct(argparse_value)
                setattr(config, config_name, value)
        self._config = config

    def __str__(self):
        raise NotImplementedError("")
