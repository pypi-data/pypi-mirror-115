import numpy as np
from miditoolkit.midi import containers
from .data import get_heat_maps, drum_names_to_pitches
from .metrics import rhythm_similarity
from .timepoints import get_rhythm_markers_by_beat


class RhythmKMeans:
    def __init__(self, cluster_centers=None):
        if cluster_centers is None:
            self.cluster_centers_ = np.zeros((0, 24))
        else:
            if type(cluster_centers) != np.ndarray:
                raise TypeError("K-means cluster centers has to be in the form of numpy.ndarray")
            elif len(cluster_centers.shape) != 2:
                raise AssertionError("K-means cluster centers has to be a 2D array")
            elif cluster_centers.shape[1] != 24:
                raise AssertionError("K-means cluster centers has to have 24 columns")
            self.cluster_centers_ = cluster_centers.copy()

    def fit(self, dataset, k, max_iter=1000, epsilon=1e-6):
        N, n_features = dataset.shape
        if n_features != 24:
            raise AssertionError("dataset has to have 24 columns")
        elif N < k:
            raise AssertionError("")
        init_indices = np.random.choice(N, size=k, replace=False)
        cluster_centers = dataset[init_indices]
        for i in range(max_iter):
            new_centers = cluster_centers.copy()
            n_points = np.ones((k, 1))

            for data in dataset:
                cluster = np.argmax(rhythm_similarity(data, cluster_centers))
                new_centers[cluster] += data
                n_points[cluster, 0] += 1

            new_centers = new_centers / n_points

            if np.mean(rhythm_similarity(new_centers, cluster_centers)) > 1 - epsilon:
                self.cluster_centers_ = new_centers
                return
            else:
                cluster_centers = new_centers

        self.cluster_centers_ = cluster_centers
        return

    def load_cluster_centers(self, cluster_centers):
        if type(cluster_centers) != np.ndarray:
            raise TypeError("K-means cluster centers has to be in the form of numpy.ndarray")
        elif len(cluster_centers.shape) != 2:
            raise AssertionError("K-means cluster centers has to be a 2D array")
        elif cluster_centers.shape[1] != 24:
            raise AssertionError("K-means cluster centers has to have 24 columns")
        self.cluster_centers_ = cluster_centers.copy()

    def k(self):
        return self.cluster_centers_.shape[0]

    def is_empty(self):
        return self.k() == 0

    def add_beat_clusters(self, midi_obj, beat_resolution=480, preprocessing='default', pitches=range(0, 128)):
        if self.is_empty():
            raise AssertionError('K-means classifier is empty. Use fit() to generate cluster centers')

        heat_maps = get_heat_maps(midi_obj, beat_resolution=beat_resolution, pitches=pitches)
        if preprocessing == 'binary':
            heat_maps = np.clip(np.ceil(heat_maps), 0., 1.)
        elif preprocessing == 'quantized':
            bins = [0, 0.5, 1.5, 2.5, 4, 5.5, 6.5, 8.5, 11]
            for i, l, r in zip(range(len(bins)), bins[:-1], bins[1:]):
                heat_maps[(heat_maps >= l) & (heat_maps < r)] = i

        for beat, heat_map in enumerate(heat_maps):
            rhythm_type = np.argmax(rhythm_similarity(heat_map, self.cluster_centers_))
            marker = containers.Marker(text=f'{preprocessing} rhythm {int(rhythm_type)}',
                                       time=beat * beat_resolution)
            midi_obj.markers.append(marker)

    def get_rhythm_scores(self, midi_obj, beat_resolution=480, pitches=range(0, 128)):
        if self.is_empty():
            raise AssertionError('K-means classifier is empty. Use fit() to generate cluster centers')

        heat_maps = get_heat_maps(midi_obj, beat_resolution=beat_resolution, pitches=pitches)
        types = np.zeros(heat_maps.shape[0])
        centers_by_beats = np.zeros((heat_maps.shape[0], 24))

        rhythm_markers_by_beat = get_rhythm_markers_by_beat(midi_obj, heat_maps.shape[0], resolution=beat_resolution)
        for i, marker in enumerate(rhythm_markers_by_beat):
            if marker is None:
                continue
            rhythm_type = int(marker.text.split(' ')[1])
            types[i] = rhythm_type
            try:
                centers_by_beats[i] = self.cluster_centers_[rhythm_type]
            except IndexError:
                pass

        return types.astype(int), rhythm_similarity(heat_maps, centers_by_beats)


