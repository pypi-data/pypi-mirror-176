import torch
import muspy
import numpy as np
import pandas as pd
from torch.nn.functional import one_hot

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
                notes_df = track_df[track_df["measure"] == m]
                #time_signature = notes_df.iloc[0]["time_signature"].item()
                #num, den = time_signature.split("/")
                
                seq = [129 for _ in range(self.ticks_per_note * 4 * (num/den))]
                
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
