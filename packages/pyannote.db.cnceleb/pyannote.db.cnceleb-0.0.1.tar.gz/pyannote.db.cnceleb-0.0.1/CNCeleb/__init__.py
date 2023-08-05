#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017-2020 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

import pandas as pd
from pathlib import Path
from pyannote.core import Segment, Timeline, Annotation
from pyannote.database import Database
from pyannote.database.protocol import SpeakerVerificationProtocol


class CNCeleb2(SpeakerVerificationProtocol):
    def trn_iter(self):

        path = Path(__file__).parent / "data"
        path = path / f"cnceleb2_duration.txt.gz"
        content = pd.read_table(
            path, names=["uri", "duration"], index_col="uri", delim_whitespace=True
        )

        for uri, duration in content.itertuples():

            speaker = uri.split("/")[0]
            speaker = f"CNCeleb_{speaker}"

            segment = Segment(0, duration)

            annotation = Annotation(uri=uri)
            annotation[segment] = speaker

            annotated = Timeline(segments=[segment], uri=uri)

            yield {
                "uri": uri,
                "database": "CNCeleb",
                "annotation": annotation,
                "annotated": annotated,
            }

    def dev_iter(self):
        raise NotImplementedError("This protocol does not define a development set.")

    def dev_try_iter(self):
        raise NotImplementedError(
            "This protocol does not define trials on the development set."
        )

    def tst_iter(self):
        raise NotImplementedError("This protocol does not define a test set.")

    def tst_try_iter(self):
        raise NotImplementedError(
            "This protocol does not define trials on the test set."
        )


class CNCeleb(Database):
    """CNCeleb

    References
    ----------
    CN-CELEB: a challenging Chinese speaker recognition dataset},
    Fan, Yue and Kang, JW and Li, LT and Li, KC and Chen, HL and Cheng, ST and Zhang, PY and Zhou, ZY and Cai, YQ and Wang, Dong
    2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)
    """

    def __init__(self, **kwargs):
        super(CNCeleb, self).__init__(**kwargs)
        self.register_protocol("SpeakerVerification", "CNCeleb", CNCeleb2)


from . import _version

__version__ = _version.get_versions()["version"]

