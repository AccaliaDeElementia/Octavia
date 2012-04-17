#!/usr/bin/env python2

import music21
import fluidsynth
import pyaudio
import numpy as np

import Markov
class Note(object):
    def __eq__(self, other):
        if isinstance(other, Note):
            return self.tones == other.tones and self.duration == other.duration
        return False
    def __ne__(self, other):
        if isinstance(other, Note):
            return self.tones != other.tones or self.duration != other.duration
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

    def __init__(self, initial=None, quarters=None, accuracy=2):
        self.__chain = Markov.InfiniteChain(chain=accuracy)   
        self.__finite = quarters != None
        self.__quarters = quarters
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


if __name__ == '__main__':
    print ('Running self test')
    Synth(soundfont='../resources/soundfonts/GrandPiano.SF2',
          notes=Composer(initial=['../resources/music/lilium.midi'],
                     quarters=120*2, accuracy=2),
          bpm=120,impact=90
         ).play()
