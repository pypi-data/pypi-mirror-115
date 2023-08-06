import os
import numpy as np


_LIBPATH = os.path.abspath(os.path.dirname(__file__))
_CACHE = {}


def key_101_2009():
    """101 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.


    > Key, K., 2009;
    > 1D inversion of multicomponent, multifrequency marine CSEM data:
    > Methodology and synthetic studies for resolving thin resistive layers;
    > Geophysics, 74(2), F9-F20;
    > DOI: 10.1190/1.3058434


    Copyright 2009 Kerry Key

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'key_101_2009' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_key_101_2009_j0j1.txt'
        _CACHE['key_101_2009'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['key_101_2009']


def key_201_2009():
    """201 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.


    > Key, K., 2009;
    > 1D inversion of multicomponent, multifrequency marine CSEM data:
    > Methodology and synthetic studies for resolving thin resistive layers;
    > Geophysics, 74(2), F9-F20;
    > DOI: 10.1190/1.3058434


    Copyright 2009 Kerry Key

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'key_201_2009' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_key_201_2009_j0j1.txt'
        _CACHE['key_201_2009'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['key_201_2009']


def key_401_2009():
    """401 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.


    > Key, K., 2009;
    > 1D inversion of multicomponent, multifrequency marine CSEM data:
    > Methodology and synthetic studies for resolving thin resistive layers;
    > Geophysics, 74(2), F9-F20;
    > DOI: 10.1190/1.3058434


    Copyright 2009 Kerry Key

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'key_401_2009' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_key_401_2009_j0j1.txt'
        _CACHE['key_401_2009'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['key_401_2009']


def key_51_2012():
    """51 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.


    > Key, K., 2012;
    > Is the fast Hankel transform faster than quadrature?;
    > Geophysics, 77(3), F21-F30;
    > DOI: 10.1190/geo2011-0237.1


    Copyright 2012 Kerry Key

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'key_51_2012' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_key_51_2012_j0j1.txt'
        _CACHE['key_51_2012'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['key_51_2012']


def key_101_2012():
    """101 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.


    > Key, K., 2012;
    > Is the fast Hankel transform faster than quadrature?;
    > Geophysics, 77(3), F21-F30;
    > DOI: 10.1190/geo2011-0237.1


    Copyright 2012 Kerry Key

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'key_101_2012' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_key_101_2012_j0j1.txt'
        _CACHE['key_101_2012'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['key_101_2012']


def key_201_2012():
    """201 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.


    > Key, K., 2012;
    > Is the fast Hankel transform faster than quadrature?;
    > Geophysics, 77(3), F21-F30;
    > DOI: 10.1190/geo2011-0237.1


    Copyright 2012 Kerry Key

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'key_201_2012' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_key_201_2012_j0j1.txt'
        _CACHE['key_201_2012'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['key_201_2012']


def wer_201_2018():
    """201 point Hankel filter, J0 and J1


    Designed and tested for controlled-source electromagnetic data.

    See the notebook `Filter-wer201.ipynb` in the repo
    https://github.com/emsig/article-fdesign


    > Werthmüller, D., K. Key, and E. Slob, 2019;
    > A tool for designing digital filters for the Hankel and Fourier
    > transforms in potential, diffusive, and wavefield modeling;
    > Geophysics, 84(2), F47-F56;
    > DOI: 10.1190/geo2018-0069.1


    Copyright 2018 Dieter Werthmüller

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'wer_201_2018' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_wer_201_2018_j0j1.txt'
        _CACHE['wer_201_2018'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['wer_201_2018']


def wer_2001_2018():
    """2001 point Hankel filter, J0 and J1


    Designed and tested for ground-penetrating radar (GPR).

    See the notebook `Filter-wer2001.ipynb` in the repo
    https://github.com/emsig/article-fdesign


    > Werthmüller, D., K. Key, and E. Slob, 2019;
    > A tool for designing digital filters for the Hankel and Fourier
    > transforms in potential, diffusive, and wavefield modeling;
    > Geophysics, 84(2), F47-F56;
    > DOI: 10.1190/geo2018-0069.1


    Copyright 2018 Dieter Werthmüller

    This work is licensed under a CC BY 4.0 license.
    <http://creativecommons.org/licenses/by/4.0/>.


    Returns
    -------
    base, j0, j1 : ndarray
        Filter base and its values.

    """
    if 'wer_2001_2018' not in _CACHE.keys():
        fname = 'lib/Hankel/hankel_wer_2001_2018_j0j1.txt'
        _CACHE['wer_2001_2018'] = np.loadtxt(
            os.path.join(_LIBPATH, fname), unpack=True)
    return _CACHE['wer_2001_2018']
