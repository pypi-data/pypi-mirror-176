##########################################################################################
# Temporal Vector
##########################################################################################
# Vector array of data that is temporally scalable, updatable by index or in bulk,
# can be zeroed, cumulative summed.
##########################################################################################
# Author: Chris McKay
# Version: 2.0
# Email: crmckay55@gmail.com
##########################################################################################
import numpy as np

import temporalvector.temporal_enums as tve


class TemporalVector:

    def __init__(self, duration: int,
                 duration_timescale: tve.VectorTimescales,
                 baseline_timescale: tve.VectorTimescales,
                 aggregation: tve.VectorAggregations,
                 default_value: float = 0):
        """
        Temporal vector that is scalable to different timeframes found in temporal_enums.
        :param duration: Integer duration of VectorTimescale type
        :param duration_timescale: timescale type of duration passed
        :param baseline_timescale: baseline timescale type (will be set for life of instance, vector in this timescale)
        :param aggregation: Aggregation type of the vector
        :param default_value: optional default value, otherwise 0 is used.
        """

        initial_vector = np.array([default_value] * duration)
        self.__vector = tve.VectorAggregations.aggregate(aggregation, initial_vector,
                                                         duration_timescale, baseline_timescale)
        self.__base_timescale = baseline_timescale
        self.__base_aggregation = aggregation

    def update_by_index(self, start_index: int = 0, end_index: int = 0, length: int = 0,
                        value=None, timescale: tve.VectorTimescales = None) -> None:
        """
        Updates a value, or series of values, in the vector. end_index and length are optional, but at least one
        of the two must be specified.  Indices beyond the length of the vector will be ignored
        :param start_index: Required: start index of the change (inclusive)
        :param end_index: Optional: end index of the change (inclusive)
        :param length: Optional: number of elements to update inclusive of start and end index
        :param value: element value
        :param timescale: Explicit call - must be hourly for now
        :return: None
        """

        # guard clauses to ensure valid parameters
        # if units do not match configured unit raise error.  Must be provided to ensure positive ID
        if (not end_index and not length) or (not start_index and not length) or (not start_index and not end_index):
            message = f"update_vector: Values of {start_index}, {end_index}, or {length} are not valid"
            raise ValueError(message)

        if timescale is not self.__base_timescale:
            message = f"update_vector: Units of {timescale} do not match {self.__base_timescale}"
            raise TypeError(message)

        if value is None:
            message = "update_vector: No value was provided"
            raise ValueError(message)

        # make the end index for use
        if start_index and length:
            end_index = start_index + length
        elif end_index and length:
            start_index = end_index - length
        elif start_index and end_index:
            length = end_index - start_index

        value_is_valid = isinstance(value, (int, float))

        if all(isinstance(i, int) and i > 0 for i in [start_index, end_index, length]):
            indexes_are_valid = True
        else:
            indexes_are_valid = False

        if not (value_is_valid and indexes_are_valid):
            message = f"{value} or {start_index, end_index, length} " \
                      f"are not valid.  Vector indexes must be a number and positive, and value a number."
            raise TypeError(message)

        if end_index > len(self.__vector) - 1:
            ...
            # TODO: how to implement error or ??? when end_index is beyond end of configured array?
            # maybe just update to end and truncate update?
            # message = f'vector with length {len(self.__vector)} has request to change value at index {end_index})'

        else:
            self.__vector[start_index:end_index] = np.array([value] * length)

    def update_bulk(self, update_list, timescale: tve.VectorTimescales) -> None:
        """
        Update list must be list with elements in order: start_index, end_index, value.
        :param update_list: list of elements [start_index, end_index, value]
        :param timescale: explicit pass of timescale to be compared to instance base timescale
        :return: None
        """

        if timescale is not self.__base_timescale:
            message = 'mass_update_vector: you must provide a timescale time that matches'
            raise TypeError(message)

        if False in (all(isinstance(i, int) for i in x) for x in update_list):
            message = 'mass_update_vector: update_list must be a list of integers'
            raise TypeError(message)

        if not all(0 < s <= e and e > 0 for s, e, v in update_list):
            message = 'mass_update_vector: update_list must be a list of valid indices'
            raise IndexError(message)

        [self.update_by_index(start_index=s, end_index=e, value=v, timescale=timescale) for s, e, v, in update_list]

    def zero(self) -> None:
        """
        Reset the base vector to all zeros for the duration and timescale configured at declaration of class
        :return: None
        """
        self.__vector = np.zeros(len(self.__vector))

    def write_entire_array(self, vector) -> None:
        """
        Write a list, array, or TemporalVector directly to a vector if the length of the list is the same as the
        duration * timescale passed at declaration of class.
        :param vector: List, TemporalVector, or np array of equal length to declared original duration * timescale
        :return: None
        """

        vector_to_write = None

        if isinstance(vector, TemporalVector):
            vector: TemporalVector
            vector_to_write = np.array(vector.get(self.__base_timescale))

        elif isinstance(vector, np.ndarray):
            vector_to_write = vector

        elif isinstance(vector, list):
            vector_to_write = np.array(vector)

        if not isinstance(vector_to_write, np.ndarray):
            raise TypeError(f"Invalid type for vector: {type(vector)}")

        if len(self.__vector) != len(vector_to_write):
            raise TypeError(f'Vectors passed is length {len(vector_to_write)} '
                            f'but temporal vector is length{len(self.__vector)}')

        self.__vector = vector_to_write.copy()

    def get_cumulative(self, target_timescale: tve.VectorTimescales = None) -> np.array:
        """
        Performs cumulative sum on a vector of desired timescale, returning the vector.  If no timescale
        is specified, then the originally declared base timescale is used.
        :param target_timescale: If the cumulative sum should be aggregated to a different timescale, put it here
        :return: cumulative sum vector in timescale of choice
        """

        if not target_timescale:
            target_timescale = self.__base_timescale

        vector = self.get(target_timescale)
        c_sum = np.cumsum(vector, axis=0)

        return c_sum

    def get(self, target_timescale: tve.VectorTimescales = None) -> np.array:
        """
        Get the vector in the timescale of choice.
        :param target_timescale:  default is base timescale, but explicitly
        :return: vector aggregated (or condensed) to desired timescale
        """
        if not target_timescale:
            raise TypeError('Must pass timescale type explicitly')

        result = tve.VectorAggregations.aggregate(self.__base_aggregation, self.__vector.copy(),
                                                  self.__base_timescale, target_timescale)

        return np.array(result)

    def length(self, target_timescale: tve.VectorTimescales) -> int:
        """
        Returns the length of the vector in the specified target timescale.
        :param target_timescale: must provide explicit target timescale
        :return: integer of vector length
        """

        if target_timescale == self.__base_timescale:
            return len(self.__vector)  # faster to just return this if timescales are the same
        else:
            # otherwise we need to convert!
            result = tve.VectorAggregations.aggregate(self.__base_aggregation, self.__vector.copy(),
                                                      self.__base_timescale, target_timescale)
            return len(result)

    def add(self, operand) -> np.array:
        """
        Addition and handles TemporalVector, list, or single value.
        If a list or array, must be same length.  If TemporalVector, will be converted to same timescale.
        :param operand: temporal vector, or list of equal length to base timescale, to add
        :return: np array of summed vector
        """

        operand = self.__validate_operand(operand, self.__base_timescale)

        self.__vector = self.__vector + operand

        return self.__vector

    def subtract(self, operand) -> np.array:
        """
        Subtraction handles TemporalVector, list, or single value.
        If a list or array, must be same length.  If TemporalVector, will be converted to same timescale.
        :param operand: temporal vector, or list of equal length to base timescale, to subtract
        :return: np array of subtracted vector
        """

        operand = self.__validate_operand(operand, self.__base_timescale)

        self.__vector = self.__vector - operand

        return self.__vector

    def multiply(self, operand) -> np.array:
        """
        Multiplication handles TemporalVector, list, or single value.
        If a list or array, must be same length.  If TemporalVector, will be converted to same timescale.
        :param operand: temporal vector, or list of equal length to base timescale, to multiply
        :return: np array of multiplied vector
        """
        operand = self.__validate_operand(operand, self.__base_timescale)

        self.__vector = self.__vector * operand

        return self.__vector

    def divide(self, operand) -> np.array:
        """
        Division handles TemporalVector or list, or single value.
        If a list or array, must be same length.  If TemporalVector, will be converted to same timescale.
        :param operand: temporal vector, or list of equal length to base timescale, to divide
        :return: np array of divided vector
        """

        operand = self.__validate_operand(operand, self.__base_timescale)

        self.__vector = self.__vector / operand

        return self.__vector

    def __validate_operand(self, vector, timescale: tve.VectorTimescales = None) -> np.array:
        """
        Checks if vector is a TemporalVector or a list of equal length to base timescale.  Also converts
        passed list, temporal vector, or array to a numpy array
        :param vector: int, list, TemporalVector or numpy array
        :return: int or numpy array as the oprand
        """
        added_length_skip = False  # if int is passed, then skip checking length of vector
        added_length = None

        if isinstance(vector, TemporalVector):
            vector: TemporalVector
            vector_to_operate = vector.get(timescale)
            added_length = len(vector_to_operate)

        elif isinstance(vector, np.ndarray):
            vector_to_operate = vector
            added_length = len(vector)

        elif isinstance(vector, list):
            vector_to_operate = np.array(vector)
            added_length = len(vector)

        elif isinstance(vector, (int, float)):
            vector_to_operate = vector
            added_length_skip = True

        else:
            raise TypeError(f"Invalid type for vector: {type(vector)}")

        if self.length(self.__base_timescale) != added_length and not added_length_skip:
            raise KeyError('Vectors are not equal lengths. Temporal vectors must be equal length to add')

        return vector_to_operate
