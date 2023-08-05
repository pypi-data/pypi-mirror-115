# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "23/02/2021"


import unittest
import shutil
import tempfile
from nxtomomill.io.config import HDF5Config, generate_default_h5_config
from nxtomomill import settings
import os


class TestH5Config(unittest.TestCase):
    """
    Test the HDF5Config class
    """

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_generate_default_config(self):
        """
        Insure we can generate a default configuration
        """
        config = HDF5Config()
        config.input_file = "toto.h5"
        config.output_file = "toto.nx"
        output = config.to_dict()

        self.assertEqual(type(output), dict)
        # check titles values
        titles_dict = output[HDF5Config.ENTRIES_AND_TITLES_SECTION_DK]
        self.assertEqual(
            titles_dict[HDF5Config.INIT_TITLES_DK], settings.H5_INIT_TITLES
        )
        self.assertEqual(
            titles_dict[HDF5Config.ZSERIE_INIT_TITLES_DK],
            settings.H5_ZSERIE_INIT_TITLES,
        )
        self.assertEqual(
            titles_dict[HDF5Config.PROJ_TITLES_DK], settings.H5_PROJ_TITLES
        )
        self.assertEqual(titles_dict[HDF5Config.REF_TITLES_DK], settings.H5_REF_TITLES)
        self.assertEqual(
            titles_dict[HDF5Config.DARK_TITLES_DK], settings.H5_DARK_TITLES
        )
        self.assertEqual(
            titles_dict[HDF5Config.ALIGNMENT_TITLES_DK], settings.H5_ALIGNMENT_TITLES
        )
        # check pixel size
        keys_dict = output[HDF5Config.KEYS_SECTION_DK]
        self.assertEqual(
            keys_dict[HDF5Config.X_PIXEL_SIZE_KEYS_DK], settings.H5_X_PIXEL_SIZE
        )
        self.assertEqual(
            keys_dict[HDF5Config.Y_PIXEL_SIZE_KEYS_DK], settings.H5_Y_PIXEL_SIZE
        )
        # check translation
        self.assertEqual(
            keys_dict[HDF5Config.X_TRANS_KEYS_DK], settings.H5_X_TRANS_KEYS
        )
        self.assertEqual(
            keys_dict[HDF5Config.Y_TRANS_KEYS_DK], settings.H5_Y_TRANS_KEYS
        )
        self.assertEqual(
            keys_dict[HDF5Config.Z_TRANS_KEYS_DK], settings.H5_Z_TRANS_KEYS
        )
        # others
        if settings.H5_VALID_CAMERA_NAMES is None:
            self.assertEqual(keys_dict[HDF5Config.VALID_CAMERA_DK], "")
        else:
            self.assertEqual(
                keys_dict[HDF5Config.VALID_CAMERA_DK], settings.H5_VALID_CAMERA_NAMES
            )
        self.assertEqual(keys_dict[HDF5Config.ROT_ANGLE_DK], settings.H5_ROT_ANGLE_KEYS)
        self.assertEqual(keys_dict[HDF5Config.DIODE_KEYS_DK], settings.H5_DIODE_KEYS)
        self.assertEqual(keys_dict[HDF5Config.Y_ROT_KEYS_DK], settings.H5_Y_ROT_KEY)
        self.assertEqual(
            keys_dict[HDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK],
            settings.H5_ACQ_EXPO_TIME_KEYS,
        )

        # check input and output file
        general_information = output[HDF5Config.GENERAL_SECTION_DK]
        self.assertEqual(general_information[HDF5Config.INPUT_FILE_DK], "toto.h5")
        self.assertEqual(general_information[HDF5Config.OUTPUT_FILE_DK], "toto.nx")

    def test_to_dict(self):
        """test the `to_dict` function"""
        config = HDF5Config()
        output_dict = config.to_dict()
        self.assertEqual(type(output_dict), dict)
        # check sections
        for section in (
            HDF5Config.GENERAL_SECTION_DK,
            HDF5Config.KEYS_SECTION_DK,
            HDF5Config.EXTRA_PARAMS_SECTION_DK,
            HDF5Config.FRAME_TYPE_SECTION_DK,
            HDF5Config.ENTRIES_AND_TITLES_SECTION_DK,
        ):
            with self.subTest(section=section):
                self.assertTrue(section in output_dict)
        # check titles keys
        for key in (
            HDF5Config.ALIGNMENT_TITLES_DK,
            HDF5Config.PROJ_TITLES_DK,
            HDF5Config.ZSERIE_INIT_TITLES_DK,
            HDF5Config.INIT_TITLES_DK,
            HDF5Config.REF_TITLES_DK,
            HDF5Config.DARK_TITLES_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(
                    key in output_dict[HDF5Config.ENTRIES_AND_TITLES_SECTION_DK]
                )
        # check pixel size
        for key in (HDF5Config.X_PIXEL_SIZE_KEYS_DK, HDF5Config.Y_PIXEL_SIZE_KEYS_DK):
            with self.subTest(key=key):
                self.assertTrue(key in output_dict[HDF5Config.KEYS_SECTION_DK])
        # translation keys
        for key in (
            HDF5Config.X_TRANS_KEYS_DK,
            HDF5Config.Y_TRANS_KEYS_DK,
            HDF5Config.Z_TRANS_KEYS_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(key in output_dict[HDF5Config.KEYS_SECTION_DK])
        # others
        for key in (
            HDF5Config.VALID_CAMERA_DK,
            HDF5Config.ROT_ANGLE_DK,
            HDF5Config.Y_ROT_KEYS_DK,
            HDF5Config.DIODE_KEYS_DK,
            HDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK,
        ):
            with self.subTest(key=key):
                self.assertTrue(key in output_dict[HDF5Config.KEYS_SECTION_DK])

    def test_from_dict(self):
        """test the `from_dict` function"""
        valid_camera_names = ("frelon", "totocam")
        alignment_titles = ("this is an alignment",)
        x_trans_keys = ("tx", "x")
        config = HDF5Config.from_dict(
            {
                HDF5Config.KEYS_SECTION_DK: {
                    HDF5Config.VALID_CAMERA_DK: valid_camera_names,
                    HDF5Config.X_TRANS_KEYS_DK: x_trans_keys,
                },
                HDF5Config.ENTRIES_AND_TITLES_SECTION_DK: {
                    HDF5Config.ALIGNMENT_TITLES_DK: alignment_titles,
                },
            }
        )
        self.assertEqual(config.valid_camera_names, valid_camera_names)
        self.assertEqual(config.alignment_titles, alignment_titles)
        self.assertEqual(config.x_trans_keys, x_trans_keys)

    def test_raises_errors(self):
        """
        Insure a type error is raised if an invalid type is passed to the
        HDF5Config class
        :return:
        """
        with self.assertRaises(TypeError):
            HDF5Config.from_dict(
                {
                    HDF5Config.ENTRIES_AND_TITLES_SECTION_DK: {
                        HDF5Config.DARK_TITLES_DK: 1213,
                    }
                }
            )

    def test_to_and_from_cfg_file(self):
        """
        Insure we can dump the configuration to a .cfg file and that we
        can read it back
        """
        file_path = os.path.join(self.folder, "output_file.cfg")
        input_config = HDF5Config()
        input_config.to_cfg_file(file_path)
        self.assertTrue(os.path.exists(file_path))
        loaded_config = HDF5Config.from_cfg_file(file_path=file_path)
        self.assertTrue(isinstance(loaded_config, HDF5Config))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestH5Config,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
