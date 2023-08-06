"""
Copyright (c) 2014, Elias Wegert
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the distribution

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

From:
https://it.mathworks.com/matlabcentral/fileexchange/44375-phase-plots-of-complex-functions?s_tid=mwa_osa_a
"""

import numpy as np
from matplotlib.colors import hsv_to_rgb


def to_rgb_255(func):
    """Convert a Numpy array with values in the range [0, 1] to [0, 255]."""

    def wrapper(*args, **kwargs):
        rgb = func(*args, **kwargs)
        return (rgb * 255).astype(np.uint8)

    return wrapper


def rect_func(x, dx):
    """Create rectangular impulses of length dx."""
    return np.mod(np.floor(x / dx), 2)


def saw_func(x, dx, a, b):
    """Saw tooth function on R with period dx onto [a,b]"""
    x = x / dx - np.floor(x / dx)
    return a + (b - a) * x


@to_rgb_255
def bw_stripes_phase(w, phaseres=20):
    """Alternating black and white stripes corresponding to phase."""
    arg = np.angle(w)
    # normalize the argument to [0, 1]
    arg[arg < 0] += 2 * np.pi
    arg /= 2 * np.pi
    black = saw_func(arg, 1 / phaseres, 0, 1)
    bmin, bmax = black.min(), black.max()
    black = np.floor(2 * (black - bmin) / (bmax - bmin))
    return np.dstack([black, black, black])


@to_rgb_255
def bw_stripes_mag(w, phaseres=20):
    """Alternating black and white stripes corresponding to modulus."""
    mag = np.absolute(w)
    black = saw_func(np.log(mag), 2 * np.pi / phaseres, 0, 1)
    bmin, bmax = black.min(), black.max()
    black = np.floor(2 * (black - bmin) / (bmax - bmin))
    return np.dstack([black, black, black])


@to_rgb_255
def domain_coloring(w, phaseres=20):
    """Standard domain coloring."""
    arg = np.angle(w)
    # normalize the argument to [0, 1]
    arg[arg < 0] += 2 * np.pi
    arg /= 2 * np.pi
    H = arg
    S = V = np.ones_like(H)
    return hsv_to_rgb(np.dstack([H, S, V]))


@to_rgb_255
def enhanced_domain_coloring(w, phaseres=20):
    """Enhanced domain coloring showing iso-lines for magnitude and phase."""
    mag, arg = np.absolute(w), np.angle(w)
    # normalize the argument to [0, 1]
    arg[arg < 0] += 2 * np.pi
    arg /= 2 * np.pi
    blackp = saw_func(arg, 1 / phaseres, 0.75, 1)
    blackm = saw_func(np.log(mag), 2 * np.pi / phaseres, 0.75, 1)
    black = blackp * blackm
    H = arg
    S, V = np.ones_like(H), black
    return hsv_to_rgb(np.dstack([H, S, V]))


@to_rgb_255
def enhanced_domain_coloring_phase(w, phaseres=20):
    """Enhanced domain coloring showing iso-lines for phase."""
    arg = np.angle(w)
    # normalize the argument to [0, 1]
    arg[arg < 0] += 2 * np.pi
    arg /= 2 * np.pi
    blackp = saw_func(arg, 1 / phaseres, 0.75, 1)
    H = arg
    S, V = np.ones_like(H), blackp
    return hsv_to_rgb(np.dstack([H, S, V]))


@to_rgb_255
def enhanced_domain_coloring_mag(w, phaseres=20):
    """Enhanced domain coloring showing iso-lines for magnitude."""
    mag, arg = np.absolute(w), np.angle(w)
    # normalize the argument to [0, 1]
    arg[arg < 0] += 2 * np.pi
    arg /= 2 * np.pi
    blackm = saw_func(np.log(mag), 2 * np.pi / phaseres, 0.75, 1)
    H = arg
    S, V = np.ones_like(H), blackm
    return hsv_to_rgb(np.dstack([H, S, V]))


