# import ffmpeg

# # Define video parameters
# width = 640
# height = 480
# fps = 30
# duration = 10

# # Create blue background
# background = ffmpeg.input("color=c=black:s=640x480:r=30:d=30", t=duration)

# # # Create white text that fades in and out
# text = ffmpeg.drawtext(background, text='Hello World', fontcolor='white', fontsize=50, x='(w-text_w)/2', y='(h-text_h)/2', enable='between(t,1,9)')

# # Output the video file
# # output_path = 'output3.mp4'
# ffmpeg.output(text, 'output3.mp4').run()



import ffmpeg
import librosa

y, sr = librosa.load("../sample2.wav")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)

video = ffmpeg.input('output.mp4')
audio = video.audio


for time in beat_times:
  video = ffmpeg.drawtext(video, text='Beat', fontcolor='white', fontsize=50, x='(w-text_w)/2', y='(h-text_h)/2', enable='between(t,{},{})'.format(time, time+0.2))
  video = video.filter('fade', t='out', st=time, d=1.0)
# video = ffmpeg.drawtext(video, text='Blah', fontcolor='white', fontsize=50, x='(w-text_w)/3', y='(h-text_h)/3', enable='between(t,1,NAN)')



out = ffmpeg.output(audio, video, 'output6.mp4')

out.run()
