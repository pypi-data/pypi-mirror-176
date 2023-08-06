import torch
import muspy
import numpy as np
import pandas as pd
from torch.nn.functional import one_hot

__all__ = ["Compose", "FixEmptyMeasures", "Factorize", "Quantize"]


class Compose:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, midi):
        for t in self.transforms:
            midi = t(midi)
        return midi


class FixEmptyMeasures:
    def __init__(self, resolution):
        self.resolution = resolution

    def __call__(self, data):
        # data shape: [num_measures, resolution]
        for measure in data:
            if len(measure[measure < 128]) == 0:
                measure[0] = 60
        return data


class Factorize:
    def __init__(self, ctxt_split=(6, 4, 6), resolution=24):
        self.ctxt_split = ctxt_split
        self.resolution = resolution

    def __call__(self, data):
        data = torch.Tensor(data).squeeze(0)
        if len(self.ctxt_split) == 1:
            re = self.factorize(data, self.resolution)
            re = [x.squeeze(0) for x in re]
        elif len(self.ctxt_split) == 3:
            past, middle, future = data.split(self.ctxt_split)
            past_x = self.factorize(past, self.resolution)
            middle_x = self.factorize(middle, self.resolution)
            future_x = self.factorize(future, self.resolution)
            re = {
                "inpaint_gd_whole": middle_x[4].contiguous().view(-1),  # middle_gd
                "past_x": past_x,
                "middle_x": middle_x,
                "future_x": future_x,
            }
        return re

    def factorize(self, data, resolution):
        data = data.reshape(-1)
        ones = torch.ones_like(data) * 127
        rx = torch.where(data < 128, ones, data) - 126
        nrx = torch.stack(
            one_hot((rx - 1).to(torch.int64), num_classes=3).split(resolution)
        )
        rx = torch.stack(rx.split(resolution))
        gd = torch.stack(data.split(resolution))
        len_x = torch.Tensor([len(m[m < 128]) for m in gd])
        px = [m[m < 128] for m in gd]
        px = torch.stack(
            [torch.cat((x, torch.ones(resolution - len(x)) * 128)) for x in px]
        )
        return [
            px.to(torch.long),
            rx.to(torch.float),
            len_x.to(torch.long),
            nrx.to(torch.float),
            gd.to(torch.long),
        ]

class StandardizedNote:
    def __init__(self, note, track, data, ticks_per_beat):
        self.track = track
        self.time = self.scaled_time(note, ticks_per_beat, data.resolution)
        self.relative_position = self.rel_pos(
            note.time, ticks_per_beat, data.barlines, data.resolution
        )
        self.duration = self.scaled_duration(note, ticks_per_beat, data.resolution)
        self.pitch = note.pitch
        self.velocity = note.velocity
        self.tempo = self.get_tempo(note, data.tempos)
        self.time_signature = self.get_time_signature(note, data.time_signatures)
        self.ticks_per_measure = self.get_ticks_per_measure(ticks_per_beat)
        self.measure = self.get_measure(note, data.barlines)

    def get_measure(self, note, barlines):
        measure = len(barlines) - len([m for m in barlines if note.time < m.time]) - 1
        return measure

    def scaled_time(self, note, ticks_per_beat, resolution):
        return round(note.time * ticks_per_beat / resolution) / ticks_per_beat

    def scaled_duration(self, note, ticks_per_beat, resolution):
        return round(note.duration * ticks_per_beat / resolution) / ticks_per_beat

    def get_tempo(self, note, tempos):
        last_tempo = sorted(
            [tempo for tempo in tempos if note.time >= tempo.time], key=lambda x: x.time
        )[-1]
        return last_tempo.qpm

    def get_time_signature(self, note, time_signatures):
        last_ts = sorted(
            [ts for ts in time_signatures if note.time >= ts.time], key=lambda x: x.time
        )[-1]
        return last_ts.numerator, last_ts.denominator

    def get_ticks_per_measure(self, ticks_per_beat):
        return int(self.time_signature[0] * 4 / self.time_signature[1])

    def rel_pos(self, time, ticks_per_beat, barlines, resolution):
        lower_time = [bar.time for bar in barlines if bar.time - time <= 0][-1]
        return round((time - lower_time) * ticks_per_beat / resolution) / ticks_per_beat



class Note:
    def __init__(self, row, ticks_per_note):
        self.track = int(row["track"])
        self.measure = int(row["measure"])
        self.rel_pos = round(row["relative_position"] * ticks_per_note)
        self.duration = round(row["duration"] * ticks_per_note)
        self.pitch = int(row["pitch"])
        self.velocity = int(row["velocity"])
        self.tempo = int(row["tempo"])

    def to_noteseq(self):
        return np.array([self.pitch] + [128] * (self.duration - 1))

    def to_remi(self):
        return np.array(
            [
                self.measure,
                self.rel_pos,
                self.duration,
                self.pitch,
                self.velocity,
                self.tempo,
            ]
        )

class Quantize:
    def __init__(self, ticks_per_beat):
        self.ticks_per_beat = ticks_per_beat


    def __call__(self, data):
        if len(data.tempos) == 0:
            data.tempos = [muspy.Tempo(time=0.0, qpm=120)]

        data.infer_barlines()
        notes = [
            StandardizedNote(
                note,
                i,
                data,
                self.ticks_per_beat,
            )
            for i, track in enumerate(data.tracks)
            for note in track.notes
        ]

        notes = [
            [
                note.track,
                note.measure,
                note.time,
                note.relative_position,
                note.duration,
                note.pitch,
                note.velocity,
                note.tempo,
                f"{note.time_signature[0]}/{note.time_signature[1]}",
                note.ticks_per_measure,
            ]
            for note in notes
        ]

        df = pd.DataFrame(
            columns=[
                # "resolution",
                "track",
                "measure",
                "time",
                "relative_position",
                "duration",
                "pitch",
                "velocity",
                "tempo",
                "time_signature",
                "ticks_per_measure",
            ],
            data=notes,
        )
        return df

class NoteSeq:
    def __init__(self, ticks_per_note):
        self.ticks_per_note = ticks_per_note
    
    def __call__(self, df):
        overflow = []
        # groups = df.groupby(by=["track", "measure"]).groups.items()
        last_measures = df.groupby("track").max()["measure"].tolist()
        tracks_ids = list(df.groupby("track").groups.keys())
        tracks = [[] for x in tracks_ids]
        groups = [range(last_measures[track] + 1) for track in tracks_ids]
        for track_ix, measures in enumerate(groups):
            track_df = df[df["track"] == track_ix]
            for m in measures:
                seq = [129 for _ in range(self.ticks_per_note * 4)]
                notes_df = track_df[track_df["measure"] == m]
                if len(notes_df) <= 0:
                    i = 0
                    while len(overflow) > 0:
                        if i >= self.ticks_per_note * 4:
                            break
                        else:
                            seq[i] = overflow.pop(0)
                            i += 1
                else:
                    for note in notes_df.iterrows():
                        n = Note(note[1], self.ticks_per_note)
                        noteseq = n.to_noteseq()
                        # if noteseq se paso pal compas del lado
                        i = 0
                        while len(overflow) > 0:
                            if i >= self.ticks_per_note * 4:
                                break
                            else:
                                seq[i] = overflow.pop(0)
                                i += 1
                        for i, ix in enumerate(range(n.rel_pos, n.rel_pos + n.duration)):
                            if ix >= self.ticks_per_note * 4:
                                overflow.append(noteseq[i])
                            else:
                                seq[ix] = noteseq[i]

                tracks[track_ix].append(np.array(seq))
        return np.array(tracks, dtype="object")
