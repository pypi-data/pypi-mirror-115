import numpy as np
import imageio
import io
import cv2
from IPython.display import Video, clear_output

class VidPlot(object):

    def __init__(self, filename="output", fps=30):
        if filename[-4:] == ".mp4":
            filename = filename[:-4]
        filename += ".mp4"
        self.__filename = filename
        if fps <= 0 or fps > 120:
            raise ValueError("FPS must be in the range from 1 to 120")
        if type(fps) is not int:
            raise TypeError("FPS must be an integer")
        self.__fps = fps
        self.writer = imageio.get_writer(self.__filename, fps=self.__fps)
        self.__done = False

    def get_img_from_fig(fig, dpi=160):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        buf.close()
        img = cv2.imdecode(img_arr, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

    def add(self, fig, dpi=160):
        self.writer.append_data(MatplotlibVideo.get_img_from_fig(fig, dpi))

    def addP(self, fig, progress, dpi=160):
        self.writer.append_data(MatplotlibVideo.get_img_from_fig(fig, dpi))
        print("Progress : {:.3f}%".format(progress * 100))
        clear_output(wait=True)

    def finnish(self, width=600):
        self.writer.close()
        self.__done = True
        return self.show(width)

    def showVideo(name, width=600):
        return Video(name, width=width, embed=True)

    def show(self, width=600):
        if self.__done:
            return Video(self.filename, width=width, embed=True)
        else:
            raise Exception("You first have to finnish the Video (x.finnish())")

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def path(self, value):
        raise Exception("You need to create a new Video in order to change the Name")

    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, value):
        raise Exception("You need to create a new Video in order to change the FPS")
