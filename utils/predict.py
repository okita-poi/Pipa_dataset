import librosa
import numpy as np
import pretty_midi

audio_path = 'mp3/3476.mp3'
y, sr = librosa.load(audio_path)

# 使用 pyin 进行音高跟踪
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7')
)

times = librosa.times_like(f0, sr=sr)
midi_notes = librosa.hz_to_midi(f0)
midi_data = pretty_midi.PrettyMIDI()
instrument = pretty_midi.Instrument(program=0)

prev_note_number = None
note_start_time = None

for idx, (t, note_number, voiced) in enumerate(zip(times, midi_notes, voiced_flag)):
    if voiced and not np.isnan(note_number):
        note_number = int(np.round(note_number))
        if note_number != prev_note_number:
            if prev_note_number is not None:
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=prev_note_number,
                    start=note_start_time,
                    end=t
                )
                instrument.notes.append(note)
            prev_note_number = note_number
            note_start_time = t
    else:
        if prev_note_number is not None:
            note = pretty_midi.Note(
                velocity=100,
                pitch=prev_note_number,
                start=note_start_time,
                end=t
            )
            instrument.notes.append(note)
            prev_note_number = None
            note_start_time = None

if prev_note_number is not None:
    note = pretty_midi.Note(
        velocity=100,
        pitch=prev_note_number,
        start=note_start_time,
        end=times[-1]
    )
    instrument.notes.append(note)

midi_data.instruments.append(instrument)
midi_data.write('output.mid')
