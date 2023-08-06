# Copyright (c) 2020 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from shapelets.dsl.argument_types import ArgumentTypeEnum
from shapelets.dsl.graph import Node, NodeInputParamType, NodeReturnType


def c3(ts: NodeInputParamType, lag: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the Schreiber, T. and Schmitz, A. (1997) measure of non-linearity for the given time series
    :param ts: SEQUENCE
    :param lag: LONG
    :return output_0: DOUBLE
    """
    pass


def abs(number: NodeInputParamType) -> NodeReturnType:
    """
    Returns the absolute value of any given number
    :param number: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def div(dividend: NodeInputParamType, divisor: NodeInputParamType) -> NodeReturnType:
    """
    Returns the result of executing a division between two numbers.
    :param dividend: DOUBLE
    :param divisor: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def fft(ts: NodeInputParamType) -> NodeReturnType:
    """
    Fast Fourier Transform (FFT). 
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def max(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the largest of the two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def min(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the smallest of the two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def paa(ts: NodeInputParamType, bins: NodeInputParamType) -> NodeReturnType:
    """
    Piecewise Aggregate Approximation (PAA).
    :param ts: SEQUENCE
    :param bins: INT
    :return output_0: SEQUENCE
    """
    pass


def pow(base: NodeInputParamType, exp: NodeInputParamType) -> NodeReturnType:
    """
    Returns base to the power exp.
    :param base: DOUBLE
    :param exp: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def plus(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the sum of two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def minus(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the difference of two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def times(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the product of two expressions.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def abs_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series with absolute numeric value of each element.
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def div_ts(ts: NodeInputParamType, divisor: NodeInputParamType) -> NodeReturnType:
    """
    Divide each point of a time series by a divisor.
    :param ts: SEQUENCE
    :param divisor: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether two expressions are equal.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def length(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns the length of a time series.
    :param ts: SEQUENCE
    :return output_0: LONG
    """
    pass


def map_ts(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new Sequence resulting from applying the lambda function to each element of the input Sequence
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def pow_ts(ts: NodeInputParamType, exp: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from applying base to the power exp to each point of the given time series.
    :param ts: SEQUENCE
    :param exp: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def sbd_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the Shape-Based distance (SBD). It computes the normalized cross-correlation and it returns the value
    that maximizes the correlation value between time series.
    :param ts: LIST:SEQUENCE
    :return output: ND_ARRAY
    """
    pass


def z_norm(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates a new set of time series with zero mean and standard deviation one.
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def to_view(sequence_id: NodeInputParamType, index: NodeInputParamType,
            window_size: NodeInputParamType) -> NodeReturnType:
    """
    Returns a View from a given Sequence using the index and window size to calculate de View size. 
    :param sequence_id: STRING
    :param index: LONG
    :param window_size: LONG
    :return output_0: VIEW
    """
    pass


def k_means(ts_list: NodeInputParamType, k: NodeInputParamType, tolerance: NodeInputParamType,
            max_iterations: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the K-Means algorithm.
    :param ts_list: LIST:SEQUENCE
    :param k: INT
    :param tolerance: FLOAT
    :param max_iterations: INT
    :return output_0: LIST:ND_ARRAY
    """
    pass


def k_shape(ts_list: NodeInputParamType, k: NodeInputParamType, tolerance: NodeInputParamType,
            max_iterations: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the K-Shape algorithm.
    :param ts_list: LIST:SEQUENCE
    :param k: INT
    :param tolerance: FLOAT
    :param max_iterations: INT
    :return output: LIST:ND_ARRAY
    """
    pass


def plus_ts(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the addition of a given value to each point of a time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def mean_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the mean value for the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def range_ts(n: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series with n values.
    :param n: LONG
    :return output_0: SEQUENCE
    """
    pass


def kurtosis(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns the kurtosis of the given time series (calculated with the adjusted Fisher-Pearson standardized moment coefficient G2).
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def times_ts(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the product of a given value to each point of a time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def to_match(sequence_id: NodeInputParamType, index: NodeInputParamType, window_size: NodeInputParamType,
             correlation: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new Match from the input arguments
    :param sequence_id: STRING
    :param index: LONG
    :param window_size: LONG
    :param correlation: DOUBLE
    :return output_0: MATCH
    """
    pass


def minus_ts(ts: NodeInputParamType, number: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from subtracting each point of a time series by a given value.
    :param ts: SEQUENCE
    :param number: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def max_inter(array: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the maximum intersection for the given Array.
    :param array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def less_than(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is less than the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def min_inter(array: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the minimum intersection for the given Array.
    :param array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def remainder(dividend: NodeInputParamType, divisor: NodeInputParamType) -> NodeReturnType:
    """
    Returns the remainder of executing a division between two numbers.
    :param dividend: DOUBLE
    :param divisor: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def cid_ce_ts(ts: NodeInputParamType, z_normalize: NodeInputParamType) -> NodeReturnType:
    """
    Calculates an estimate for the time series complexity defined by Batista, Gustavo EAPA, et al (2014).
     (A more complex time series has more peaks, valleys, etc.)
    Param z_normalize: Controls whether the time series should be z-normalized or not.
    :param ts: SEQUENCE
    :param z_normalize: BOOLEAN
    :return output_0: DOUBLE
    """
    pass


def moment_ts(ts: NodeInputParamType, k: NodeInputParamType) -> NodeReturnType:
    """
    Returns the kth moment of the given time series.
    :param ts: SEQUENCE
    :param k: INT
    :return output_0: DOUBLE
    """
    pass


def reduce_ts(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns the result as Double of reducing all elements from the input Sequence with the given lambda function
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def median_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the median value for the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def to_double(num: NodeInputParamType) -> NodeReturnType:
    """
    Parses the given number as a Double number and returns the result.
    :param num: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def div_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Division of two time series. Time series must have the same length
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def concat_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Joins two time series along an existing axis.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def filter_ts(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new Sequence resulting from applying the predicate function to each element of the input Sequence.
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def not_equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether two number are not equal.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def reverse_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Reverses the points of the given time series.
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def uniques_ts(ts: NodeInputParamType, is_sorted: NodeInputParamType) -> NodeReturnType:
    """
    Finds unique values from an input time series
    :param ts: SEQUENCE
    :param is_sorted: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def trend_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Trend test for time series. Trends show the general tendency of the data to increase or decrease during a long period of time.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def mean_inter(array: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the mean intersection for the given Array.
    :param array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def abs_energy(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sum over the square values of the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def plus_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the addition of the two given time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def constant_ts(value: NodeInputParamType, rows: NodeInputParamType, start: NodeInputParamType,
                every: NodeInputParamType) -> NodeReturnType:
    """
    Generates a constant time series.
    :param value: DOUBLE
    :param rows: LONG
    :param start: LONG
    :param every: LONG
    :return output_0: SEQUENCE
    """
    pass


def variance_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Computes the variance for the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def convolve_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def mean_change(ts: NodeInputParamType) -> NodeReturnType:
    """
     Calculates the mean over the differences between subsequent time series values in the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def times_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the product of the two given time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def minus_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the difference of two time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def skewness_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sample skewness of the given time series (calculated with the adjusted Fisher-Pearson standardized
    moment coefficient G1).
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def conjugate_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns the conjugate time series.
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def less_than_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns an Array with Booleans stating whether the item of the first time series is less than the equivalent item
     of the second time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: ARRAY
    """
    pass


def greater_than(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is greater than the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def max_value_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the maximum value for the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def min_value_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the minimum value for the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def manhattan_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Calculates Manhattan distances between the given list of time series. Returns an Array with an upper triangular matrix where each position
    corresponds to the distance between two time series. Diagonal elements will be zero.
    :param ts_list: LIST:SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def euclidean_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates euclidean distances between time series.
    :param ts: LIST:SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def sample_stdev(ts: NodeInputParamType) -> NodeReturnType:
    """
    Estimates standard deviation based on a sample. The standard deviation is calculated using the "n-1" method.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def split_every_n(ts: NodeInputParamType, n: NodeInputParamType) -> NodeReturnType:
    """
    Splits any given sequence into new sequences of n points
    :param ts: SEQUENCE
    :param n: INT
    :return output_0: LIST:SEQUENCE
    """
    pass


def adfuller_test(tss: NodeInputParamType) -> NodeReturnType:
    """
    Augmented Dickey-Fuller test
    :param tss: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def sum_values_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sum over the time series values.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def contains_value(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a boolean based on whether a given value is contained within a time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def hann_window_ts(m: NodeInputParamType, start: NodeInputParamType, every: NodeInputParamType) -> NodeReturnType:
    """
    Return a time series with Hanning window of size m. The Hann window is a taper formed by using a raised cosine or sine-squared
     with ends that touch zero. Start and every params represent the index of the time series
    :param m: LONG
    :param start: LONG
    :param every: LONG
    :return output_0: SEQUENCE
    """
    pass


def fft_aggregated(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the spectral centroid(mean), variance, skew, and kurtosis of the absolute fourier transform spectrum.
    :param ts: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def binned_entropy(ts: NodeInputParamType, max_bins: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the binned entropy for the given time series and number of bins.
    :param ts: SEQUENCE
    :param max_bins: INT
    :return output_0: DOUBLE
    """
    pass


def visvalingam_ts(ts: NodeInputParamType, num_points: NodeInputParamType) -> NodeReturnType:
    """
    Reduces a time series by applying the Visvalingam method (minimun triangle area) until the number of points is reduced to num_points.
    :param ts: SEQUENCE
    :param num_points: INT
    :return output_0: SEQUENCE
    """
    pass


def decompose_view(view: NodeInputParamType) -> NodeReturnType:
    """
    Returns the elements of the given View: sequence ID, index and end. 
    :param view: VIEW
    :return sequence_id: STRING
    :return index: LONG
    :return end: LONG
    """
    pass


def local_maximals(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates all Local Maximals fot the given time series
    :param ts: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def get_row_single(ts: NodeInputParamType, at: NodeInputParamType) -> NodeReturnType:
    """
    Returns the index value from the given Sequence.
    :param ts: SEQUENCE
    :param at: LONG
    :return output_0: DOUBLE
    """
    pass


def matrix_profile(ts_1: NodeInputParamType, ts_2: NodeInputParamType,
                   subsequence_length: NodeInputParamType) -> NodeReturnType:
    """
    Calculate the matrix profile between two time series using a subsequence length.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :param subsequence_length: INT
    :return output_0: ARRAY
    """
    pass


def count_equals_ts(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Counts occurrences of value in the time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def ergodicity_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Ergodicity test
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def abs_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Returns an list of Sequences where with the absolute numeric value of each element of the given time series.
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:SEQUENCE
    """
    pass


def pattern_in_data(query: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the maximum correlation and the index of the best occurrence for a single query in a time series.
    :param query: SEQUENCE
    :param ts: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def greater_than_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns an Array of Booleans with the result of ts_1 > ts_2.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def fft_coefficient(ts: NodeInputParamType, coefficient: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the fourier coefficients of the one-dimensional discrete Fourier Transform for real input by fast fourier transformation algorithm.
    :param ts: SEQUENCE
    :param coefficient: LONG
    :return output_0: ND_ARRAY
    """
    pass


def filter_nd_array(functor: NodeInputParamType, nd_array: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new NDArray resulting from applying the predicate function to each element of the input NDArray
    :param functor: FUNCTION
    :param nd_array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def generate_levels(ts: NodeInputParamType, size_in_bytes: NodeInputParamType,
                    max_levels: NodeInputParamType) -> NodeReturnType:
    """
    Produces a nodes with as many elements as levels produced for the input sequence.
     The elements in the nodes indicates how many blocks each level has.
    :param ts: SEQUENCE
    :param size_in_bytes: LONG
    :param max_levels: INT
    :return output_0: LONG
    """
    pass


def count_above_mean(xss: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the number of values in the time series that are higher than the mean.
    :param xss: SEQUENCE
    :return output: DOUBLE
    """
    pass


def to_dense_regular(ts: NodeInputParamType) -> NodeReturnType:
    """
    Change time series density type to regular
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def count_below_mean(xss: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the number of values in the time series that are lower than the mean.
    :param xss: SEQUENCE
    :return output: DOUBLE
    """
    pass


def seasonality_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Seasonality test for time series.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def cwt_coefficients(ts: NodeInputParamType, widths: NodeInputParamType, coefficient_of_interest: NodeInputParamType,
                     width_of_interest: NodeInputParamType) -> NodeReturnType:
    """
    Calculates a Continuous wavelet transform for the Ricker wavelet, also known as the "Mexican hat wavelet".
    :param ts: SEQUENCE
    :param widths: ND_ARRAY
    :param coefficient_of_interest: INT
    :param width_of_interest: INT
    :return output_0: DOUBLE
    """
    pass


def periodicity_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Periodicity tests for time series.
    :param ts: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def has_duplicates_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns if the input time series contain duplicated elements.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def number_crossing_m(ts: NodeInputParamType, m: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the number of m-crossings. A m-crossing is defined as two sequential values where the first value is lower
    than m and the next is greater, or vice versa. If m is set to zero, the number of zero crossings will be returned.
    :param ts: SEQUENCE
    :param m: INT
    :return output_0: DOUBLE
    """
    pass


def hamming_distances(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Calculates Hamming distances between time series.
    :param ts_list: LIST:SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def auto_covariance_ts(ts: NodeInputParamType, unbiased: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the auto-covariance for the given time series.
    Param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :param ts: SEQUENCE
    :param unbiased: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def z_norm_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Calculates a new set of time series with zero mean and standard deviation one for every time series included in the given list.
    :param ts_list: LIST:SEQUENCE
    :return output_o: LIST:SEQUENCE
    """
    pass


def has_duplicates_max(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns if the maximum within input time series is duplicated.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def has_duplicates_min(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns if the minimum of the input time series is duplicated.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def pattern_self_match(ts: NodeInputParamType, begin: NodeInputParamType, end: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the maximum correlation and the index of the best occurrence for a set of queries in a time series.
    :param ts: SEQUENCE
    :param begin: LONG
    :param end: LONG
    :return output_0: LONG
    :return output_1: LONG
    :return output_2: DOUBLE
    """
    pass


def cross_covariance_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType,
                        unbiased: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the cross-covariance of the given time series.
    Param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :param unbiased: BOOLEAN
    :return output_0: DOUBLE
    """
    pass


def symmetry_looking_ts(ts: NodeInputParamType, range_percentage: NodeInputParamType) -> NodeReturnType:
    """
    Calculates if the distribution of the given time series looks symmetric. Requires a the percentage of the range to compare with.
    :param ts: SEQUENCE
    :param range_percentage: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def less_than_or_equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is less than or equal the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def auto_correlation_ts(ts: NodeInputParamType, maxLag: NodeInputParamType,
                        unbiased: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the autocorrelation of the specified lag for the given time series.
    :param ts: SEQUENCE
    :param maxLag: LONG
    :param unbiased: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def index_mass_quantile(ts: NodeInputParamType, quantile: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the index of the mass quantile.
    :param ts: SEQUENCE
    :param quantile: FLOAT
    :return output_0: DOUBLE
    """
    pass


def isax_representation(ts: NodeInputParamType, alphabet_size: NodeInputParamType) -> NodeReturnType:
    """
    iSAX Representation. This function should receive a time series which have suffered a z-normalization and a PAA to its z-normalization.
    :param ts: SEQUENCE
    :param alphabet_size: INT
    :return output_0: SEQUENCE
    """
    pass


def mean_absolute_change(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the mean over the absolute differences between subsequent time series values in the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def approximated_entropy(ts: NodeInputParamType, length: NodeInputParamType,
                         filtering_level: NodeInputParamType) -> NodeReturnType:
    """
    Calculates a vectorized Approximate entropy algorithm (https://en.wikipedia.org/wiki/Approximate_entropy)
    Requires a time series, the length of compared run of data and the filtering level (must be positive).
    :param ts: SEQUENCE
    :param length: INT
    :param filtering_level: FLOAT
    :return output_0: ND_ARRAY
    """
    pass


def cross_correlation_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType,
                         unbiased: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the cross-correlation of the given time series.
    Param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :param unbiased: BOOLEAN
    :return output_0: DOUBLE
    """
    pass


def squared_euclidean_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the non squared version of the euclidean distance.
    :param ts: LIST:SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def max_min_normalization(ts: NodeInputParamType, high: NodeInputParamType, low: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given time series according to its minimum and maximum value and adjusts each value within the range [low, high].
    :param ts: SEQUENCE
    :param high: DOUBLE
    :param low: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def mean_normalization_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given time series according to its maximum-minimum value and its mean. 
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def standard_deviation_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the standard deviation of the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def greater_than_or_equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is greater than or equal the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def energy_ratio_by_chunks(ts: NodeInputParamType, num_segments: NodeInputParamType,
                           segment_focus: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sum of squares of chunk i out of N chunks expressed as a ratio with the sum of squares over the whole series. 
    segment_focus should be lower than the number of segmentsCalculates the sum of squares of chunk i out of N chunks expressed as a ratio
    with the sum of squares over the whole series. segmentFocus should be lower than the number of segments
    :param ts: SEQUENCE
    :param num_segments: LONG
    :param segment_focus: LONG
    :return output_0: DOUBLE
    """
    pass


def friedrich_coefficients(ts: NodeInputParamType, polynomial_order: NodeInputParamType,
                           number_of_quantiles: NodeInputParamType) -> NodeReturnType:
    """
    Coefficients of polynomial. Requires a time series, order of polynomial to fit for estimating fixed 
    points of dynamics and number of quantiles to use for averaging
    :param ts: SEQUENCE
    :param polynomial_order: INT
    :param number_of_quantiles: FLOAT
    :return output_0: ND_ARRAY
    """
    pass


def absolute_sum_of_changes(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the value of an aggregation function f_agg (e.g. var or mean) of the autocorrelation (Compare to
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation), taken over different all possible lags (1 to length of x)
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def visvalingam_multiple_ts(ts_list: NodeInputParamType, num_points: NodeInputParamType) -> NodeReturnType:
    """
    Applies Visvalingam method (minimun triangle area) to a list of time series.
    :param ts_list: LIST:SEQUENCE
    :param num_points: INT
    :return output_0: LIST:SEQUENCE
    """
    pass


def large_standard_deviation(ts: NodeInputParamType, threshold: NodeInputParamType) -> NodeReturnType:
    """
    Checks if the given time series have a large standard deviation.
    :param ts: SEQUENCE
    :param threshold: FLOAT
    :return output_0: BOOLEAN
    """
    pass


def matrix_profile_self_join(ts: NodeInputParamType, subsequence_length: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the matrix profile between the time series and itself using a subsequence length.
    :param ts: SEQUENCE
    :param subsequence_length: INT
    :return output_0: ND_ARRAY
    """
    pass


def last_location_of_maximum(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the last location of the maximum value of the given time series. The position is calculated relatively
    to the length of the time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def last_location_of_minimum(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the last location of the minimum value of each time series. The position is calculated relatively
    to the length of the series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def max_langevin_fixed_point(ts: NodeInputParamType, polynomial_order: NodeInputParamType,
                             number_of_quantiles: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the largest fixed point of dynamics. Requires a time series, the order of polynomial to fit for estimating fixed points
    of dynamics and the number of quantiles to use for averaging.
    :param ts: SEQUENCE
    :param polynomial_order: INT
    :param number_of_quantiles: FLOAT
    :return output_0: LONG
    """
    pass


def filter_greater_than_value(max_value: NodeInputParamType, array: NodeInputParamType) -> NodeReturnType:
    """
    Returns an array with those values smaller than the given max value
    :param max_value: INT
    :param array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def longest_strike_above_mean(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the length of the longest consecutive subsequence in the time series that is above the mean of the time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def local_maximal_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Calculates all Local Maximals fot the given list of time series
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:ND_ARRAY
    """
    pass


def longest_strike_below_mean(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the length of the longest consecutive subsequence in the time series that is below the mean of the time series
    :param ts: SEQUENCE
    :return output: DOUBLE
    """
    pass


def first_location_of_maximum(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the first relative location of the maximal value for each time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def first_location_of_minimum(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the first location of the minimal value of each time series. The position is calculated relatively to the length of the series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def contains_value_multiple_ts(ts_list: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a list of boolean based on whether a given value is contained within a list of time series.
    :param ts_list: LIST:SEQUENCE
    :param value: DOUBLE
    :return output_0: LIST:BOOLEAN
    """
    pass


def sum_of_reoccurring_values_ts(ts: NodeInputParamType, ts_is_sorted: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sum of all values that are present in the time series more than once.
    :param ts: SEQUENCE
    :param ts_is_sorted: BOOLEAN
    :return output_0: DOUBLE
    """
    pass


def decimal_scaling_normalization(ts: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given time series according to its maximum value and adjusts each value within the range (-1, 1).
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def dynamic_time_warping_distance(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the Dynamic Time Warping Distance for the given list of time series. Returns an Array with an upper triangular matrix
    where each position corresponds to the distance between two time series. Diagonal elements will be zero.
    :param ts: LIST:SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def filter_greater_than_value_list(max_value: NodeInputParamType, values: NodeInputParamType) -> NodeReturnType:
    """
    Returns a list of integer with those values smaller than the given max value
    :param max_value: INT
    :param values: LIST:INT
    :return output_0: LIST:INT
    """
    pass


def mean_second_derivative_central(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates mean value of a central approximation of the second derivative for the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def mean_normalization_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given list of time series according to the maximum-minimum value and mean of each time series. 
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:SEQUENCE
    """
    pass


def max_min_normalization_multiple_ts(ts_list: NodeInputParamType, high: NodeInputParamType,
                                      low: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given list of time series according to its minimum and maximum value and adjusts each value within the range [low, high].
    :param ts_list: LIST:SEQUENCE
    :param high: DOUBLE
    :param low: DOUBLE
    :return output_0: LIST:SEQUENCE
    """
    pass


def sum_of_reoccurring_data_points_ts(ts: NodeInputParamType, ts_is_sorted: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sum of all data points that are present in the time series more than once.
    :param ts: SEQUENCE
    :param ts_is_sorted: BOOLEAN
    :return output_0: DOUBLE
    """
    pass


def time_reversal_asymmetry_statistic_ts(ts: NodeInputParamType, lag: NodeInputParamType) -> NodeReturnType:
    """
     This function calculates the value of:
    
        .. math::
    
            \frac{1}{n-2lag} \sum_{i=0}^{n-2lag} x_{i + 2 \cdot lag}^2 \cdot x_{i + lag} - x_{i + lag} \cdot  x_{i}^2
    
        which is
    
        .. math::
    
            \mathbb{E}[L^2(X)^2 \cdot L(X) - L(X) \cdot X^2]
    
    where :math:`\mathbb{E}` is the mean and :math:`L` is the lag operator. It was proposed in [1] as a promising feature to extract from time series.
    :param ts: SEQUENCE
    :param lag: INT
    :return output_0: DOUBLE
    """
    pass


def variance_larger_than_standard_deviation(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates if the variance of the given time series is greater than the standard deviation. In other words, if the variance of
    the time series is larger than 1.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def ratio_value_number_to_time_series_length(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates a factor which is 1 if all values in the time series occur only once, and below one if this is not the case.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def decimal_scaling_normalization_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given list of time series according to its maximum value and adjusts each value within the range (-1, 1).
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:SEQUENCE
    """
    pass
