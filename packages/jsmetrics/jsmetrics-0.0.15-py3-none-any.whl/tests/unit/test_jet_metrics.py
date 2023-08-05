# -*- coding: utf-8 -*-

"""
    Tests for jet metrics (jetstream_metrics.py & jetstream_metrics_utils)
    Includes:
        – tests for each metric defined and expected outputs
        – test for each utility function used in the metric
"""

# imports
import unittest
from parameterized import parameterized
import xarray as xr
import numpy as np
from jsmetrics import (
    details_for_all_metrics,
    jetstream_metrics,
    jetstream_metrics_components,
)
from . import (
    set_up_test_uv_data,
    set_up_test_u_data,
    set_up_test_zg_data,
    set_up_nan_dataset,
)


# docs
__author__ = "Thomas Keel"
__email__ = "thomas.keel.18@ucl.ac.uk"
__status__ = "Development"


MAX_VARIABLES = 7


class TestMetricDetailsDict(unittest.TestCase):
    def setUp(self):
        self.metric_details = details_for_all_metrics.METRIC_DETAILS

    def test_metric_dict_keys(self):
        for metric_name in self.metric_details.keys():
            self.assertIsInstance(metric_name, str)

    def test_metric_dict_values(self):
        for metric in self.metric_details.values():
            self.assertIsInstance(metric, dict)
            self.assertEqual(len(metric.keys()), MAX_VARIABLES)
            self.assertListEqual(
                list(metric.keys()),
                [
                    "variables",
                    "coords",
                    "plev_units",
                    "metric",
                    "name",
                    "description",
                    "doi",
                ],
            )

    def test_variables(self):
        for metric in self.metric_details.values():
            self.assertIsInstance(metric["variables"], list)
            self.assertGreaterEqual(len(metric["variables"]), 0)
            self.assertLessEqual(len(metric["variables"]), MAX_VARIABLES)

    def test_metric_coords(self):
        for metric in self.metric_details.values():
            self.assertIsInstance(metric["coords"], dict)
            for coord in metric["coords"].keys():
                self.assertIsInstance(coord, str)

    @parameterized.expand(
        [
            ("plev", 0, 100000),
            ("lat", -91, 91),
            ("lon", -1, 361),
        ]
    )
    def test_each_coord(self, coord, min_value, max_value):
        for metric in self.metric_details.values():
            if coord in metric["coords"].keys():
                self.assertEqual(len(metric["coords"][coord]), 2)
                self.assertGreaterEqual(min(metric["coords"][coord]), min_value)
                self.assertLessEqual(max(metric["coords"][coord]), max_value)

    def test_funcs(self):
        for metric in self.metric_details.values():
            self.assertTrue(callable(metric["metric"]))


