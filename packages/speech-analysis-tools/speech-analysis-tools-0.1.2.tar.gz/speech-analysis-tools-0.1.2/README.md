# Resemble Speech Tools

This package contains collated tools for quantifying issues in speech clips.

The repo currently has support for detecting vocal fry (H2H1 metric proposed by Kane-Drugman):

#### Usage:
`from speechtools.metrics import get_creak_features`


`get_creak_features(waveform, fs, f0_min=20, f0_max=500, window=1600, hop=160,
                       use_fixed_windows=False, return_frames=False`

##### Special Parameters
- `use_fixed_frames`: This needs to be `True` if user wants to override internally used `window` and `hop` sizes. If `False`, the default window and hop sizes specified by the KaneDrugman papers are used for analysis.
- `return_frames`: When `False` the resulting metric is interpolated to be of `waveform` length.

   
## Miscellaneous
There are also a few private functions bundled in for signal processing under `speechtools.audio_utils`:
- Splitting up the signal into chunks of `win_length` strided by `hop_size`
- Obtaining frame level LPC residuals


#### Papers:
1. Kane, J., Drugman, T., Gobl, C., (2013) "Improved automatic 
       detection of creak", 27(4), pp. 1028-1047, Computer Speech and Language.
2. Drugman, T., Kane, J., Gobl, C. (2012) "Resonator-based creaky voice detection", 
	       Proceedings of Interspeech.