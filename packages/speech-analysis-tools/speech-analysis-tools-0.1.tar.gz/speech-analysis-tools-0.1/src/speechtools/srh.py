from functools import partial
import numpy as np
from multiprocessing import Pool

from . import VOICING_DECISION_THRESHOLD, SRH_ITERS
from .audio_utils import _cached_blackman_window, _sliding_frames


def _srh_f0(frame, sample_rate, f0_min=20, f0_max=600, n_harmonics=5):
    window = _cached_blackman_window(len(frame))
    windowed_frame = window * frame
    windowed_frame -= np.mean(windowed_frame)

    spectrum = np.fft.fft(windowed_frame, sample_rate)
    spectrum = np.abs(spectrum[:sample_rate // 2])
    if (spectrum > 0).any():
        spectrum /= np.sqrt(np.sum(spectrum ** 2))

    srh = np.zeros((f0_max))
    # SRH Spectral Criterion
    for f in range(f0_min, f0_max):
        a_freqs = sum(spectrum[(i + 1) * f] for i in range(n_harmonics))
        b_freqs = sum([spectrum[round((i - 0.5) * f)] for i in range(2, n_harmonics)])
        srh[f] = a_freqs - b_freqs

    f0 = np.argmax(srh)
    srh_max = srh[f0]
    return f0, srh_max


def _get_f0_frames(frames, sample_rate, f0_min=20, f0_max=400):
    f_min, f_max = f0_min, f0_max

    with Pool() as pool:
        # According to paper, the computation is repeated twice. SRH_ITERS == 2 by default
        for idx in range(SRH_ITERS):
            vals = pool.map(partial(_srh_f0, sample_rate=sample_rate, f0_min=f_min, f0_max=f_max), frames)
            freqs, srh_vals = np.array(list(vals)).T
            tmp_position = np.argwhere(srh_vals > 0.1)
            f0s = freqs[tmp_position]

            if len(f0s) > 0:
                # ToDo: Mean and Median are very close here, but mean could be more accurate (not tried)
                median_f0 = np.median(f0s)
                f_min, f_max = map(lambda x: int(round(x)), [0.5 * median_f0, 2 * median_f0])

    uv_threshold = 0.085 if np.std(srh_vals) > 0.05 else VOICING_DECISION_THRESHOLD
    vuvs = (srh_vals > uv_threshold).astype(int)
    return freqs, vuvs, srh_vals


def sliding_srh_f0(waveform, sample_rate, f0_min=20, f0_max=400, window=1024, hop=256):
    frames = _sliding_frames(waveform, window, hop)
    return _get_f0_frames(frames, sample_rate, f0_min, f0_max)