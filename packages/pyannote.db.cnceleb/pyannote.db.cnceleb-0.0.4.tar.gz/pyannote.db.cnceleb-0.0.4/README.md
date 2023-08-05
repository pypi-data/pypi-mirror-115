# CN-Celeb plugin for pyannote.database

This package provides an implementation of the speaker verification protocols used in the `CNCeleb` paper.

## Citation

Please cite the following reference if your research relies on the `CNCeleb` dataset:

```bibtex
@inproceedings{fan2020cn,
  title={CN-CELEB: a challenging Chinese speaker recognition dataset},
  author={Fan, Yue and Kang, JW and Li, LT and Li, KC and Chen, HL and
          Cheng, ST and Zhang, PY and Zhou, ZY and Cai, YQ and Wang, Dong},
  booktitle={ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages={7604--7608},
  year={2020},
  organization={IEEE}
}
```

Please cite the following references if your research relies on this package. This is where the whole `pyannote.database` framework was first introduced:

```bibtex
@inproceedings{pyannote.metrics,
  author = {Herv\'e Bredin},
  title = {{pyannote.metrics: a toolkit for reproducible evaluation, diagnostic, and error analysis of speaker diarization systems}},
  booktitle = {{Interspeech 2017, 18th Annual Conference of the International Speech Communication Association}},
  year = {2017},
  month = {August},
  address = {Stockholm, Sweden},
  url = {http://pyannote.github.io/pyannote-metrics},
}
```

## Installation

* Install this package

```bash
$ pip install pyannote.db.cnceleb
```

* [Download CN-Celeb dataset](http://www.openslr.org/82/) to obtain this kind of directory structure:

```
/path/to/CN-Celeb/CN-Celeb_flac/data/id00001/entertainment-01-001.flac
...
/path/to/CN-Celeb/CN-Celeb2_flac/data/id10000/vlog-01-001.flac
...
```

* Update [`~/.pyannote/database.yml`](https://github.com/pyannote/pyannote-database) to look like this:

```yaml
Databases:
  CNCeleb:
    - /path/to/CN-Celeb/CN-Celeb_flac/data/{uri}.flac
    - /path/to/CN-Celeb/CN-Celeb2_flac/data/{uri}.flac
```

## Usage

```python
from pyannote.database import get_protocol
protocol = get_protocol('CNCeleb.SpeakerVerification.CNCeleb')
```

One can use `protocol.train` generator to train the background model.

```python
for training_file in protocol.train():
    uri = training_file['uri']
    print('Current filename is {0}.'.format(uri))

    # "who speaks when" as a pyannote.core.Annotation instance
    annotation = training_file['annotation']
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        print('{0} speaks between t={1:.1f}s and t={2:.1f}s.'.format(
            speaker, segment.start, segment.end))
   
    break  # this should obviously be replaced
           # by the actual background training
```
