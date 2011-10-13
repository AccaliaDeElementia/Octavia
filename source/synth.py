#!/usr/bin/env python2
from threading import Thread
import Queue
import music21
import fluidsynth
import numpy
import pyaudio
import Markov

class Octavia (object):
    class __Player (Thread):
        def __init__(self, queue, sample_rate):
            Thread.__init__(self)
            self.__queue = queue
            self.__sample_rate = sample_rate

        def run(self):
            player = pyaudio.PyAudio()
            stream = player.open(format=pyaudio.paInt16, channels=2,
                                 rate=self.__sample_rate, output=True)
            try:
                while True:
                    sample = self.__queue.get(timeout=5.0)
                    stream.write(sample.astype(numpy.int16).tostring())
                    self.__queue.task_done()
            except Queue.Empty:
                pass
    class __Sequencer (Thread):
        def __init__ (self, queue, midi, soundfont, 
                      note_duration, note_fadeout, note_impact,
                      sample_rate, song_length):
            def get_notes():
                res = []
                for part in music.parts:
                    pitches = lambda n: (tuple(p.midi for p in n.pitches) 
                                         if 'pitches' in dir(n) else ())
                    duration = lambda n: n.duration.quarterLength
                    res.append([(pitches(note),duration(note)) 
                                for note in part.notes])
                return res
            Thread.__init__(self)
            self.__queue = queue
            music = music21.converter.parse(midi)
            notes = get_notes()
            num_notes = int(song_length * (note_duration + 
                            note_duration * note_fadeout) ** -1)
            self.__chain = Markov.FiniteChain(chain=6,limit=num_notes)
            for part in notes:
                self.__chain.insert(part)
            self.__soundfont = soundfont
            self.__duration = int(sample_rate * note_duration)
            self.__fadeout = int(note_duration*note_fadeout)
            self.__note_impact = note_impact

        def run(self):
            duration = self.__duration
            fadeout = self.__fadeout
            synth = fluidsynth.Synth()
            sfid = synth.sfload(self.__soundfont)
            synth.program_select(0, sfid, 0, 0)
            for note in self.__chain:
                nduration = int(duration * note[1])
                sample = []
                for part in note[0]:
                    synth.noteon(0, part, self.__note_impact)
                sample = numpy.append(sample, synth.get_samples(nduration))
                for part in note[0]:
                    synth.noteoff(0, part)
                self.__queue.put(sample)

    def __init__ (self, midi, soundfont, note_duration=.2, note_fadeout=.1,
                        note_impact=.9, sample_rate=44100, song_length=60):
        self.__midi = midi
        self.__soundfont = soundfont
        self.__note_duration = note_duration
        self.__note_fadeout = note_fadeout
        self.__note_impact = int(100. * note_impact)
        self.__sample_rate = sample_rate
        self.__song_length = song_length

    def play(self):
        queue = Queue.Queue(100)
        synth_opts = {
            'queue': queue,
            'midi': self.__midi,
            'soundfont': self.__soundfont,
            'note_duration': self.__note_duration,
            'note_fadeout': self.__note_fadeout,
            'note_impact': self.__note_impact,
            'sample_rate': self.__sample_rate,
            'song_length': self.__song_length,
        }
        synth = self.__Sequencer(**synth_opts)
        player_opts = {
            'queue': queue,
            'sample_rate': self.__sample_rate,
        }
        player = self.__Player(**player_opts)
        synth.start()
        player.start()
        synth.join()
        player.join()

if __name__ == '__main__':
    o = Octavia('../resources/music/lilium.midi', '../resources/soundfonts/GrandPiano.SF2')
    o.play()

