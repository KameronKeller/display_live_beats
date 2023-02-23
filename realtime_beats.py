import librosa
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf

# Global variables
current_frame = 0
start_time = 0
beat_index = 0
activity_counter = 0

y, sr = librosa.load("../sample2.mp3", duration=30)
# y, sr = librosa.load(librosa.example('brahms'))
# y, sr = librosa.load(librosa.example('choice'))
# y, sr = librosa.load(librosa.example('fishin'))
# y, sr = librosa.load(librosa.example('nutcracker'))
# y, sr = librosa.load(librosa.example('trumpet'))
# y, sr = librosa.load(librosa.example('vibeace', hq=True))

tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)
clicks = librosa.clicks(frames=beats, sr=sr, length=len(y))

# Reshape arrays to have two channels  (2 columns)
y = np.reshape(y, (-1, 1))
y = np.column_stack((y, y))

# Reshape arrays to have two channels (2 columns)
clicks = np.reshape(clicks, (-1, 1))
clicks = np.column_stack((clicks, clicks))

# Add in clicks
y = y + clicks 


event = threading.Event()

def print_realtime_beats(time, current_frame):
	global start_time
	global beat_index
	global activity_counter

	if start_time == 0:
		start_time = time.outputBufferDacTime

	if beat_index < len(beat_times) - 1:
		current_time = time.outputBufferDacTime

		next_beat_time = start_time + beat_times[beat_index]
		
		if current_time >= next_beat_time:
			if beat_index % 8 == 0:
				print("Movement {}".format(activity_counter))
				activity_counter += 1
			else:
				print("\tBEAT {}".format(beat_index))
			beat_index += 1


def callback(outdata, frames, time, status):
	global current_frame

	# Print any status messages
	if status:
		print(status)

	# Print beats in real time
	print_realtime_beats(time, current_frame)

	# Calculate the chunksize, accounting for the length of the data
	chunksize = min(len(y) - current_frame, frames)

	# Add the next chunk to the output stream
	outdata[:chunksize] = y[current_frame:current_frame + chunksize]

	# If at the end of the song, stop the callback
	if chunksize < frames:
		outdata[chunksize:] = 0
		raise sd.CallbackStop()
	current_frame += chunksize

stream = sd.OutputStream(samplerate=sr, callback=callback, finished_callback=event.set)
with stream:
	event.wait()  # Wait until playback is finished


