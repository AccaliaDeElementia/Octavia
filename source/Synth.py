#!/usr/bin/env python2

import music21
import fluidsynth
import pyaudio
import numpy as np

import Markov

class Synth(object):
    class Note(object):
        def __hash__(self):
            return hash(self.tones) ^ hash(self.duration)
        def __init__(self, tones, duration):
            self.tones = tones
            self.duration = duration
    def __init__(self):
        pass
    def load_music(self, input_):
        chain = Markov.InfiniteChain()
        music = music21.converter.parse(input_)
        for part in music.parts:
            notes = []
            for note in part.notes:
                tones = getattr(note, 'pitches', ())
                if tones:
                    tones = tuple(tone.midi for tone in tones)
                length = note.quarterLength
                notes.append(self.Note(tones, length))
            chain.insert(notes)
        self.__chain = chain

    def play_music(self, soundfont, bpm=60):
        synth = fluidsynth.Synth()
        sfid = synth.sfload(soundfont)
        synth.program_select(0, sfid, 0, 0)
        player = pyaudio.PyAudio()
        stream = player.open(format=pyaudio.paInt16, channels=2,
                             rate=44100, output=True)
        tempo = 44100*60/bpm
        for note in self.__chain:
            samp = []
            duration = int(tempo*note.duration)
            for tone in note.tones:
                synth.noteon(0, tone, 100)
            samp = np.append(samp, synth.get_samples(duration))
            for tone in note.tones:
                synth.noteoff(0, tone)
            stream.write(samp.astype(np.int16).tostring())


if __name__ == '__main__':
    print ('Running self test')
    synth = Synth()
    #synth.load_music('../resources/music/lilium.midi')
    synth.load_music('../resources/music/jsbach_bwv578.midi')
    synth.play_music('../resources/soundfonts/GrandPiano.SF2')
