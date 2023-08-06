"""
.. _bispectrum:

Implementation using Numba acceleration.

.. moduleauthor:: Michael O'Brien <michaelobrien@g.harvard.edu>

"""

import numpy as np
import numba as nb
from time import time


def bispectrum(*u, ntheta=None, kmin=None, kmax=None,
               diagnostics=True, error=False,
               nsamples=None, sample_thresh=None,
               compute_fft=True, exclude_upper=False, use_pyfftw=False,
               bench=False, progress=False, **kwargs):
    """
    Estimate the bispectrum :math:`B(k_1, k_2, \\theta)`
    and bicoherence index :math:`b(k_1, k_2, \\theta)` of a real
    scalar or vector field :math:`u`.

    Assuming statistical homogeneity, the bispectrum
    :math:`B(\mathbf{k}_1, \mathbf{k}_2, \mathbf{k}_3)` is defined as the
    3-point correlation function in Fourier space with
    :math:`\mathbf{k}_1 + \mathbf{k}_2 + \mathbf{k}_3 = 0`. For a
    real :math:`u`

    .. math::
        B(\mathbf{k}_1, \mathbf{k}_2, - \mathbf{k}_1 - \mathbf{k}_2) = 
            \\langle\\tilde{u}(\mathbf{k}_1)\\tilde{u}(\mathbf{k}_2)
            \\tilde{u}^{*}(\mathbf{k}_1+\mathbf{k}_2)\\rangle,

    where :math:`\\tilde{u}` is the Fourier transform of :math:`u`
    and :math:`\\langle\cdot\\rangle` is some ensemble average.
    We compute our bispectrum as

    .. math::
        B(k_1, k_2, \\theta) = \\frac{1}{V_1 V_2} \int\int_{\Omega}
            d^D \mathbf{k}_1 d^D \mathbf{k}_2 \ 
                \\tilde{u}(\mathbf{k}_1)\\tilde{u}(\mathbf{k}_2)
                    \\tilde{u}^{*}(\mathbf{k}_1 + \mathbf{k}_2),

    and the bicoherence as

    .. math::
        b(k_1, k_2, \\theta) = \\frac{
            |\int\int_{\Omega} d^D \mathbf{k}_1 d^D \mathbf{k}_2 \ 
                \\tilde{u}(\mathbf{k}_1)\\tilde{u}(\mathbf{k}_2)
                    \\tilde{u}^{*}(\mathbf{k}_1 + \mathbf{k}_2)|}{
            \int\int_{\Omega} d^D \mathbf{k}_1 d^D \mathbf{k}_2 \ 
                |\\tilde{u}(\mathbf{k}_1)\\tilde{u}(\mathbf{k}_2)
                    \\tilde{u}^{*}(\mathbf{k}_1 + \mathbf{k}_2)|}.

    :math:`\Omega` is the set of all unique
    (:math:`\mathbf{k}_1`, :math:`\mathbf{k}_2`) pairs such that
    :math:`|\mathbf{k}_1| \in [k_1, k_1+1)`,
    :math:`|\mathbf{k}_2| \in [k_2, k_2+1)`, and
    :math:`\\arccos{(\hat{\mathbf{k}}_1 \cdot \hat{\mathbf{k}}_2)} \in [\\theta, \\theta+\\Delta \\theta)`.
    By "unique" pairs, we mean (:math:`\mathbf{k}_1`, :math:`\mathbf{k}_2`)
    but not the complex conjugate evaluations for
    (:math:`-\mathbf{k}_1`, :math:`-\mathbf{k}_2`). Otherwise,
    :math:`B` would be a real function.

    If the data is also statistically isotropic, then we can say that
    the bispectrum is only a function of scalar wavenumber,
    :math:`B = B(k_1, k_2, k_3)`. In this case, :math:`B` accounts
    for all degrees of freedom of the bispectrum. Use this implementation's
    variance estimates on the average over :math:`\\Omega`
    to test this assumption.

    To calculate :math:`B`, we take the average

    .. math::
        B(k_1, k_2, \\theta) = \\frac{1}{|\Omega|}
            \sum\limits_{\Omega} \\tilde{u}(\mathbf{k}_1)\\tilde{u}(\mathbf{k}_2)
                                 \\tilde{u}^{*}(\mathbf{k}_1 + \mathbf{k}_2),

    where now :math:`\\tilde{u}` is an FFT. For 3D fields, the full sum is often
    too large to compute. Instead, we compute a naive Monte Carlo
    integration by drawing :math:`N` uniform samples
    :math:`(\mathbf{k}_1^n, \mathbf{k}_2^n)` from the set :math:`\Omega`.
    This defines an unbiased estimator of :math:`B`,

     .. math::
        \\hat{B}(k_1, k_2, \\theta) = \\frac{1}{N}
            \sum\limits_{n = 1}^{N} \\tilde{u}(\mathbf{k}_1^n)\\tilde{u}(\mathbf{k}_2^n)
                                 \\tilde{u}^{*}(\mathbf{k}_1^n + \mathbf{k}_2^n).

    The same procedure is used to compute :math:`b`. By default, this
    implementation returns :math:`B(k_1, k_2)`, the mean
    bispectrum summed over triangle angle :math:`\\theta`.

    To learn more, read `here <https://arxiv.org/pdf/astro-ph/0112551.pdf>`_.

    .. note::
        One can recover the sum over triangles by multiplying ``counts * B``
        when ``nsamples = None``. Or, if ``ntheta = None``,
        evaulate ``omega * B``.

    .. note::
        When considering the bispectrum as a function of triangle
        angle, mesh points may be set to ``np.nan`` depending on
        :math:`k_1, \ k_2`. For example, :math:`\\theta = 0`
        would yield ``np.nan`` for all
        :math:`k_1 + k_2 > \\sqrt{2} \ k_{nyq}`, where :math:`k_{nyq}`
        is the Nyquist frequency.
        Computing a boolean mask with ``np.isnan`` and reductions
        like ``np.nansum`` can be useful.

    .. note::
        Computing ``np.nansum(B*counts, axis=0)/np.sum(counts, axis=0)``
        recovers the bispectrum summed over triangle angles.
        To recover the corresponding bicoherence, evaulate
        ``np.abs(np.nansum(B, axis=0)) / np.nansum(np.abs(B)/b, axis=0)``.

    Parameters
    ----------
    u : `np.ndarray`
        Scalar or vector field.
        If vector data, pass arguments as ``u1, u2, ..., un``,
        where ``ui`` is the ith vector component.
        Each ``ui`` can be 2D or 3D, and all must have the
        same ``ui.shape`` and ``ui.dtype``. The vector
        bispectrum will be computed as the sum over bispectra
        of each component.
    ntheta : `int`, optional
        Number of angular bins :math:`\\theta` between triangles
        formed by wavevectors :math:`\mathbf{k_1}, \ \mathbf{k_2}`.
        If ``None``, sum over all triangle angles. Otherwise,
        return a bispectrum for each angular bin.
    kmin : `int`, optional
        Minimum wavenumber in bispectrum calculation.
        If ``None``, ``kmin = 1``.
    kmax : `int`, optional
        Maximum wavenumber in bispectrum calculation.
        If ``None``, ``kmax = max(u.shape)//2``
    diagnostics : `bool`, optional
        Return the optional sampling and normalization diagnostics,
        documented below. Set ``error = True`` to also return the
        standard error of the mean.
    error : `bool`, optional
        Return standard error of the mean of the Monte-Carlo integration.
        ``diagnostics = True`` must also be set. This will add a bit of
        time to the calculation.
    nsamples : `int`, `float` or `np.ndarray`, shape `(kmax-kmin+1, kmax-kmin+1)`, optional
        Number of sample triangles or fraction of total
        possible triangles. This may be an array that
        specifies for a given :math:`k_1, \ k_2`.
        If ``None``, calculate the exact sum.
    sample_thresh : `int`, optional
        When the size of the sample space is greater than
        this number, start to use sampling instead of exact
        calculation. If ``None``, switch to exact calculation
        when ``nsamples`` is less than the size of the sample space.
    compute_fft : `bool`, optional
        If ``False``, do not take the FFT of the input data.
        FFTs should not be passed with the zero-frequency
        component in the center, and it should have the same
        shape as the real-space data.
    exclude_upper : `bool`, optional
        If ``True``, set points where :math:`k_1 + k_2 > k_{nyq}`
        to ``np.nan``. This keyword only applies when summing
        over angles, e.g. when ``ntheta is None``.
    use_pyfftw : `bool`, optional
        If ``True``, use ``pyfftw`` instead of ``np.fft``
        to compute FFTs.
    bench : `bool`, optional
        If True, print calculation time.
    progress : `bool`, optional
        Print progress bar of calculation.
    kwargs
        Additional keyword arguments passed to
        ``np.fft.fftn`` or ``pyfftw.builders.fftn``.

    Returns
    -------
    B : `np.ndarray`, shape `(m, kmax-kmin+1, kmax-kmin+1)`
        Bispectrum :math:`B(k_1, k_2, \\theta)`.
    b : `np.ndarray`, shape `(m, kmax-kmin+1, kmax-kmin+1)`
        Bicoherence index :math:`b(k_1, k_2, \\theta)`.
    kn : `np.ndarray`, shape `(kmax-kmin+1,)`
        Left edges of wavenumber bins :math:`k_1` or :math:`k_2`
        along axis of bispectrum.
    theta : `np.ndarray`, shape `(m,)`, optional
        Left edges of angular bins :math:`\\theta`, ranging from
        :math:`[0, \ \\pi)`.
    counts : `np.ndarray`, shape `(m, kmax-kmin+1, kmax-kmin+1)`, optional
        Number of evaluations in the bispectrum sum, :math:`N`.
    omega : `np.ndarray`, shape `(kmax-kmin+1, kmax-kmin+1)`, optional
        Number of possible triangles in the sample space, :math:`|\\Omega|`.
        This is implemented for if sampling were *not* restricted by the Nyquist
        frequency. Note that this is only implemented for ``ntheta = None``.
    stderr : `np.ndarray`, shape `(m, kmax-kmin+1, kmax-kmin+1)`, optional
        Standard error of the mean for each bin. This can be an
        error estimate for the Monte Carlo integration. To convert
        to the standard deviation, evaluate ``stderr * np.sqrt(counts)``.
    """
    shape, ndim = nb.typed.List(u[0].shape), u[0].ndim
    ncomp = len(u)

    if ndim not in [2, 3]:
        raise ValueError("Data must be 2D or 3D.")

    # Geometry of output image
    kmax = int(max(shape)/2) if kmax is None else int(kmax)
    kmin = 1 if kmin is None else int(kmin)
    kn = np.arange(kmin, kmax+1, 1, dtype=int)
    dim = kn.size
    theta = np.arange(0, np.pi, np.pi/ntheta) if ntheta is not None else None
    # ...make costheta monotonically increase
    costheta = np.flip(np.cos(theta)) if theta is not None else np.array([1.])

    # theta = 0 should be included
    if theta is not None:
        costheta[-1] += 1e-5

    if bench:
        t0 = time()

    # Get binned radial coordinates of FFT
    kv = np.meshgrid(*([np.fft.fftfreq(Ni).astype(np.float32)*Ni
                        for Ni in shape]), indexing="ij")
    kr = np.zeros_like(kv[0])
    for i in range(ndim):
        kr[...] += kv[i]**2
    kr[...] = np.sqrt(kr)

    kcoords = nb.typed.List()
    for i in range(ndim):
        temp = kv[i].astype(np.int16).ravel()
        kcoords.append(temp)

    del kv, temp

    kbins = np.arange(int(np.ceil(kr.max())))
    kbinned = (np.digitize(kr, kbins)-1).astype(np.int16)

    del kr

    # Enumerate indices in each bin
    k1bins, k2bins = nb.typed.List(), nb.typed.List()
    for ki in kn:
        mask = kbinned == ki
        temp1 = np.where(mask)
        temp2 = np.where(mask[..., :shape[-1]//2+1])
        k1bins.append(np.ravel_multi_index(temp1, shape))
        k2bins.append(np.ravel_multi_index(temp2, shape))

    del kbinned

    # FFT
    ffts = []
    for i in range(ncomp):
        if compute_fft:
            temp = u[i]
            if use_pyfftw:
                fft = _fftn(temp, **kwargs)
            else:
                fft = np.fft.rfftn(temp, **kwargs)
            del temp
        else:
            fft = u[i][..., :shape[-1]//2+1]
        ffts.append(fft)
        del fft

    # Sampling settings
    if sample_thresh is None:
        sample_thresh = np.iinfo(np.int64).max
    if nsamples is None:
        nsamples = np.iinfo(np.int64).max
        sample_thresh = np.iinfo(np.int64).max

    # Sampling mask
    if np.issubdtype(type(nsamples), np.integer):
        nsamples = np.full((dim, dim), nsamples, dtype=np.int_)
    elif np.issubdtype(type(nsamples), np.floating):
        nsamples = np.full((dim, dim), nsamples)
    elif type(nsamples) is np.ndarray:
        if np.issubdtype(nsamples.dtype, np.integer):
            nsamples = nsamples.astype(np.int_)

    # Run main loop
    compute_point = eval(f"_compute_point{ndim}D")
    args = (k1bins, k2bins, kn, costheta, kcoords,
            nsamples, sample_thresh, ndim, dim, shape,
            progress, exclude_upper, error, compute_point, *ffts)
    B, norm, omega, counts, stderr = _compute_bispectrum(*args)

    # Set zero values to nan values for division
    mask = counts == 0.
    norm[mask] = np.nan
    counts[mask] = np.nan

    # Get bicoherence and average bispectrum
    b = np.abs(B) / norm
    B.real /= counts
    B.imag /= counts

    # Prepare diagnostics
    if error:
        stderr[counts <= 1.] = np.nan

    # Switch back to theta monotonically increasing
    if ntheta is not None:
        B[...] = np.flip(B, axis=0)
        b[...] = np.flip(b, axis=0)
        if diagnostics:
            counts[...] = np.flip(counts, axis=0)
            if error:
                stderr[...] = np.flip(stderr, axis=0)
    else:
        B, b = B[0], b[0]
        if diagnostics:
            counts = counts[0]
            if error:
                stderr = stderr[0]

    if bench:
        print(f"Time: {time() - t0:.04f} s")

    result = [B, b, kn]
    if ntheta is not None:
        result.append(theta)
    if diagnostics:
        result.extend([counts, omega])
        if error:
            result.append(stderr)

    return tuple(result)


def _fftn(image, overwrite_input=False, threads=-1, **kwargs):
    """
    Calculate N-dimensional fft of image with pyfftw.
    See pyfftw.builders.fftn for kwargs documentation.

    Parameters
    ----------
    image : np.ndarray
        Real or complex-valued 2D or 3D image
    overwrite_input : bool, optional
        Specify whether input data can be destroyed.
        This is useful for reducing memory usage.
        See pyfftw.builders.fftn for more.
    threads : int, optional
        Number of threads for pyfftw to use. Default
        is number of cores.

    Returns
    -------
    fft : np.ndarray
        The fft. Will be the shape of the input image
        or the user specified shape.
    """
    import pyfftw

    if image.dtype in [np.complex64, np.complex128]:
        dtype = 'complex128'
        fftn = pyfftw.builders.fftn
    elif image.dtype in [np.float32, np.float64]:
        dtype = 'float64'
        fftn = pyfftw.builders.rfftn
    else:
        raise ValueError(f"{data.dtype} is unrecognized data type.")

    a = pyfftw.empty_aligned(image.shape, dtype=dtype)
    f = fftn(a, threads=threads, overwrite_input=overwrite_input, **kwargs)
    a[...] = image
    fft = f()

    del a, fftn

    return fft


@nb.njit(parallel=True)
def _compute_bispectrum(k1bins, k2bins, kn, costheta, kcoords, nsamples,
                        sample_thresh, ndim, dim, shape, progress,
                        exclude, error, compute_point, *ffts):
    knyq = max(shape) // 2
    ntheta = costheta.size
    bispec = np.full((ntheta, dim, dim), np.nan+1.j*np.nan, dtype=np.complex128)
    binorm = np.full((ntheta, dim, dim), np.nan, dtype=np.float64)
    counts = np.full((ntheta, dim, dim), np.nan, dtype=np.float64)
    omega = np.zeros((dim, dim), dtype=np.int64)
    if error:
        stderr = np.full((ntheta, dim, dim), np.nan, dtype=np.float64)
    else:
        stderr = np.zeros((1, 1, 1), dtype=np.float64)
    for i in range(dim):
        k1 = kn[i]
        k1ind = k1bins[i]
        nk1 = k1ind.size
        for j in range(i+1):
            k2 = kn[j]
            if ntheta == 1 and (exclude and k1 + k2 > knyq):
                continue
            k2ind = k2bins[j]
            nk2 = k2ind.size
            nsamp = nsamples[i, j]
            nsamp = int(nsamp) if type(nsamp) is np.int64 \
                else max(int(nsamp*nk1*nk2), 1)
            if nsamp < nk1*nk2 or nsamp > sample_thresh:
                samp = np.random.randint(0, nk1*nk2, size=nsamp)
                count = nsamp
            else:
                samp = np.arange(nk1*nk2)
                count = nk1*nk2
            bispecbuf = np.zeros(count, dtype=np.complex128)
            binormbuf = np.zeros(count, dtype=np.float64)
            cthetabuf = np.zeros(count, dtype=np.float64) if ntheta > 1 \
                else np.array([0.], dtype=np.float64)
            countbuf = np.zeros(count, dtype=np.float64)
            compute_point(k1ind, k2ind, kcoords, ntheta,
                          nk1, nk2, shape, samp, count,
                          bispecbuf, binormbuf, cthetabuf, countbuf,
                          *ffts)
            if ntheta == 1:
                _fill_sum(i, j, bispec, binorm, counts, stderr,
                          bispecbuf, binormbuf, countbuf, error)
            else:
                binned = np.searchsorted(costheta, cthetabuf)
                _fill_binned_sum(i, j, ntheta, binned, bispec, binorm,
                                 counts, stderr, bispecbuf, binormbuf,
                                 countbuf, error)
            omega[i, j], omega[j, i] = nk1*nk2, nk1*nk2
        if progress:
            with nb.objmode():
                _printProgressBar(i, dim-1)
    return bispec, binorm, omega, counts, stderr


@nb.njit(parallel=True, cache=True)
def _fill_sum(i, j, bispec, binorm, counts, stderr,
              bispecbuf, binormbuf, countbuf, error):
    N = countbuf.sum()
    norm = binormbuf.sum()
    value = bispecbuf.sum()
    bispec[0, i, j], bispec[0, j, i] = value, value
    binorm[0, i, j], binorm[0, j, i] = norm, norm
    counts[0, i, j], counts[0, j, i] = N, N
    if error and N > 1:
        variance = np.abs(bispecbuf - (value / N))**2
        err = np.sqrt(variance.sum() / (N*(N - 1)))
        stderr[0, i, j], stderr[0, j, i] = err, err


@nb.njit(parallel=True, cache=True)
def _fill_binned_sum(i, j, ntheta, binned, bispec, binorm, counts,
                     stderr, bispecbuf, binormbuf, countbuf, error):
    N = np.bincount(binned, weights=countbuf, minlength=ntheta)
    norm = np.bincount(binned, weights=binormbuf, minlength=ntheta)
    value = np.bincount(binned, weights=bispecbuf.real, minlength=ntheta) +\
        1.j*np.bincount(binned, weights=bispecbuf.imag, minlength=ntheta)
    bispec[:, i, j], bispec[:, j, i] = value, value
    binorm[:, i, j], binorm[:, j, i] = norm, norm
    counts[:, i, j], counts[:, j, i] = N, N
    if error:
        variance = np.zeros_like(countbuf)
        for n in range(ntheta):
            if N[n] > 1:
                idxs = np.where(binned == n)
                mean = value[n] / N[n]
                variance[idxs] = np.abs(bispecbuf[idxs] - mean)**2 / (N[n]*(N[n]-1))
        err = np.sqrt(np.bincount(binned, weights=variance, minlength=ntheta))
        stderr[:, i, j], stderr[:, j, i] = err, err


@nb.njit(parallel=True, cache=True)
def _compute_point3D(k1ind, k2ind, kcoords, ntheta, nk1, nk2, shape,
                     samp, count, bispecbuf, binormbuf,
                     cthetabuf, countbuf, *ffts):
    kx, ky, kz = kcoords[0], kcoords[1], kcoords[2]
    Nx, Ny, Nz = shape[0], shape[1], shape[2]
    for idx in nb.prange(count):
        n, m = k1ind[samp[idx] % nk1], k2ind[samp[idx] // nk1]
        k1x, k1y, k1z = kx[n], ky[n], kz[n]
        k2x, k2y, k2z = kx[m], ky[m], kz[m]
        k3x, k3y, k3z = k1x+k2x, k1y+k2y, k1z+k2z
        if np.abs(k3x) > Nx//2 or np.abs(k3y) > Ny//2 or np.abs(k3z) > Nz//2:
            continue
        sample, norm = 0, 0
        for fft in ffts:
            s1 = fft[k1x, k1y, k1z] if k1z >= 0 \
                else np.conj(fft[-k1x, -k1y, -k1z])
            s2 = fft[k2x, k2y, k2z] if k2z >= 0 \
                else np.conj(fft[-k2x, -k2y, -k2z])
            s3 = np.conj(fft[k3x, k3y, k3z]) if k3z >= 0 \
                else fft[-k3x, -k3y, -k3z]
            temp = s1*s2*s3
            sample += temp
            norm += np.abs(temp)
        bispecbuf[idx] = sample
        binormbuf[idx] = norm
        countbuf[idx] = 1
        if ntheta > 1:
            k1dotk2 = k1x*k2x+k1y*k2y+k1z*k2z
            k1norm, k2norm = np.sqrt(k1x**2+k1y**2+k1z**2), np.sqrt(k2x**2+k2y**2+k2z**2)
            costheta = k1dotk2 / (k1norm*k2norm)
            cthetabuf[idx] = costheta


@nb.njit(parallel=True, cache=True)
def _compute_point2D(k1ind, k2ind, kcoords, ntheta, nk1, nk2, shape,
                     samp, count, bispecbuf, binormbuf,
                     cthetabuf, countbuf, *ffts):
    kx, ky = kcoords[0], kcoords[1]
    Nx, Ny = shape[0], shape[1]
    for idx in nb.prange(count):
        n, m = k1ind[samp[idx] % nk1], k2ind[samp[idx] // nk1]
        k1x, k1y = kx[n], ky[n]
        k2x, k2y = kx[m], ky[m]
        k3x, k3y = k1x+k2x, k1y+k2y
        if np.abs(k3x) > Nx//2 or np.abs(k3y) > Ny//2:
            continue
        sample, norm = 0, 0
        for fft in ffts:
            s1 = fft[k1x, k1y] if k1y >= 0 else np.conj(fft[-k1x, -k1y])
            s2 = fft[k2x, k2y] if k2y >= 0 else np.conj(fft[-k2x, -k2y])
            s3 = np.conj(fft[k3x, k3y]) if k3y >= 0 else fft[-k3x, -k3y]
            temp = s1*s2*s3
            sample += temp
            norm += np.abs(temp)
        bispecbuf[idx] = sample
        binormbuf[idx] = norm
        countbuf[idx] = 1
        if ntheta > 1:
            k1dotk2 = k1x*k2x+k1y*k2y
            k1norm, k2norm = np.sqrt(k1x**2+k1y**2), np.sqrt(k2x**2+k2y**2)
            costheta = k1dotk2 / (k1norm*k2norm)
            cthetabuf[idx] = costheta


@nb.jit(forceobj=True, cache=True)
def _printProgressBar(iteration, total, prefix='', suffix='', decimals=1,
                      length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar

    Adapted from
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    prefix = '(%d/%d)' % (iteration, total) if prefix == '' else prefix
    percent = str("%."+str(decimals)+"f") % (100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    prog = '\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)
    print(prog, end=printEnd, flush=True)
    if iteration == total:
        print()


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    N = 20
    np.random.seed(1234)
    data = np.random.rand(N, N, N)+1

    kmin, kmax = 1, 10
    result = bispectrum(data, kmin=kmin, kmax=kmax,
                        ntheta=9, progress=True, bench=True)
    bispec, bicoh, kn, theta, counts, omega = result

    print(np.nansum(bispec), np.nansum(bicoh))

    tidx = 0
    bispec, bicoh, counts = [x[tidx] for x in [bispec, bicoh, counts]]

    # Plot
    cmap = 'plasma'
    labels = [r"$|B(k_1, k_2)|$", "$b(k_1, k_2)$",
              "$arg \ B(k_1, k_2)$", "counts"]#, "counts"]
    data = [np.log10(np.abs(bispec)), np.log10(bicoh),
            np.angle(bispec), np.log10(counts)]#, np.log10(counts)]
    fig, axes = plt.subplots(ncols=2, nrows=2)
    for i in range(len(data)):
        ax = axes.flat[i]
        im = ax.imshow(data[i], origin="lower",
                       interpolation="nearest",
                       cmap=cmap,
                       extent=[kmin, kmax, kmin, kmax])
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=cax)
        cbar.set_label(labels[i])
        #if i == 0:
        #    ax.contour(data[i], colors='k', extent=[kmin, kmax, kmin, kmax])
        ax.set_xlabel(r"$k_1$")
        ax.set_ylabel(r"$k_2$")

    plt.tight_layout()

    plt.show()
