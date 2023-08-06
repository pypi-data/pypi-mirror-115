# -*- coding: utf-8 -*-
"""Helper functions for pybaselines.

Created on March 5, 2021
@author: Donald Erb

"""

import numpy as np

from ._compat import jit


# Note: the triple quotes are for including the attributes within the documentation
PENTAPY_SOLVER = 2
"""An integer designating the solver to use if pentapy is installed.
pentapy's solver can be used for solving pentadiagonal linear systems, such
as those used for the Whittaker-smoothing-based algorithms. Should be 2 (default)
or 1. See :func:`pentapy.core.solve` for more details.
"""

PERMC_SPEC = None
"""A deprecated constant used in previous versions. Will be removed in v0.6.0."""

# the minimum positive float values such that a + _MIN_FLOAT != a
# TODO this is mostly used to prevent dividing by 0; is there a better way to do that?
# especially since it is usually max(value, _MIN_FLOAT) and in some cases value could be
# < _MIN_FLOAT but still > 0 and useful; think about it
_MIN_FLOAT = np.finfo(float).eps


class ParameterWarning(UserWarning):
    """
    Warning issued when a parameter value is outside of the recommended range.

    For cases where a parameter value is valid and will not cause errors, but is
    outside of the recommended range of values and as a result may cause issues
    such as numerical instability that would otherwise be hard to diagnose.
    """


def relative_difference(old, new, norm_order=None):
    """
    Calculates the relative difference (norm(new-old) / norm(old)) of two values.

    Used as an exit criteria in many baseline algorithms.

    Parameters
    ----------
    old : numpy.ndarray or float
        The array or single value from the previous iteration.
    new : numpy.ndarray or float
        The array or single value from the current iteration.
    norm_order : int, optional
        The type of norm to calculate. Default is None, which is l2
        norm for arrays, abs for scalars.

    Returns
    -------
    float
        The relative difference between the old and new values.

    """
    numerator = np.linalg.norm(new - old, norm_order)
    denominator = np.maximum(np.linalg.norm(old, norm_order), _MIN_FLOAT)
    return numerator / denominator


def gaussian(x, height=1.0, center=0.0, sigma=1.0):
    """
    Generates a gaussian distribution based on height, center, and sigma.

    Parameters
    ----------
    x : numpy.ndarray
        The x-values at which to evaluate the distribution.
    height : float, optional
        The maximum height of the distribution. Default is 1.0.
    center : float, optional
        The center of the distribution. Default is 0.0.
    sigma : float, optional
        The standard deviation of the distribution. Default is 1.0.

    Returns
    -------
    numpy.ndarray
        The gaussian distribution evaluated with x.

    """
    return height * np.exp(-0.5 * ((x - center)**2) / sigma**2)


def gaussian_kernel(window_size, sigma=1.0):
    """
    Creates an area-normalized gaussian kernel for convolution.

    Parameters
    ----------
    window_size : int
        The number of points for the entire kernel.
    sigma : float, optional
        The standard deviation of the gaussian model.

    Returns
    -------
    numpy.ndarray, shape (window_size,)
        The area-normalized gaussian kernel.

    Notes
    -----
    Return gaus/sum(gaus) rather than creating a unit-area gaussian
    since the unit-area gaussian would have an area smaller than 1
    for window_size < ~ 6 * sigma.

    """
    # centers distribution from -half_window to half_window
    x = np.arange(0, window_size) - (window_size - 1) / 2
    gaus = gaussian(x, 1, 0, sigma)
    return gaus / np.sum(gaus)


def _get_edges(data, pad_length, mode='extrapolate', extrapolate_window=None, **pad_kwargs):
    """
    Provides the left and right edges for padding data.

    Parameters
    ----------
    data : array-like
        The array of the data.
    pad_length : int
        The number of points to add to the left and right edges.
    mode : str, optional
        The method for padding. Default is 'extrapolate'. Any method other than
        'extrapolate' will use numpy.pad.
    extrapolate_window : int, optional
        The number of values to use for linear fitting on the left and right
        edges. Default is None, which will set the extrapolate window size equal
        to the `half_window` size.
    **pad_kwargs
        Any keyword arguments to pass to numpy.pad, which will be used if `mode`
        is not 'extrapolate'.

    Returns
    -------
    left_edge : numpy.ndarray, shape(pad_length,)
        The array of data for the left padding.
    right_edge : numpy.ndarray, shape(pad_length,)
        The array of data for the right padding.

    Notes
    -----
    If mode is 'extrapolate', then the left and right edges will be fit with
    a first order polynomial and then extrapolated. Otherwise, uses numpy.pad.

    """
    y = np.asarray(data)
    if pad_length == 0:
        return y

    mode = mode.lower()
    if mode == 'extrapolate':
        if extrapolate_window is None:
            extrapolate_window = 2 * pad_length + 1
        x = np.arange(-pad_length, y.shape[0] + pad_length)
        left_poly = np.polynomial.Polynomial.fit(
            x[pad_length:-pad_length][:extrapolate_window],
            y[:extrapolate_window], 1
        )
        right_poly = np.polynomial.Polynomial.fit(
            x[pad_length:-pad_length][-extrapolate_window:],
            y[-extrapolate_window:], 1
        )

        left_edge = left_poly(x[:pad_length])
        right_edge = right_poly(x[-pad_length:])
    else:
        padded_data = np.pad(y, pad_length, mode, **pad_kwargs)
        left_edge = padded_data[:pad_length]
        right_edge = padded_data[-pad_length:]

    return left_edge, right_edge


