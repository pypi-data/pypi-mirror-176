# Advanced Simulation: Temporal Vector

## Description

This package was created to support Monte Carlo simulations that require 1-D numerical value vectors of data 
across time.  The vectors are time-aware, and can be expanded or condensed to different time periods using different
aggregation methods (max, min, cumulative).  Update methods are provided to write the entire vector, update a 
specific range, or pass a list of index, range, value lines.  Methods to add, multiply, and divide vectors are provided.
For speed, the underlying vector is based on Numpy.  

This is used to abstract the underlying vector functionality to make the simulation code simpler.


## Getting Started

Download links:

HTTPS clone URL: https://github.com/crmckay55/sim_pkg_temporal_vector.git

pip install temporalvector


## How to use this package

### Instantiating and using a vector:
```python
import temporalvector.temporal_vector as tv
import temporalvector.temporal_enums as tve

# Create a vector with 1 day of duration, stored in hourly format, 
# with cumulative aggregation, 1 default value.  Further calls must recognize base vector is in Hour format
v = tv.TemporalVector(1, 
                      tve.VectorTimescales.Day, tve.VectorTimescales.Hour, 
                      tve.VectorAggregations.Cumulative, 1)

# this makes a numpy array of length 24, value of 1 

# retrieve the numpy vector values in days, and hours of duration (cumulative)
v_days = v.get(tve.VectorTimescales.Day)  # returns numpy array of length 1, value 24 (because cumulative aggregation)
v_hours = v.get(tve.VectorTimescales.Hour) # returns numpy array of length 24, value 1

# update the vector for the first 12 hours (index 0 to 11), so now half zeroes, half 1's
v.update_by_index(start_index=0, end_index=12, value=0, timescale=tve.VectorTimescales.Hour)

length = v.length(tve.VectorTimescales.Hour)

# update list to make first 12 hours 1, last 12 hour 0
bulk_update = [[0, 12, 1], [12, length - 1, 0]]
v.update_bulk(bulk_update, tve.VectorTimescales.Hour)

# Should return cumulative vector [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
v_cumulative = v.get_cumulative(tve.VectorTimescales.Hour)

```

Other VectorAggregations include Minimum and Maximum, if you want only the minimum and maximum values when 
updating the timescale on a vector.


### Other functions

Multiply, divide, add, and subtract a vector.  I didn't use overloading at this time because the functions are meant
to be an in-place operation.  Functions can accept a list, another TemporalVector, or a single value.