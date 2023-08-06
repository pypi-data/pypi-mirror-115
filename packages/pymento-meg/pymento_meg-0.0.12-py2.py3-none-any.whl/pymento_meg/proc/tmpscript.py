import mne
import pandas as pd
from pathlib import Path
from pymento_meg.config import reject_criteria
from pymento_meg.proc.bids import get_events
from pymento_meg.utils import (
    _plot_evoked_fields,
    _get_channel_subsets,
)
from pymento_meg.proc.artifacts import remove_eyeblinks_and_heartbeat
from pymento_meg.proc.bids import get_events
from autoreject import (
    AutoReject,
    get_rejection_threshold
)

import mne
from mne.preprocessing import (
    create_ecg_epochs,
    create_eog_epochs,
    ICA,
)
from autoreject import (
    get_rejection_threshold
)

from pymento_meg.utils import _construct_path
from pathlib import Path

import matplotlib
matplotlib.use('QT5Agg')

subject = '007'
figdir = '/tmp/figs'

raw = mne.io.read_raw_fif('memento-sss/sub-007/meg/sub-007_task-memento_proc-sss_meg.fif')
raw.crop(tmin=0, tmax=1000)
raw.load_data()
raw.filter(l_freq=0.5, h_freq=40)

# estimate rejection criteria for high-amplitude artifacts from artificial
# events
tstep = 1.0
events = mne.make_fixed_length_events(raw, duration=tstep)
epochs = mne.Epochs(raw, events, tmin=0.0, tmax=tstep, baseline=(0, 0))
reject = get_rejection_threshold(epochs)
# DO ICA HERE
remove_eyeblinks_and_heartbeat(raw, subject, figdir, reject, epochs, tstep)
events, event_dict = get_events(raw)
epochs = mne.Epochs(raw, events, event_dict, tmin=-0.5, tmax=0.5, picks='meg')




epochs.load_data()
ar = AutoReject()
epochs_clean = ar.fit_transform(epochs)

