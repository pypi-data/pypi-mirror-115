from functools import lru_cache
import numpy as np
from scipy import signal
from surfboard.utils import metric_slidingwindow


@lru_cache(maxsize=None)
def _cached_boxcar_window(frame_len):
    return signal.windows.boxcar(frame_len)


@lru_cache(maxsize=None)
def _cached_hanning_window(frame_len):
    return signal.windows.hann(frame_len)


@lru_cache(maxsize=None)
def _cached_blackman_window(frame_len):
    return signal.windows.blackman(frame_len)


def _check_and_pad_waveform(waveform, window, hop):
    # Pad an extra frame if needed, to prevent loss of trailing frames
    n_overlap = window - hop
    wave_len = len(waveform)
    remainder_samples = (wave_len - n_overlap) % (window - n_overlap)
    padding = hop - remainder_samples
    if padding > 0:
        waveform = np.concatenate((waveform, np.zeros(padding)))
    return waveform


def _constant_overlap_and_add(frames, hop_size):
    # Constant Overlap Add
    result = np.array([])
    window = _cached_boxcar_window(frames[0].shape[0])
    assert signal.check_COLA(window, len(window), len(window)-hop_size), "COLA check failed for window, " \
                                                                         "during reconstruction"
    for idx, frame in enumerate(frames):
        windowed_frame = frame * window
        if idx == 0:
            result = windowed_frame
        else:
            result = np.concatenate((result, np.zeros(hop_size)))
            result[idx*hop_size:] += windowed_frame[:]
    return result


def _sliding_frames(waveform, window, hop):
    waveform = _check_and_pad_waveform(waveform, window, hop)
    @metric_slidingwindow(window, hop, truncate_end=True)
    def _wave_frames(frame):
        return frame
    return _wave_frames(waveform).squeeze(0)