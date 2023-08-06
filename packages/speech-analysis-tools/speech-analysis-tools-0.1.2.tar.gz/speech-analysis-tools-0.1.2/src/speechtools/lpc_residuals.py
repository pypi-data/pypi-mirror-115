import numpy as np
from surfboard.utils import metric_slidingwindow
from librosa import core
from scipy import signal

from .audio_utils import _check_and_pad_waveform, _cached_hanning_window


def _lpc_residual(frame, order=24, normalize_power=False):
    """Compute LPC residual from a hanning windowed frame"""
    window = _cached_hanning_window(len(frame))
    windowed_frame = window * frame
    a = core.lpc(windowed_frame, order)
    residue = signal.lfilter(a, 1, windowed_frame)

    if normalize_power:
        residue *= np.sqrt(np.sum(windowed_frame**2)/np.sum(residue**2))

    return residue


def sliding_lpc_residues(waveform, order=24, window=1024, hop=256, normalize_power=False):
    # Prevent dropping trailing frames
    waveform = _check_and_pad_waveform(waveform, window, hop)
    @metric_slidingwindow(frame_length=window, hop_length=hop, truncate_end=True)
    def _frame_lpc_residue(frame, order, normalize_power=False):
        return _lpc_residual(frame, order=order, normalize_power=normalize_power)

    return _frame_lpc_residue(waveform, order, normalize_power).squeeze(0)
