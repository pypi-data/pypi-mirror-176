import unittest
from time import perf_counter

import numpy as np

import temporalvector.temporal_vector as tv
import temporalvector.temporal_enums as tve


class TestTemporalVector(unittest.TestCase):

    def setUp(self) -> None:
        self.tic = perf_counter()
        self.vector_cumulative_hour = tv.TemporalVector(100,
                                                        tve.VectorTimescales.Hour,
                                                        tve.VectorTimescales.Hour,
                                                        tve.VectorAggregations.Cumulative, 1)

        self.vector_cumulative_day = tv.TemporalVector(100,
                                                       tve.VectorTimescales.Day,
                                                       tve.VectorTimescales.Hour,
                                                       tve.VectorAggregations.Cumulative, 24)

    def tearDown(self) -> None:
        toc = '%.4f' % ((perf_counter() - self.tic) * 1000)
        toc = toc.rjust(8, ' ')
        message = self._testMethodName
        message = message.ljust(50, '.')
        print(f'{message} in {toc} milliseconds')

    def test_tv_update_by_index(self) -> None:
        start = 5
        end = 7
        length = 2

        self.vector_cumulative_hour.update_by_index(start_index=start, end_index=end, value=2,
                                                    timescale=tve.VectorTimescales.Hour)
        self.vector_cumulative_hour.update_by_index(start_index=start + 10, length=length, value=2,
                                                    timescale=tve.VectorTimescales.Hour)
        self.vector_cumulative_hour.update_by_index(end_index=end + 20, length=length, value=2,
                                                    timescale=tve.VectorTimescales.Hour)

        expected = np.array([1, 2, 2, 1])

        vector = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)

        actual_startend = vector[start - 1:end + 1]  # need 4 so 4,5,6,7 (stops before 7+1 = 8)
        actual_startlength = vector[start + 9:start + 13]  # need 4 so 14, 15, 16, 17 (stops before 5 + 13 = 18)
        actual_endlength = vector[end - 3:end + 1]  # need 4 so 24,25,26,27 (stops before 27+1 = 28)

        self.assertEqual(np.array_equal(expected, actual_startend), True, 'Index update does not match-startend')
        self.assertEqual(np.array_equal(expected, actual_startlength), True, 'Index update does not match-startlength')
        self.assertEqual(np.array_equal(expected, actual_endlength), True, 'Index update does not match-endlength ')

        # incorrect timescale
        self.assertRaises(TypeError,
                          self.vector_cumulative_hour.update_by_index,
                          start_index=start, end_index=end, value=2, timescale=tve.VectorTimescales.Day)

        # value not passed
        self.assertRaises(ValueError,
                          self.vector_cumulative_hour.update_by_index,
                          start_index=start, end_index=end, timescale=tve.VectorTimescales.Hour)

        # not enough index data passed
        self.assertRaises(ValueError,
                          self.vector_cumulative_hour.update_by_index,
                          start_index=start, timescale=tve.VectorTimescales.Hour)

        # incorrect value type
        self.assertRaises(TypeError,
                          self.vector_cumulative_hour.update_by_index,
                          start_index=2.5, end_index=end, value=2, timescale=tve.VectorTimescales.Hour)

        # incorrect value type
        self.assertRaises(TypeError,
                          self.vector_cumulative_hour.update_by_index,
                          start_index=5, end_index=2, value=2, timescale=tve.VectorTimescales.Hour)

    def test_tv_update_bulk(self) -> None:
        update_list = [[1, 6, 10], [20, 25, 25]]

        self.vector_cumulative_day.update_bulk(update_list, tve.VectorTimescales.Hour)
        comparison_1 = np.array([1, 10, 10, 10, 10, 10, 1])
        comparison_2 = np.array([1, 25, 25, 25, 25, 25, 1])

        vector = self.vector_cumulative_day.get(tve.VectorTimescales.Hour)

        self.assertEqual(np.array_equal(comparison_1, vector[0:7]), True, 'Comparison failed')
        self.assertEqual(np.array_equal(comparison_2, vector[19:26]), True, 'Comparison failed')

        # incorrect timescale
        self.assertRaises(TypeError, self.vector_cumulative_day.update_bulk,
                          update_list=update_list,
                          timescale=tve.VectorTimescales.Day)

        # incorrect values in update matrix with text
        bad_update_list = [[1, 6, 'apples'], [20, 25, 25]]

        self.assertRaises(TypeError,
                          self.vector_cumulative_day.update_bulk,
                          bad_update_list,
                          tve.VectorTimescales.Hour)

        # incorrect values in update matrix with bad end index
        bad_update_list = [[1, 6, 2], [20, 19, 25]]

        self.assertRaises(IndexError, self.vector_cumulative_day.update_bulk,
                          bad_update_list,
                          tve.VectorTimescales.Hour)

    def test_tv_vector_zero(self) -> None:
        self.vector_cumulative_hour.zero()
        should_be_zero = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)
        length = len(should_be_zero)
        comparison_vector = np.zeros(length)

        self.assertEqual(np.array_equal(should_be_zero, comparison_vector), True, 'Vector should be zero')

    def test_tv_vector_add(self) -> None:
        array_to_add = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)
        checksum_of_array_to_add = np.sum(array_to_add, axis=0)

        # this adds the two vectors together, and we don't need to result to generate the errors
        # since it's added internally, we can call the get_vector to get the new added vector
        self.vector_cumulative_hour.add(array_to_add)
        checksum_of_added_array = np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0)

        self.assertEqual(checksum_of_added_array, checksum_of_array_to_add * 2,
                         'Vector array should be added but is not')

        self.assertRaises(KeyError, self.vector_cumulative_hour.add,
                          array_to_add[2:])

        list_to_add = list(array_to_add)
        self.vector_cumulative_hour.add(list_to_add)
        checksum_of_added_list = np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0)
        self.assertEqual(checksum_of_added_list, checksum_of_array_to_add * 3, 'Vector list should be added but is not')

    def test_tv_vector_subtract(self) -> None:

        # only checking single value since all other arithmetic functions are tested with similar code.
        value_to_subtract = 0.5

        expected_checksum = np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0) / 2
        self.vector_cumulative_hour.subtract(value_to_subtract)

        actual_checksum = np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0)

        self.assertEqual(expected_checksum, actual_checksum, 'Vector should be subtracted')

    def test_tv_vector_multiply(self) -> None:
        operand = 3
        operand_array = np.array([operand] * self.vector_cumulative_hour.length(tve.VectorTimescales.Hour))

        # multiply by array
        source = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)
        source_operand_checksum = np.sum(source, axis=0) * operand

        # this multiplies the two vectors together, and we don't need to result to generate the errors
        # since it's added internally, we can call the get_vector to get the new added vector
        self.vector_cumulative_hour.multiply(operand_array)
        checksum_of_added_array = np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0)

        self.assertEqual(checksum_of_added_array, source_operand_checksum,
                         'Vector array should be multiplied but is not')

        # multiply by single value
        source = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)
        source_operand_checksum = np.sum(source, axis=0) * operand

        # this multiplies the two vectors together, and we don't need to result to generate the errors
        # since it's added internally, we can call the get_vector to get the new added vector
        self.vector_cumulative_hour.multiply(operand)
        checksum_of_added_array = np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0)

        self.assertEqual(checksum_of_added_array, source_operand_checksum,
                         'Vector array should be multiplied but is not')

    def test_tv_vector_divide(self) -> None:
        operand = 3
        operand_array = np.array([operand] * self.vector_cumulative_hour.length(tve.VectorTimescales.Hour))

        # multiply by array
        source = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)
        source_operand_checksum = float(np.sum(source, axis=0) / operand)

        # this multiplies the two vectors together, and we don't need to result to generate the errors
        # since it's added internally, we can call the get_vector to get the new added vector
        self.vector_cumulative_hour.divide(operand_array)
        checksum_of_added_array = float(np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0))

        self.assertAlmostEqual(checksum_of_added_array, source_operand_checksum, 4,
                               'Vector array should be multiplied but is not')

        # multiply by single value
        source = self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)
        source_operand_checksum = float(np.sum(source, axis=0) / operand)

        # this multiplies the two vectors together, and we don't need to result to generate the errors
        # since it's added internally, we can call the get_vector to get the new added vector
        self.vector_cumulative_hour.divide(operand)
        checksum_of_added_array = float(np.sum(self.vector_cumulative_hour.get(tve.VectorTimescales.Hour), axis=0))

        self.assertAlmostEqual(checksum_of_added_array, source_operand_checksum, 4,
                               'Vector array should be multiplied but is not')

    def test_tv_vector_write_list(self) -> None:
        # trying np.array write
        length = self.vector_cumulative_hour.length(tve.VectorTimescales.Hour)
        replacement_vector = np.array([2] * length)

        self.vector_cumulative_hour.write_entire_array(replacement_vector)

        self.assertEqual(np.array_equal(replacement_vector,
                                        self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)), True,
                         'Vector should be updated correctly with np.array')

        replacement_vector = [2] * length
        self.vector_cumulative_hour.write_entire_array(replacement_vector)
        self.assertEqual(np.array_equal(replacement_vector,
                                        self.vector_cumulative_hour.get(tve.VectorTimescales.Hour)), True,
                         'Vector should be updated correctly with list')

        incorrect_vector = [2] * (length - 2)

        self.assertRaises(TypeError, self.vector_cumulative_hour.write_entire_array,
                          vector=incorrect_vector)

        self.assertRaises(TypeError, self.vector_cumulative_hour.write_entire_array,
                          vector='apples')

        # Trying Temporal Vector for mass write
        new_vector = tv.TemporalVector(100,
                                       tve.VectorTimescales.Hour,
                                       tve.VectorTimescales.Hour,
                                       tve.VectorAggregations.Cumulative, 0.5)

        self.vector_cumulative_hour.write_entire_array(new_vector)

        self.assertEqual(np.array_equal(new_vector.get(tve.VectorTimescales.Hour),
                                        self.vector_cumulative_hour.get(tve.VectorTimescales.Hour))
                         , True, 'Vector should be updated correctly with temporal vector')

    def test_tv_get_vector_cumulative(self) -> None:
        cumulative_vector = self.vector_cumulative_day.get_cumulative(tve.VectorTimescales.Hour)

        test_list = np.array(cumulative_vector[0:10])
        comparison_vector = np.cumsum([1] * 10)

        self.assertEqual(np.array_equal(test_list, comparison_vector), True, 'Vector should be equal')

    def test_tv_get_vector(self) -> None:
        comparison_vector = np.array([1] * self.vector_cumulative_day.length(tve.VectorTimescales.Hour))
        actual_vector = np.array(
                [round(x, 2) for x in self.vector_cumulative_day.get(tve.VectorTimescales.Hour)])
        self.assertEqual(np.array_equal(comparison_vector, actual_vector), True, 'Get_vector not returned correctly')

        self.assertRaises(TypeError, self.vector_cumulative_day.get, target_timescale=None)

    def test_tv_length(self) -> None:
        expected_length = 100 * (tve.VectorTimescales.Day / tve.VectorTimescales.Hour)

        self.assertEqual(self.vector_cumulative_day.length(tve.VectorTimescales.Hour), expected_length,
                         'Length check failed')

        # length with conversion
        expected_length = expected_length / 24

        self.assertEqual(self.vector_cumulative_day.length(tve.VectorTimescales.Day), expected_length,
                         'Length check failed')
