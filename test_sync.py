import librosa
import sounddevice as sd

def beat_tracker(y):
    # Calculate beat tracking features
    onset_env = librosa.onset.onset_strength(y, sr=sr, hop_length=hop_length)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, hop_length=hop_length)
    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)
    # Print the beat times
    print(beat_times)

def audio_callback(indata, frames, time, status):
    global t, frame_count
    if status:
        print(status)
    # Convert audio data to mono
    indata = np.mean(indata, axis=1)
    # Track beats in real time
    beat_tracker(indata)

y, sr = librosa.load("../sample2.mp3")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)
clicks = librosa.clicks(frames=beats, sr=sr, length=len(y))


sd.play(y + clicks, sr)
sd.wait()
