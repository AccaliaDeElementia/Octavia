#!/usr/bin/env python2
from warnings import warn
import sys

import music21
import fluidsynth
import pyaudio
import numpy as np

import Markov

class Note(object):
    def __eq__(self, other):
        if isinstance(other, Note):
            return (self.tones == other.tones
                    and self.duration == other.duration)
        return False
    def __ne__(self, other):
        if isinstance(other, Note):
            return (self.tones != other.tones
                    or self.duration != other.duration)
        return True
    def __lt__(self, other):
        if isinstance(other, Note):
            if self.tones < other.tones:
                return True
            else:
                return self.duration < other.duration
        return False
    def __le__(self, other):
        if isinstance(other, Note):
            if self.tones < other.tones:
                return True
            else:
                return self.duration <= other.duration
        return False
    def __gt__(self, other):
        if isinstance(other, Note):
            if self.tones > other.tones:
                return True
            else:
                return self.duration > other.duration
        return True
    def __ge__(self, other):
        if isinstance(other, Note):
            if self.tones > other.tones:
                return True
            else:
                return self.duration >= other.duration
        return True
    def __hash__(self):
        return hash(self.tones) ^ hash(self.duration)
    def __init__(self, tones, duration):
        self.tones = tuple(tones)
        self.duration = duration

class Composer(object):
    def __iter__(self):
        if not self.__chain.has_data():
            return
        quarters = 0
        for note in self.__chain:
            if self.__finite and quarters > self.__quarters:
                break
            quarters += note.duration
            yield note

    def __init__(self, initial=None, quarters=None, accuracy=2,
                 rests=sys.maxint):
        self.__chain = Markov.InfiniteChain(chain=accuracy)
        self.__finite = quarters != None
        self.__quarters = quarters
        self.__rests = rests
        if initial:
            for file_ in initial:
                self.add(file_)

    def add(self, input_):
        music = music21.converter.parse(input_)
        for part in music.parts:
            notes = []
            for note in part.notes:
                tones = getattr(note, 'pitches', [])
                if tones:
                    tones = [tone.midi for tone in tones]
                    length = note.quarterLength
                else:
                    length = min(note.quarterLength, self.__rests)
                notes.append(Note(tones, length))
            self.__chain.insert(notes)

class Synth(object):
    def __init__(self, soundfont, notes, bpm=60, impact=70):
        synth = fluidsynth.Synth()
        sfid = synth.sfload(soundfont)
        synth.program_select(0, sfid, 0, 0)
        self.__notes = notes
        self.__synth = synth
        self.__bpm = bpm
        self.__impact = impact

    def play(self):
        player = pyaudio.PyAudio()
        stream = player.open(format=pyaudio.paInt16, channels=2,
                             rate=44100, output=True)
        tempo = 44100*60/self.__bpm
        for note in self.__notes:
            samp = []
            duration = int(tempo*note.duration)
            for tone in note.tones:
                self.__synth.noteon(0, tone, self.__impact)
            samp = np.append(samp, self.__synth.get_samples(duration))
            for tone in note.tones:
                self.__synth.noteoff(0, tone)
            stream.write(samp.astype(np.int16).tostring())

class Octavia(object):
    def __init__(self, inputs, soundfont, bpm=60, length=300,
                 impact=70, track=0, accuracy=2, rests=sys.maxint):
        for str_ in inputs:
            if not isinstance(str_, (str, unicode)):
                raise TypeError('inputs must be a sequence of strings')
        if not isinstance (soundfont, (str, unicode)):
            raise TypeError('soundfont must be a string')
        if not isinstance (bpm, (int, float)):
            raise TypeError('bpm must be a number')
        elif bpm <= 0:
            raise ValueError('bpm must be a positive number')
        elif bpm > 500:
            warn('bpm is larger than 500, this is probably an error')
        if length != None and not isinstance(length, (int, float)):
            raise TypeError('length must be None or a number')
        elif length != None and length <= 0:
            raise ValueError('length must be None or a positive number')
        if not isinstance(impact, int):
            raise TypeError('impact nust be of type int')
        elif impact < 0 or impact > 100:
            raise ValueError('impact must be between 0 and 100')
        if not isinstance(track, int):
            raise TypeError('track must be of type int')
        elif track < 0:
            raise ValueError('track must be non-negative')
        if not isinstance(accuracy, int):
            raise TypeError('accuracy must be of type int')
        elif accuracy < 1:
            raise ValueError('accuracy must be positive')
        elif accuracy > 10:
            warn('Accuracy is unusually high,' +
                ' this is probably an error')
        if not isinstance(rests, int):
            raise TypeError('rests must be of type int')
        elif rests < 1:
            raise ValueError('rests must be positive')
        locals_ = locals()
        for name in locals_:
            setattr(self, name, locals_[name])
        self.composer = Composer(quarters=bpm*length/60,
                                accuracy=accuracy, rests=rests)
        for input_ in inputs:
            self.composer.add(input_)

    def play(self):
        synth = Synth(soundfont=self.soundfont, notes=self.composer,
                      bpm=self.bpm, impact=self.impact)
        synth.play()

if __name__ == '__main__':
    import argparse

    def getargs():
        parser = argparse.ArgumentParser()
        parser.add_argument('inputs', type=str, nargs='+',
            metavar='musicfile',
            help='The music file to source music from')
        parser.add_argument('soundfont', type=str, metavar='soundfont',
            help='The soundfont (.SF2) file to use for playback')
        parser.add_argument('-b', '--bpm', type=int, default=60,
            dest='bpm', metavar='BPM',
            help='Set the playback speed')
        parser.add_argument('-l', '--length', type=float, default=300.,
            metavar='seconds', help='Set playback length in seconds')
        parser.add_argument('-i', '--impact', type=int,
            default=70, help='Set the playback \'impact\' (volume)')
        parser.add_argument('-t', '--track', type=int, default=0,
            metavar='id',
            help='Set the track id to play from soundfont')
        parser.add_argument('-a', '--accuracy', type=int, default=2,
            help='Set the accuracy of the reproduction '+
                 '(highter = more accurate)')
        parser.add_argument('-r', '--rests', type=int,
        default=sys.maxint, help='Maximum rest length')
        return vars(parser.parse_args())
    args = getargs()
    octavia = Octavia (**args)
    octavia.play()
