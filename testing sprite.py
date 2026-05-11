from PIL import Image
import glob
import os
import moviepy.editor as mpy



def create_animation_frames():
    img_seq = glob.glob(os.path.join('Funtimefoxy_idle', '*.png'))
    img_seq.sort()
    clip = mpy.ImageSequenceClip(img_seq, fps=30)
    clip.write_videofile('animation.mp4')
    clip.close()


def main():
    create_animation_frames()

#def load_animation_frame(path):

if __name__ == "__main__":
    main()