class TestArcherCaldeira2008(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_uv_data()

    def test_metric(self):
        result = jetstream_metrics.archer_caldeira_2008(self.data)
        for col in [
            "mass_weighted_average_ws",
            "mass_flux_weighted_pressure",
            "mass_flux_weighted_latitude",
        ]:
            self.assertIn(col, result)
            # self.assertEqual(10, result[col].max())

        self.assertEqual(
            float(result["mass_weighted_average_ws"].max()), 23.904821395874023
        )

    def test_get_mass_weighted_average_windspeed(self):
        tested_func = jetstream_metrics.archer_caldeira_2008
        test_data = self.data.isel(plev=1)
        # should fail because needs two plevs
        self.assertRaises(ValueError, lambda: tested_func(test_data))


class TestWoollings2010(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()
        # self.data = make_fake_seasonal_data(self.data)
        self.test_sig = self._get_test_sig()

    @staticmethod
    def _get_test_sig():
        # Seed the random number generator
        np.random.seed(42)
        time_step = 0.25
        period = 5.0
        time_vec = np.arange(0, 5, time_step)
        test_sig = np.sin(2 * np.pi / period * time_vec) + 0.5 * np.random.randn(
            time_vec.size
        )
        return test_sig

    def test_metric(self):
        tested_func = jetstream_metrics.woollings_et_al_2010
        result = tested_func(self.data, filter_freq=1, window_size=2)
        self.assertIsInstance(result, xr.Dataset)
        self.assertEqual(result["ff_jet_lat"][0], 36.25)
        self.assertEqual(result["ff_jet_speed"][0], 43.365413665771484)
        tested_func(self.data["ua"], filter_freq=1, window_size=2)

    def test_apply_lancoz_filter(self):
        tested_func = jetstream_metrics_components.apply_lanczos_filter
        test_ua = self.data["ua"]
        self.assertRaises(AssertionError, lambda: tested_func(self.data, 2, 4))
        self.assertRaises(AssertionError, lambda: tested_func(test_ua, -2, 1))
        self.assertRaises(ValueError, lambda: tested_func(test_ua, 2, -1))
        self.assertRaises(ValueError, lambda: tested_func(test_ua, 2, 1))
        self.assertRaises(
            ValueError,
            lambda: tested_func(test_ua, test_ua["time"].count() + 2, 1),
        )
        self.assertRaises(
            ValueError,
            lambda: tested_func(test_ua, 2, test_ua["time"].count() + 1),
        )
        self.assertEqual(float(tested_func(test_ua, 2, 4).max()), 99.514892578125)

    def test_get_latitude_and_speed_where_max_ws(self):
        tested_func = jetstream_metrics_components.get_latitude_and_speed_where_max_ws
        self.assertRaises(AttributeError, lambda: tested_func(["lol"]))
        tested_data = self.data["ua"].isel(plev=0, lon=0, time=0)
        self.assertEqual(tested_func(tested_data)[0], 81.25)
        self.assertEqual(tested_func(tested_data)[1], -9.87109375)
        self.assertRaises(
            KeyError, lambda: tested_func(tested_data.rename({"lat": "lt"}))
        )
        nan_dataset = set_up_nan_dataset()
        self.assertEqual(tested_func(nan_dataset), (np.nan, np.nan))

    def test_apply_fourier_filter(self):
        tested_func = jetstream_metrics_components.apply_low_freq_fourier_filter
        res = tested_func(self.test_sig, 2)
        self.assertAlmostEqual(res[10].real, -0.0956296962962675, places=7)


class TestBarnesPolvani2013(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()

    def test_metric(self):
        result = jetstream_metrics.barnes_polvani_2013(
            self.data, filter_freq=1, window_size=2
        )
        self.assertIsInstance(result, xr.Dataset)
        self.assertEqual(result["jet_lat"][1], 35.85)
        self.assertEqual(round(float(result["jet_speed"][2]), 5), 33.1134)
        self.assertEqual(float(result["jet_width"][1]), 17.5)

    def test_calc_jet_width_for_one_day(self):
        test_func = jetstream_metrics_components.calc_jet_width_for_one_day
        self.assertTrue(
            np.isnan(test_func(self.data["ua"].isel(time=0, plev=0), 25, None))
        )
        self.assertTrue(
            np.isnan(
                test_func(
                    self.data["ua"].isel(time=0, plev=0, lon=0, lat=slice(2, 5)),
                    0,
                    1,
                )
            )
        )

    def test_get_3_latitudes_and_speed_around_max_ws(self):
        test_func = jetstream_metrics_components.get_3_latitudes_and_speed_around_max_ws
        test_data = self.data["ua"].isel(time=0, plev=0, lat=slice(0, 2))
        res = test_func(test_data["lat"])
        self.assertEqual(len(res[0]), 3)
        self.assertTrue(np.isnan(res[0][-1]))
        test_data = self.data["ua"].isel(time=0, plev=0, lat=slice(68, 73))
        res = test_func(test_data["lat"])
        self.assertEqual(len(res[0]), 3)
        self.assertTrue(np.isnan(res[0][-1]))

    def test_get_3_neighbouring_coord_values(self):
        test_func = jetstream_metrics_components.get_3_neighbouring_coord_values
        res = test_func(45, 1)
        self.assertEqual(list(res), [44.0, 45.0, 46.0])


class TestScreenSimmonds2013(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_zg_data()

    def test_metric(self):
        # result = jetstream_metrics.screen_and_simmonds_2013(self.data)
        pass


class TestBarnesPolvani2015(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()

    def test_metric(self):
        result = jetstream_metrics.barnes_polvani_2015(self.data)
        self.assertEqual(float(result["jet_lat"].mean()), 43.25)
        self.assertEqual(round(float(result["jet_speed"].max()), 5), 14.31842)
        self.assertEqual(round(float(result["jet_speed"].min()), 5), 13.52321)


class TestFrancisVavrus2015(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_uv_data()

    def test_metric(self):
        result = jetstream_metrics.francis_vavrus_2015(self.data)
        self.assertEqual(float(result["mci"].mean()), -0.01847001537680626)
        self.assertTrue(result["mci"].max() == 1)
        self.assertTrue(result["mci"].min() == -1)


# class TestLocalWaveActivity(unittest.TestCase):
#     def setUp(self):
#         self.data = set_up_test_zg_data()

#     def test_metric(self):
#         result = jetstream_metrics.local_wave_activity(self.data)
#         self.assertTrue(result)


class TestCattiaux2016(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_zg_data()

    def test_metric(self):
        tested_func = jetstream_metrics.cattiaux_et_al_2016
        subset_data = self.data.isel(plev=0)
        res = tested_func(subset_data)
        tested_func(subset_data["zg"])
        self.assertEqual(round(float(res["sinuosity"].max()), 3), 2.749)


class TestBarnesSimpson2017(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()

    def test_metric(self):
        test_func = jetstream_metrics.barnes_simpson_2017
        result = test_func(self.data)
        self.assertEqual(round(float(result["jet_lat"].mean()), 5), 42.79215)
        self.assertEqual(round(float(result["jet_speed"].max()), 5), 86.99976)


class TestGrisePolvani2017(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()

    def test_metric(self):
        result = jetstream_metrics.grise_polvani_2017(self.data)
        jetstream_metrics.grise_polvani_2017(self.data["ua"])
        self.assertEqual(float(result["jet_lat"].min()), 35.38)
        self.assertEqual(float(result["jet_lat"].max()), 36.41)
        self.assertEqual(round(float(result["jet_speed"].max()), 5), 22.92644)


class TestCeppi2018(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()

    def test_metric(self):
        result = jetstream_metrics.ceppi_et_al_2018(self.data)
        print(result)
        self.assertEqual(float(result["jet_lat"][0].data), 37.316638365674194)


class TestBracegirdle2018(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_u_data()

    def test_metric(self):
        tested_func = jetstream_metrics.bracegirdle_et_al_2018
        test_data = self.data.sel(plev=slice(85000, 85000))
        result = tested_func(test_data)
        tested_func(test_data["ua"])
        # self.assertRaises(ValueError, lambda: tested_func(self.data))
        self.assertEqual(float(result["seasonal_JPOS"].max()), 37.725)
        self.assertEqual(float(result["annual_JPOS"].max()), 37.725)
        self.assertEqual(round(float(result["seasonal_JSTR"].max()), 3), 8.589)
        self.assertEqual(round(float(result["annual_JSTR"].max()), 3), 8.589)


class TestKerr2020(unittest.TestCase):
    def setUp(self):
        self.data = set_up_test_uv_data()

    def test_metric(self):
        tested_func = jetstream_metrics.kerr_et_al_2020
        # Should raise index error as takes only one plev
        self.assertRaises(IndexError, lambda: tested_func(self.data))
        test_data = self.data.sel(plev=50000)
        result = tested_func(test_data)
        self.assertEqual(result["jet_lat_by_lon"].isel(time=0).dropna("lon").size, 192)
        self.assertEqual(float(result["jet_lat_by_lon"].max()), 72.5)
        self.assertEqual(float(result["smoothed_jet_lats"].max()), 65.0)
        self.assertEqual(
            result["smoothed_jet_lats"].isel(time=0).dropna("lon").size, 61
        )


if __name__ == "__main__":
    unittest.main()
