import librosa
import threading
import numpy as np

import sounddevice as sd
import soundfile as sf

y, sr = librosa.load("../sample2.mp3", duration=20)
# y, sr = librosa.load(librosa.example('brahms'))
# y, sr = librosa.load(librosa.example('choice'))
# y, sr = librosa.load(librosa.example('fishin'))
# y, sr = librosa.load(librosa.example('nutcracker'))
# y, sr = librosa.load(librosa.example('trumpet'))
# y, sr = librosa.load(librosa.example('vibeace', hq=True))

tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)
clicks = librosa.clicks(frames=beats, sr=sr, length=len(y))


event = threading.Event()


# Reshape arrays to have two channels  (2 columns)
y = np.reshape(y, (-1, 1))
y = np.column_stack((y, y))

# Reshape arrays to have two channels (2 columns)
clicks = np.reshape(clicks, (-1, 1))
clicks = np.column_stack((clicks, clicks))

# Add in clicks
y = y + clicks 

# def print_beats(current_frame)

current_frame = 0
start_time = 0
beat_index = 0
activity_counter = 0

def callback(outdata, frames, time, status):
	global current_frame
	global beat_index
	global start_time
	global activity_counter

	if status:
		print(status)
	if start_time == 0:
		start_time = time.outputBufferDacTime
		print("start: {}".format(start_time))

	if beat_index < len(beat_times) - 1:
		current_time = time.outputBufferDacTime
		# print(current_time)
		next_beat_time = start_time + beat_times[beat_index]
		if current_time >= next_beat_time:
			if beat_index % 8 == 0:
				print("Movement {}".format(activity_counter))
				activity_counter += 1
			else:
				print("\tBEAT {}".format(beat_index))
			beat_index += 1

	chunksize = min(len(y) - current_frame, frames)
	# print(current_frame)
	# outdata[:chunksize] = y[current_frame:current_frame + chunksize]
	# print(time.outputBufferDacTime)
	outdata[:chunksize] = y[current_frame:current_frame + chunksize]
	# outdata[:] = y.reshape(-1, 1)
	if chunksize < frames:
		outdata[chunksize:] = 0
		raise sd.CallbackStop()
	current_frame += chunksize

stream = sd.OutputStream(samplerate=sr, callback=callback, finished_callback=event.set)
with stream:
	event.wait()  # Wait until playback is finished


