# groover 0.1.2

## Installation

`groover` is a beat-by-beat rhythm feature clustering and token generation tool for `.mid` files. You can download `groover` using pip:

```shell
pip install groover
```

To check if `groover` is successfully installed, type `python` in the terminal, and do the following:

```
>>> from groover import RhythmKMeans
>>> type(RhythmKMeans())
<class 'groover.classifier.RhythmKMeans'>
```

## Documentation

### data

#### `get_heat_maps(midi_obj, n_bins=24, beat_resolution=480, rid_melody=False, is_drum=False, pitches=range(0, 128))`
Returns a numpy array of shape `(n, n_bins)`, where `n` is the number of beats in `midi_obj`. Each row is the rhythmic heat map of a beat, taking into consideration the notes' velocity and pitch.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to get heat maps from
 - `n_bins`: `int`
     - the number of bins in a beat
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `rid_melody`: `bool`
     - whether to ignore melody notes when calculating rhythmic intensity
 - `is_drum`: `bool`
     - whether drum notes are valid or non-drum notes are valid
 - `pitches`: object with method `__contains__()`, such as `list` or `set`
     - the pitches to be considered valid
    
#### `get_dataset(midi_objs, n_bins=24, beat_resolution=480, rid_melody=False, is_drum=False, pitches=range(0, 128))`
Returns a numpy array of shape `(n, n_bins)`, where `n` is the total number of beats of midi objects in `midi_objs`. Each row is the rhythmic heat map of a beat, taking into consideration the notes' velocity and pitch.
##### Parameters
 - `midi_obj`: `list`
     - the list containing midi objects to get heat maps from
 - `n_bins`: `int`
     - the number of bins in a beat
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `rid_melody`: `bool`
     - whether to ignore melody notes when calculating rhythmic intensity
 - `is_drum`: `bool`
     - whether drum notes are valid or non-drum notes are valid
 - `pitches`: object with method `__contains__()`, such as `list` or `set`
     - the pitches to be considered valid
    
### RhythmKMeans
`RhythmKMeans` classifies rhythmic heat maps and use them to predict and evaluate rhythmic tokens.

#### `RhythmKMeans.__init__(self, cluster_centers=None)`
##### Parameters
 - `cluster_centers`: `numpy.ndarray`
     - the cluster centers in the shape of `(k, 24)`, where k is the number of clusters and each row is a cluster.

#### `RhythmKMeans.load_cluster_centers(self, cluster_centers)`
Loads `cluster_centers` as the classifier's cluster centers.
##### Parameters
 - `cluster_centers`: `numpy.ndarray`
     - the cluster centers in the shape of `(k, 24)`, where k is the number of clusters and each row is a cluster.

#### `RhythmKMeans.fit(self, dataset, k, max_iter=1000, epsilon=1e-6)`
Makes the classifier's cluster centers align with the dataset.
##### Parameters
 - `dataset`: `numpy.ndarray`
     - a numpy array of shape `(n, 24)`, where `n` is the total number of beats in the dataset, with each row being the rhythmic heat map of a beat
 - `k`: `int`
     - the number of clusters to be generated
 - `max_iter`: `int`
     - the maximum number of iterations to perform
 - `epsilon`: `float`
     - if the average distance of the cluster centers between iterations is lower than `epsilon`, clustering ends early

#### `RhythmKMeans.k(self)`
Returns the number of clusters of the classifier.

#### `RhythmKMeans.is_empty(self)`
Returns `True` if the classifier is not fitted to any data yet, `False` otherwise.

#### `RhythmKMeans.add_beat_clusters(self, midi_obj, beat_resolution=480, preprocessing='default', pitches=range(0, 128))`
Adds markers with rhythm types to `midi_obj`.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to add beat-by-beat rhythm markers to
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `preprocessing`: `str`
     - can be either `'default'`, `'binary'`, or `'quantized'`, which will then change the rhythmic heat maps' values accordingly
 - `pitches`: object with method `__contains__()`, such as `list` or `set`
     - the pitches to be considered valid

#### `RhythmKMeans.get_rhythm_scores(self, midi_obj, beat_resolution=480, pitches=range(0, 128))`
Returns a tuple of numpy arrays. The first is the rhythm types in shape `(n,)` that is specified by the markers in the midi object, and the second array is the alignment score between the notes and the rhythm type in shape `(n,)`. `n` is the number of beats in the midi object
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to be evaluated
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `preprocessing`: `str`
     - can be either `'default'`, `'binary'`, or `'quantized'`, which will then change the rhythmic heat maps' values accordingly
 - `pitches`: object with method `__contains__()`, such as `list` or `set`
     - the pitches to be considered valid

### DrumRawClassifier
`DrumRawClassifier` classifies drum heat maps and use them to predict and evaluate rhythmic tokens.

#### `DrumRawClassifier.__init__(self, n_bins=96, drums=None)`
##### Parameters
 - `n_bins`: `int`
     - the number of bins in each bar
 - `drums`: `list`
     - the list of drums that will be used, options are `['bass_drum', 'closed_hihat', 'crash', 'floor_tom', 'open_hihat', 'ride', 'snare', 'tambourine', 'tom']`
     - is set to `['bass_drum', 'closed_hihat', 'snare']` by default

#### `DrumRawClassifier.fit_from_midi(self, midi_objs, k_all=100, k_separate=20, quantize=True)`
Makes the classifier's rhythm classes align with the dataset.
##### Parameters
 - `midi_objs`: `list`
     - the list containing midi objects to get drum heat maps from
 - `k_all`: `int`
     - the number of composite rhythm types to be generated
 - `k_separate`: `int`
     - the number of drum-by-drum rhythm types to be generated for each drum type
 - `quantize`: `True`
     - if `quantize` is set to `True`, then drum notes that are not on the 16th note time will be disregarded
   
#### `DrumRawClassifier.add_composite_bar_class(self, midi_obj, rid_empty=True)`
Adds markers with composite drum rhythm types to `midi_obj`.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to add bar-by-bar drum rhythm markers to
 - `rid_empty`: `bool`
     - if `rid_empty` is set to `True`, then rhythm types with no drum notes will not be added as a marker
   
#### `DrumRawClassifier.add_separate_bar_class(self, midi_obj, rid_empty=True)`
Adds markers with separate drum rhythm types to `midi_obj`.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to add bar-by-bar drum rhythm markers to
 - `rid_empty`: `bool`
     - if `rid_empty` is set to `True`, then rhythm types with no drum notes will not be added as a marker