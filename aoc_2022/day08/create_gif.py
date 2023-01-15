from moviepy.editor import VideoFileClip
videoClip = VideoFileClip("output.mp4")
videoClip.write_gif("output.gif",opt='we')