from moviepy.editor import *
#from moviepy.video.io.VideoFileClip import VideoFileClip
#from moviepy.video.fx.resize import resize

def videoDisplay(path):
    
    clip = VideoFileClip(path).resize(0.75)
    #clip.resize(0.8)
    clip.preview()

#videoDisplay("D:/Vision/Face/FACE_LATEST/videos/How to Shave - Shaving Tips for Men _ Gillette.mp4")
#videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
