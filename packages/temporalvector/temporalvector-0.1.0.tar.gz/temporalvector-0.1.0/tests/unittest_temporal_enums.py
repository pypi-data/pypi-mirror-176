import math
import unittest
from time import perf_counter

import numpy as np

import temporalvector.temporal_enums as tve


class TestTemporalVectorEnums(unittest.TestCase):

    def setUp(self) -> None:
        self.tic = perf_counter()
        self.minute_vector = np.array([1, 0] * 60)
        self.minute_vector_type = tve.VectorTimescales.Minute

        self.hour_vector = np.array([60, 0] * (12 * 365 * 12))
        self.hour_vector_type = tve.VectorTimescales.Hour

        self.year_vector = np.array([525_600] * 12)
        self.year_vector_type = tve.VectorTimescales.Year

    def tearDown(self) -> None:
        toc = '%.4f' % ((perf_counter() - self.tic) * 1000)
        toc = toc.rjust(8, ' ')
        message = self._testMethodName
        message = message.ljust(50, '.')
        print(f'{message} in {toc} milliseconds')

    def test_tve_cumulative_aggregation_down_cumulative1(self):
        # check minute to second
        frac, whole = math.modf(self.minute_vector_type / tve.VectorTimescales.Second)

        self.assertEqual(frac, 0, 'VectorTimescales have factors that are not divisible')

        expected_length = len(self.minute_vector) * whole
        expected_sum = float(np.sum(self.minute_vector))

        new_vector = tve.VectorAggregations.aggregate(tve.VectorAggregations.Cumulative,
                                                      self.minute_vector,
                                                      self.minute_vector_type,
                                                      tve.VectorTimescales.Second)

        self.assertEqual(expected_length, len(new_vector), 'Cumulative vector not expected length')
        self.assertAlmostEqual(expected_sum, float(np.sum(new_vector)), 1, 'Cumulative sum not as expected')

    def test_tve_cumulative_aggregation_down_cumulative2(self):
        # check hour to minute
        frac, whole = math.modf(self.hour_vector_type / tve.VectorTimescales.Minute)
        self.assertEqual(frac, 0, 'VectorTimescales have factors that are not divisible')

        expected_length = len(self.hour_vector) * whole
        expected_sum = float(np.sum(self.hour_vector))

        new_vector = tve.VectorAggregations.aggregate(tve.VectorAggregations.Cumulative,
                                                      self.hour_vector,
                                                      self.hour_vector_type,
                                                      tve.VectorTimescales.Minute)

        self.assertEqual(expected_length, len(new_vector), 'Cumulative vector not expected length')
        self.assertAlmostEqual(expected_sum, float(np.sum(new_vector)), 1, 'Cumulative sum not as expected')

    def test_tve_cumulative_aggregation_down_cumulative3(self):
        # check year to day
        frac, whole = math.modf(self.year_vector_type / tve.VectorTimescales.Day)
        self.assertEqual(frac, 0, 'VectorTimescales have factors that are not divisible')

        expected_length = len(self.year_vector) * whole
        expected_sum = float(np.sum(self.year_vector))

        new_vector = tve.VectorAggregations.aggregate(tve.VectorAggregations.Cumulative,
                                                      self.year_vector,
                                                      self.year_vector_type,
                                                      tve.VectorTimescales.Day)

        self.assertEqual(expected_length, len(new_vector), 'Cumulative vector not expected length')
        self.assertAlmostEqual(expected_sum, float(np.sum(new_vector)), 1, 'Cumulative sum not as expected')

    def test_tve_cumulative_aggregation_up_cumulative1(self):
        # check minute to hour
        frac, whole = math.modf(tve.VectorTimescales.Hour / self.minute_vector_type)

        self.assertEqual(frac, 0, 'VectorTimescales have factors that are not divisible')

        frac, whole = math.modf(len(self.minute_vector) / whole)
        expected_length = whole if frac == 0 else whole + 1
        expected_sum = np.sum(self.minute_vector)

        new_vector = tve.VectorAggregations.aggregate(tve.VectorAggregations.Cumulative,
                                                      self.minute_vector,
                                                      self.minute_vector_type,
                                                      tve.VectorTimescales.Hour)

        self.assertEqual(expected_length, len(new_vector), 'Cumulative vector not expected length')
        self.assertEqual(expected_sum, np.sum(new_vector), 'Cumulative sum not as expected')

    def test_tve_cumulative_aggregation_up_cumulative2(self):
        # check hour to year
        frac, whole = math.modf(tve.VectorTimescales.Year / self.hour_vector_type)

        self.assertEqual(frac, 0, 'VectorTimescales have factors that are not divisible')

        frac, whole = math.modf(len(self.hour_vector) / whole)
        expected_length = whole if frac == 0 else whole + 1
        expected_sum = np.sum(self.hour_vector)

        new_vector = tve.VectorAggregations.aggregate(tve.VectorAggregations.Cumulative,
                                                      self.hour_vector,
                                                      self.hour_vector_type,
                                                      tve.VectorTimescales.Year)

        self.assertEqual(expected_length, len(new_vector), 'Cumulative vector not expected length')
        self.assertEqual(expected_sum, np.sum(new_vector), 'Cumulative sum not as expected')

    def test_tve_aggregate_errors(self):
        bad_aggregation = 'apples'
        self.assertRaises(TypeError,
                          tve.VectorAggregations.aggregate,
                          bad_aggregation,
                          self.minute_vector,
                          self.minute_vector_type, tve.VectorTimescales.Hour)

    def test_tve_aggregation_min_up(self):
        correct_return_min = np.array([0, 0])

        returned_min_longer = tve.VectorAggregations.aggregate(tve.VectorAggregations.Minimum, self.minute_vector,
                                                               tve.VectorTimescales.Minute,
                                                               tve.VectorTimescales.Hour)

        self.assertEqual(np.array_equal(correct_return_min, returned_min_longer), True, 'Min aggregation not correct')

    def test_tve_aggregation_max_up(self):
        correct_return_max = np.array([1, 1])
        returned_max_longer = tve.VectorAggregations.aggregate(tve.VectorAggregations.Maximum, self.minute_vector,
                                                               tve.VectorTimescales.Minute,
                                                               tve.VectorTimescales.Hour)

        self.assertEqual(np.array_equal(correct_return_max, returned_max_longer), True, 'Max aggregation not correct')

    def test_tve_aggregation_min_down(self):
        correct_return_min = np.repeat(self.minute_vector, 60)

        returned_min_shorter = tve.VectorAggregations.aggregate(tve.VectorAggregations.Minimum, self.minute_vector,
                                                                tve.VectorTimescales.Minute,
                                                                tve.VectorTimescales.Second)

        self.assertEqual(np.array_equal(correct_return_min, returned_min_shorter), True, 'Min aggregation not correct')

    def test_tve_aggregation_max_down(self):
        correct_return_max = np.repeat(self.minute_vector, 60)

        returned_max_shorter = tve.VectorAggregations.aggregate(tve.VectorAggregations.Maximum, self.minute_vector,
                                                                tve.VectorTimescales.Minute,
                                                                tve.VectorTimescales.Second)

        self.assertEqual(np.array_equal(correct_return_max, returned_max_shorter), True, 'Max aggregation not correct')