class DrumRawClassifier:
    def __init__(self, n_bins=96, drums=None):
        if drums is None:
            self.drums = ["bass_drum", "closed_hihat", "snare"]
        else:
            self.drums = drums
        self.n_bins = n_bins
        self.rhythms = dict()

    def get_drum_maps(self, midi_obj, bar_resolution=1920):
        return np.stack([get_heat_maps(
            midi_obj=midi_obj,
            n_bins=self.n_bins,
            beat_resolution=bar_resolution,
            is_drum=True,
            pitches=drum_names_to_pitches[drum]
        ) for drum in self.drums], axis=1)

    def get_drum_dataset(self, midi_objs):
        dataset = np.zeros((0, len(self.drums), self.n_bins))
        for midi_obj in midi_objs:
            time_signatures = midi_obj.time_signature_changes
            if len(time_signatures) > 1:
                continue
            num = time_signatures[0].numerator
            while num % 2 == 0:
                num /= 2
            if num != 1:
                continue

            drum_maps = self.get_drum_maps(
                midi_obj=midi_obj,
                bar_resolution=midi_obj.ticks_per_beat * 4
            )
            dataset = np.concatenate((dataset, drum_maps))

        return dataset

    def fit(self, dataset, k=100, drum="all", quantize=True):
        dataset_temp = dataset.copy()

        if drum == "all":
            indices = np.arange(dataset_temp.shape[1])
        else:
            indices = np.array([self.drums.index(drum)])

        if quantize:
            for i in np.arange(16):
                dataset_temp[:, :, (i * 6 + 1):(i * 6 + 6)] = 0

        rhythm_count = dict()
        for data in dataset_temp[:, indices].reshape(dataset_temp.shape[0], len(indices) * dataset_temp.shape[2]):
            rhythm_tuple = tuple(data)
            if rhythm_tuple in rhythm_count.keys():
                rhythm_count[rhythm_tuple] += 1
            else:
                rhythm_count[rhythm_tuple] = 1

        pairs = sorted(list(rhythm_count.items()), key=lambda x: -x[1])
        self.rhythms[drum] = np.array([pair[0] for pair in pairs])[:k]

    def fit_from_midi(self, midi_objs, k_all=100, k_separate=20, quantize=True):
        dataset = self.get_drum_dataset(midi_objs)
        self.fit(dataset, k=k_all, quantize=quantize)
        for drum in self.drums:
            self.fit(dataset, k=k_separate, drum=drum, quantize=quantize)

    def add_bar_class(self, midi_obj, bar_resolution=1920, rid_empty=True):
        drum_maps = self.get_drum_maps(midi_obj, bar_resolution=bar_resolution)

        for bar, drum_map in enumerate(drum_maps.reshape(drum_maps.shape[0], len(self.drums) * self.n_bins)):
            rhythm_type = np.argmax(rhythm_similarity(drum_map, self.rhythms["all"]))
            if rid_empty:
                if np.sum(self.rhythms["all"][rhythm_type]) == 0.:
                    continue
            marker = containers.Marker(text=f'drum rhythm {int(rhythm_type)}',
                                       time=bar * bar_resolution)
            midi_obj.markers.append(marker)

    def add_separate_bar_class(self, midi_obj, bar_resolution=1920, rid_empty=True):
        drum_maps = self.get_drum_maps(midi_obj, bar_resolution=bar_resolution)

        for i_drum, drum in enumerate(self.drums):
            for bar, drum_map in enumerate(drum_maps[:, i_drum, :].reshape(drum_maps.shape[0], self.n_bins)):
                rhythm_type = np.argmax(rhythm_similarity(drum_map, self.rhythms[drum]))
                if rid_empty:
                    if np.sum(self.rhythms[drum][rhythm_type]) == 0.:
                        continue
                marker = containers.Marker(text=f'{drum} rhythm {int(rhythm_type)}',
                                           time=bar * bar_resolution)
                midi_obj.markers.append(marker)