def pad_edges(data, pad_length, mode='extrapolate',
              extrapolate_window=None, **pad_kwargs):
    """
    Adds left and right edges to the data.

    Parameters
    ----------
    data : array-like
        The array of the data.
    pad_length : int
        The number of points to add to the left and right edges.
    mode : str, optional
        The method for padding. Default is 'extrapolate'. Any method other than
        'extrapolate' will use numpy.pad.
    extrapolate_window : int, optional
        The number of values to use for linear fitting on the left and right
        edges. Default is None, which will set the extrapolate window size equal
        to the `half_window` size.
    **pad_kwargs
        Any keyword arguments to pass to numpy.pad, which will be used if `mode`
        is not 'extrapolate'.

    Returns
    -------
    padded_data : numpy.ndarray, shape (N + 2 * half_window,)
        The data with padding on the left and right edges.

    Notes
    -----
    If mode is 'extrapolate', then the left and right edges will be fit with
    a first order polynomial and then extrapolated. Otherwise, uses numpy.pad.

    """
    y = np.asarray(data)
    if pad_length == 0:
        return y

    if mode.lower() == 'extrapolate':
        left_edge, right_edge = _get_edges(y, pad_length, mode, extrapolate_window)
        padded_data = np.concatenate((left_edge, y, right_edge))
    else:
        padded_data = np.pad(y, pad_length, mode.lower(), **pad_kwargs)

    return padded_data


def padded_convolve(data, kernel, mode='reflect', **pad_kwargs):
    """
    Pads data before convolving to reduce edge effects.

    Parameters
    ----------
    data : numpy.ndarray, shape (N,)
        The data to smooth.
    kernel : numpy.ndarray, shape (M,)
        A pre-computed, normalized kernel for the convolution. Indices should
        span from -half_window to half_window.

    Returns
    -------
    numpy.ndarray, shape (N,)
        The smoothed input array.

    """
    # TODO need to revisit this and ensure everything is correct
    padding = min(data.shape[0], kernel.shape[0]) // 2
    convolution = np.convolve(
        pad_edges(data, padding, mode, **pad_kwargs), kernel, mode='valid'
    )
    return convolution


def _safe_std(array, **kwargs):
    """
    Calculates the standard deviation and protects against nan and 0.

    Used to prevent propogating nan or dividing by 0.

    Parameters
    ----------
    array : numpy.ndarray
        The array of values for calculating the standard deviation.
    **kwargs
        Additional keyword arguments to pass to :func:`numpy.std`.

    Returns
    -------
    std : float
        The standard deviation of the array, or `_MIN_FLOAT` if the
        calculated standard deviation was 0 or if `array` was empty.

    Notes
    -----
    Does not protect against the calculated standard deviation of a non-empty
    array being nan because that would indicate that nan or inf was within the
    array, which should not be protected.

    """
    # std would be 0 for an array with size of 1 and inf if size <= ddof; only
    # internally use ddof=1, so the second condition is already covered
    if array.size < 2:
        std = _MIN_FLOAT
    else:
        std = array.std(**kwargs)
        if std == 0:
            std = _MIN_FLOAT

    return std


@jit(nopython=True, cache=True)
def _interp_inplace(x, y, y_start=None, y_end=None):
    """
    Interpolates values inplace between the two ends of an array.

    Parameters
    ----------
    x : numpy.ndarray
        The x-values for interpolation. All values are assumed to be valid.
    y : numpy.ndarray
        The y-values. The two endpoints, y[0] and y[-1] are assumed to be valid,
        and all values inbetween (ie. y[1:-1]) will be replaced by interpolation.
    y_start : float, optional
        The initial y-value for interpolation. Default is None, which will use the
        first item in `y`.
    y_end : float, optional
        The end y-value for interpolation. Default is None, which will use the
        last item in `y`.

    Returns
    -------
    y : numpy.ndarray
        The input `y` array, with the interpolation performed inplace.

    """
    if y_start is None:
        y_start = y[0]
    if y_end is None:
        y_end = y[-1]
    y[1:-1] = y_start + (x[1:-1] - x[0]) * ((y_end - y_start) / (x[-1] - x[0]))

    return y


