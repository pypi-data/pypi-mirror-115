import numpy as np
from scipy import signal
from functools import partial
from librosa import core
from librosa.feature import zero_crossing_rate
from multiprocessing import Pool

from .srh import sliding_srh_f0
from .lpc_residuals import sliding_lpc_residues
from .audio_utils import _constant_overlap_and_add, _cached_hanning_window, _sliding_frames


def _resonator_filter(frame, rho, f_cutoff, sample_rate):
    phi = 2 * np.pi * f_cutoff / sample_rate
    b = [1, 0, 0]
    a = [1, -2 * rho * np.cos(phi), rho ** 2]
    return signal.lfilter(b, a, frame)


def _frame_h1h2(frame, f0s_median, sample_rate):
    window = _cached_hanning_window(len(frame))

    out1 = _resonator_filter(frame, rho=0.97, f_cutoff=f0s_median, sample_rate=sample_rate)
    out1 /= np.max(np.abs(out1))
    out2 = _resonator_filter(frame, rho=0.8, f_cutoff=f0s_median, sample_rate=sample_rate)

    out1_windowed = window * out1
    out2_windowed = window * out2

    autocorr2 = np.correlate(out2_windowed, out2_windowed, mode='full')
    N2 = len(autocorr2)
    correction_factor = N2 / (N2 - np.arange(N2))
    autocorr2 = correction_factor * autocorr2

    max_pos = np.argmax(autocorr2)
    # max_pos = 5 if max_pos < 5 else max_pos

    f0 = round(sample_rate / max_pos)

    autocorr1 = np.correlate(out1_windowed, out1_windowed, mode='full')
    spectrogram = np.fft.fft(autocorr1, sample_rate)
    spectrogram = np.abs(spectrogram[0:sample_rate // 2])
    spectrogram /= np.sqrt(np.sum(spectrogram ** 2))
    spectrogram = 20 * np.log10(spectrogram)

    h2h1 = spectrogram[int(round(2 * f0))] - spectrogram[int(round(f0))]

    return h2h1, f0


def _get_h1h2_frames(frames, median_f0, sample_rate):
    with Pool() as pool:
        vals = pool.map(partial(_frame_h1h2, f0s_median=median_f0, sample_rate=sample_rate), frames)
    h2h1_vals, f0s = np.array(list(vals)).T
    return h2h1_vals, f0s


def sliding_h1h2(waveform, median_f0, sample_rate, window, hop):
    frames = _sliding_frames(waveform, window, hop)
    return _get_h1h2_frames(frames, median_f0, sample_rate=sample_rate)


def get_creak_features(waveform, fs, f0_min=20, f0_max=500, window=1600, hop=160,
                       use_fixed_windows=False, return_frames=False):
    '''
    Calculates H2H1 metric using RVCD - Kane, Drugman method
    Adapted from:
    https://github.com/jckane/Voice_Analysis_Toolkit/blob/a61e8d9678ecb01bde0ca9ba18e7c2050bf97431/general_fcns/GetLPCresidual.m#L20

    Process:
    Downsample to 16kHz
    LPC residual analyzed at 25ms and 5ms
    recombine residues
    Analyze srh-f0 100 ms and 10 ms and obtain median F0
    calculate h2h1 with 50ms and 10 ms

    :param waveform: Input waveform :param fs: sample rate of input waveform :param f0_min: min. threshold to analyze
    f0 :param f0_max: max. threshold to analyze f0 :param window: window size in samples, to use when return_frames
    is True :param hop: hop size in samples, to use when return_frames is True :param use_fixed_windows: If True,
    override internal window and hop sizes of various steps to be as defined by user. :param return_frames: If True,
    return metric data at length of input waveform, else, return metric in frames as per user specified window and
    hop sizes. :return: H2H1 Metric.
    '''

    # Caution: Computationally expensive for higher sample rates.
    if fs != 16000:
        waveform = core.resample(waveform, fs, 16000)
        fs = 16000
    n_coeffs = 2 + fs // 1000
    _win, _hop = window, hop

    if not use_fixed_windows:
        _win = int(25e-3 * fs)
        _hop = int(5e-3 * fs)
    residue_frames = sliding_lpc_residues(waveform, order=n_coeffs, window=_win, hop=_hop)
    residue_frames = residue_frames / np.abs(residue_frames).max()
    residues = _constant_overlap_and_add(residue_frames, hop_size=_hop)[:len(waveform)]

    if not use_fixed_windows:
        _win = int(100e-3 * fs)
        _hop = int(10e-3 * fs)
    f0s, vuvs, _ = sliding_srh_f0(residues, sample_rate=fs, window=_win, hop=_hop, f0_min=f0_min, f0_max=f0_max)
    median_f0 = f0s[(vuvs > 0.0) & (f0s > f0_min) & (f0s < f0_max)]
    median_f0 = np.median(median_f0)

    _win = int(50e-3 * fs) if not use_fixed_windows else window
    metric, f02s = sliding_h1h2(residues, median_f0, fs, window=_win, hop=_hop)
    moving_average_size = int(100e-3 * fs)
    moving_average_frame = moving_average_size // _hop

    if not use_fixed_windows:
        _win = int(20e-3 * fs)
        _hop = _win//4
    zcr = zero_crossing_rate(waveform, frame_length=_win, hop_length=_hop).squeeze(0)
    moving_avg_filter = lambda x, N: np.convolve(x, np.ones(N) / N, mode='valid')
    metric = signal.medfilt(metric, 7)
    metric = moving_avg_filter(metric, moving_average_frame)
    vuvs   = moving_avg_filter(vuvs, moving_average_frame)

    interpolate = lambda x: np.interp(np.arange(len(residues)), np.linspace(0, len(residues), len(x)), x)
    metric, f02s, vuvs, zcr = map(interpolate, [metric, f02s, vuvs, zcr])

    if return_frames:
        # Produce metrics to be of analysis window and hop
        metric, f02s, vuvs, zcr = map(partial(_sliding_frames, window=window, hop=hop), [metric, f02s, vuvs, zcr])
        metric, f02s, vuvs, zcr = map(partial(np.mean, axis=1), [metric, f02s, vuvs, zcr])

    return metric, f02s, vuvs, zcr