@to_rgb_255
def bw_stripes_imag(w, phaseres=20):
    """Alternating black and white stripes corresponding to imaginary part.
    In particular recommended for stream lines of potential flow.
    """
    imres = 10 / phaseres
    black = saw_func(np.imag(w), imres, 0, 1)
    bmin, bmax = black.min(), black.max()
    black = np.floor(2 * (black - bmin) / (bmax - bmin))
    return np.dstack([black, black, black])


@to_rgb_255
def bw_stripes_real(w, phaseres=20):
    """Alternating black and white stripes corresponding to real part.
    In particular recommended for stream lines of potential flow.
    """
    reres = 10 / phaseres
    black = saw_func(np.real(w), reres, 0, 1)
    bmin, bmax = black.min(), black.max()
    black = np.floor(2 * (black - bmin) / (bmax - bmin))
    return np.dstack([black, black, black])


@to_rgb_255
def cartesian_chessboard(w, phaseres=20):
    """Cartesian Chessboard on the complex points space. The result will hide
    zeros.
    """
    blackx = rect_func(np.real(w), 4 / phaseres)
    blacky = rect_func(np.imag(w), 4 / phaseres)
    white = np.mod(blackx + blacky, 2)
    return np.dstack([white, white, white])


@to_rgb_255
def polar_chessboard(w, phaseres=20):
    """
    Polar Chessboard on the complex points space. The result will show
    conformality.
    """
    mag, arg = np.absolute(w), np.angle(w)
    # normalize the argument to [0, 1]
    arg[arg < 0] += 2 * np.pi
    arg /= 2 * np.pi

    blackp = rect_func(arg, 1 / phaseres)
    blackm = rect_func(np.log(mag), 2 * np.pi / phaseres)
    black = np.mod(blackp + blackm, 2)
    return np.dstack([black, black, black])

def create_colorscale(N=256):
    """
    Create a HSV colorscale which will be used to map argument values from
    [-pi, pi]. Red color is associated to zero.

    Parameters
    ==========
        N : int
            Number of discretized colors. Default to 256.

    Returns
    =======
        colorscale : np.ndarray [N x 3]
            Each row is an RGB colors (0 <= R,G,B <= 255).
    """
    H = np.linspace(0, 1, N)
    S = V = np.ones_like(H)
    colorscale = hsv_to_rgb(np.dstack([H, S, V]))
    colorscale = (colorscale.reshape((-1, 3)) * 255).astype(np.uint8)
    colorscale = np.roll(colorscale, int(len(colorscale) / 2), axis=0)
    return colorscale

def wegert(coloring, w, phaseres=20, N=256):
    """
    Parameters
    ==========

    coloring : str
        A character from ``"a"`` to ``"j"``.

    w : ndarray [n x m]
        Numpy array with the results (complex numbers) of the evaluation of
        a complex function.

    phaseres : int
        Number of constant-phase lines.

    N : int
        Number of discretized color in the colorscale. Default to 256.

    Returns
    =======

    img : np.ndarray [n x m x 3]
        An array of RGB colors (0 <= R,G,B <= 255)

    colorscale : np.ndarray [N x 3] or None
        RGB colors to be used in the colorscale. If the function computes
        black and white colors, ``None`` will be returned.
    """
    mapping = {
        "a": [domain_coloring, True],
        "b": [enhanced_domain_coloring, True],
        "c": [enhanced_domain_coloring_mag, True],
        "d": [enhanced_domain_coloring_phase, True],
        "e": [bw_stripes_mag, False],
        "f": [bw_stripes_phase, False],
        "g": [bw_stripes_real, False],
        "h": [bw_stripes_imag, False],
        "i": [cartesian_chessboard, False],
        "j": [polar_chessboard, False]
    }

    if coloring not in mapping.keys():
        raise KeyError(
            "`coloring` must be one of the following: {}".format(mapping.keys())
        )
    func, create_cc = mapping[coloring]
    if create_cc:
        return func(w, phaseres), create_colorscale(N)
    return func(w, phaseres), None