def _convert_coef(coef, original_domain):
    """
    Scales the polynomial coefficients back to the original domain of the data.

    For fitting, the x-values are scaled from their original domain, [min(x),
    max(x)], to [-1, 1] in order to improve the numerical stability of fitting.
    This function rescales the retrieved polynomial coefficients for the fit
    x-values back to the original domain.

    Parameters
    ----------
    coef : array-like
        The array of coefficients for the polynomial. Should increase in
        order, for example (c0, c1, c2) from `y = c0 + c1 * x + c2 * x**2`.
    original_domain : array-like, shape (2,)
        The domain, [min(x), max(x)], of the original data used for fitting.

    Returns
    -------
    output_coefs : numpy.ndarray
        The array of coefficients scaled for the original domain.

    """
    zeros_mask = np.equal(coef, 0)
    if zeros_mask.any():
        # coefficients with one or several zeros sometimes get compressed
        # to leave out some of the coefficients, so replace zero with another value
        # and then fill in later
        coef = coef.copy()
        coef[zeros_mask] = _MIN_FLOAT  # could probably fill it with any non-zero value

    fit_polynomial = np.polynomial.Polynomial(coef, domain=original_domain)
    output_coefs = fit_polynomial.convert().coef
    output_coefs[zeros_mask] = 0

    return output_coefs


def _quantile_loss(y, fit, quantile, eps=None):
    r"""
    An approximation of quantile loss.

    The loss is defined as :math:`\rho(r) / |r|`, where r is the residual, `y - fit`,
    and the function :math:`\rho(r)` is `quantile` for `r` > 0 and 1 - `quantile`
    for `r` < 0. Rather than using `|r|` as the denominator, which is non-differentiable
    and causes issues when `r` = 0, the denominator is approximated as
    :math:`\sqrt{r^2 + eps}` where `eps` is a small number.

    Parameters
    ----------
    y : numpy.ndarray
        The values of the raw data.
    fit : numpy.ndarray
        The fit values.
    quantile : float
        The quantile value.
    eps : float, optional
        A small value added to the square of `residual` to prevent dividing by 0.
        Default is None, which uses `(1e-6 * max(abs(fit)))**2`.

    Returns
    -------
    numpy.ndarray
        The calculated loss, which can be used as weighting when performing iteratively
        reweighted least squares (IRLS)

    References
    ----------
    Schnabel, S., et al. Simultaneous estimation of quantile curves using quantile
    sheets. AStA Advances in Statistical Analysis, 2013, 97, 77-87.

    """
    if eps is None:
        # 1e-6 seems to work better than the 1e-4 in Schnabel, et al
        eps = (np.abs(fit).max() * 1e-6)**2
    residual = y - fit
    numerator = np.where(residual > 0, quantile, 1 - quantile)
    # use max(eps, _MIN_FLOAT) to ensure that eps + 0 > 0
    denominator = np.sqrt(residual**2 + max(eps, _MIN_FLOAT))  # approximates abs(residual)

    return numerator / denominator


def _quantile_irls(y, basis, weights, quantile=0.05, max_iter=250, tol=1e-6, eps=None):
    """
    An iteratively reweighted least squares (irls) version of quantile regression.

    Parameters
    ----------
    y : numpy.ndarray, shape (N,)
        The array of data values.
    basis : numpy.ndarray, shape (N, M)
        The basis matrix for the calculation. For example, if fitting a polynomial,
        `basis` would be the Vandermonde matrix.
    weights : numpy.ndarray, shape (N,)
        The array of initial weights.
    quantile : float, optional
        The quantile at which to fit the baseline. Default is 0.05.
    max_iter : int, optional
        The maximum number of iterations. Default is 250.
    tol : float, optional
        The exit criteria. Default is 1e-6.
    eps : float, optional
        A small value added to the square of the residual to prevent dividing by 0.
        Default is None, which uses the square of the maximum-absolute-value of the
        fit each iteration multiplied by 1e-6.

    Returns
    -------
    baseline : numpy.ndarray, shape (N,)
        The calculated baseline.
    weights : numpy.ndarray, shape (N,)
        The weight array used for fitting the data.
    tol_history : numpy.ndarray
        An array containing the calculated tolerance values for
        each iteration. The length of the array is the number of iterations
        completed. If the last value in the array is greater than the input
        `tol` value, then the function did not converge.
    coef : numpy.ndarray, shape (M,)
        The array of coefficients used to create the best fit using `basis.dot(coef)`.

    Notes
    -----
    This should not be called directly since it does no input validation.

    References
    ----------
    Schnabel, S., et al. Simultaneous estimation of quantile curves using
    quantile sheets. AStA Advances in Statistical Analysis, 2013, 97, 77-87.

    """
    # estimate first iteration using least squares
    coef = np.linalg.lstsq(basis * weights[:, None], y * weights, None)[0]
    baseline = basis.dot(coef)
    tol_history = np.empty(max_iter)
    for i in range(max_iter):
        baseline_old = baseline
        weights = np.sqrt(_quantile_loss(y, baseline, quantile, eps))
        coef = np.linalg.lstsq(basis * weights[:, None], y * weights, None)[0]
        baseline = basis.dot(coef)
        # relative_difference(baseline_old, baseline, 1) gives nearly same result and
        # the l2 norm is faster to calculate, so use that instead of l1 norm
        calc_difference = relative_difference(baseline_old, baseline)
        tol_history[i] = calc_difference
        if calc_difference < tol:
            break

    return baseline, weights, tol_history[:i + 1], coef
