##########################################################################################
# Temporal Vector Enums and Functions
##########################################################################################
# TimeScale and Aggregation types for temporal vectors.  Allows scale up and down
# of vectors on a Cumulative, Max, or Min basis switching between timescales of second,
# minute, hour, day, and year.
##########################################################################################
# Author: Chris McKay
# Version: 2.0
# Email: crmckay55@gmail.com
##########################################################################################

import math

from enum import Enum
from enum import IntEnum

import numpy as np


class VectorTimescales(IntEnum):
    """
    Timescales values, using 1  second as the base.  Integers are scalar factors to convert between timescales.
    """
    Second = 1
    Minute = 60
    Hour = 3_600
    Day = 86_400
    # Week = 604_800 Not implemented because week and month don't convert cleanly b/w day and year
    # Month = ? Not implemented because week and month don't convert cleanly b/w day and year
    Year = 31_536_000  # assumed 365 days


class VectorAggregations(Enum):
    """
    Aggregation types for vectors, including the method to do the expansion or aggregation to different
    timescales
    """
    Cumulative = 'cumulative'
    Maximum = 'maximum'
    Minimum = 'minimum'

    def aggregate(self, vector: np.array,
                  original_timescale: VectorTimescales, new_timescale: VectorTimescales) -> np.array:
        """
        Aggregate (expand or contract) vector according to aggregation type, and timescale direction
        :param self: reference to aggregation enum selected
        :param vector: vector to modify
        :param original_timescale: timescale of passed vector
        :param new_timescale: timescale for new vector
        :return: vector in new timescale according to aggregation type
        """

        # determine if we're shrinking or lengthening the vector, and adjust vector if needed
        # shorter timeframe means new timescale is longer (shorter vector),
        # longer timeframe means new timescale is shorter (longer vector)

        if not isinstance(self, VectorAggregations):
            raise TypeError("Invalid aggregation type")

        # guard clause to return vector if both timescales are the same - faster than doing the math!
        if isinstance(vector, list):
            vector = np.array(vector)

        if new_timescale == original_timescale:
            return vector

        factor = new_timescale / original_timescale

        if factor > 1:
            vector = _reshape_to_timescale(vector, original_timescale, new_timescale)  # reshape to aggregate by row
            shorter_timeframe = False
        else:
            factor = int(1 / factor)
            shorter_timeframe = True

        result = []

        if self == VectorAggregations.Cumulative:
            if shorter_timeframe:
                # shorter timeframe = longer vector = divide each element by the factor and repeat it factor times
                # to turn the longer timeframe into shorter (e.g. 1 day = 24tons, to divided out is 1 ton 24 times)
                result = np.repeat(vector / factor, factor)

            else:
                result = np.sum(vector, axis=1)  # reshaped vector - sum each row

        # if not cumulative, the repeat if expanded, or max/min if shrunk
        elif shorter_timeframe:
            # if max, just repeat the element factor times
            # e.g. max or min of x in a day, is x per hour 24 times
            result = np.repeat(vector, factor)

        elif not shorter_timeframe:

            if self == VectorAggregations.Maximum:
                result = np.amax(vector, axis=1)  # reshaped vector, get the max in each row

            elif self == VectorAggregations.Minimum:
                result = np.amin(vector, axis=1)  # reshaped vector, get the max in each row

        return np.array(result)


def _reshape_to_timescale(vector,
                          original_timescale: VectorTimescales,
                          new_timescale: VectorTimescales) -> np.array:
    """
    Reshapes a vector to the desired timescale, including padding zeroes if needed for reshape
    :param vector: vector to reshape and rescale.
    :param original_timescale: enum of original timescale
    :param new_timescale: enum of desired timescale
    :return: reshaped list in new timescale
    """

    # pad zeroes first, to ensure that the vector will be divisible by the new timescale
    vector = np.append(vector, _pad_zeroes(len(vector), original_timescale, new_timescale))

    timescale_width = int(new_timescale / original_timescale)

    fraction_of_elements, number_of_elements = math.modf(len(vector) / timescale_width)

    if fraction_of_elements != 0:
        print('Vector has not been reshaped as a full multiple of the timescale!')
        raise ValueError

    reshaped_vector = np.reshape(vector,
                                 (int(number_of_elements),
                                  timescale_width))

    return reshaped_vector


def _pad_zeroes(current_length: int,
                current_timescale: VectorTimescales,
                new_timescale: VectorTimescales) -> np.array:
    """
    Returns a list of zeros to pad to a vector to make it a full multiple of selected VectorTimescale
    :param current_length: no need to pass whole vector, just the length
    :param new_timescale: Enum of desired timescale (VectorTimescales)
    :return: list of zeros to pad to original vector to scale to desired timescale
    """

    # no zeroes needed if we're condensing down to a shorter timescale
    if new_timescale < current_timescale:
        return []

    # the length of the vector must be divisible by new_timescale with no remainder.
    timescale_multiple = int(new_timescale / current_timescale)

    # get the frac piece so we can 1-frac to get proportion to pad
    frac, whole = math.modf(current_length / timescale_multiple)
    frac = 1 if frac == 0 else frac

    zeroes_to_pad = int(timescale_multiple * (1 - frac))

    return np.array([0] * zeroes_to_pad)
