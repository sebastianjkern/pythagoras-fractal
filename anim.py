# %%
import skia
import numpy as np
import inspect
import matplotlib.pyplot as plt
import cv2
import os

class Anim:
    def __init__(self, iterations, skip=1, shape=(1080, 1920, 4)):
        self._array = np.zeros(shape, dtype=np.uint8)
        self._surface = skia.Surface(self._array)
        self._canvas = self._surface.getCanvas()
        self._iterations = iterations

        self.width = shape[1]
        self.height = shape[0]

        self.background_color = skia.ColorBLACK
        self._canvas.clear(self.background_color)

        self.func = None
        self.vars = lambda: None

        self.vars.iteration = 0
        self.vars.skip = skip
        self.name = "out"

        try:
            os.mkdir("out", mode=0o666)
        except OSError as error:
            print(error)

        self._images = []

    def __enter__(self):
        return self
      
    def __exit__(self, *_):
        self._execute()
        frame = cv2.imread(os.path.join('out', self._images[0]))
        height, width, _ = frame.shape

        video = cv2.VideoWriter(self.name + ".mp4", 0, 60, (width, height))

        for image in self._images:
            video.write(cv2.imread(os.path.join('out', image)))

        cv2.destroyAllWindows()
        video.release()
        print("Finished writing video")

    def _execute(self):
        if len(inspect.signature(self.func).parameters) != 3:
            raise TypeError()

        rate = int(self._iterations / 100)

        if rate == 0:
            rate = 1

        for _iteration in range(self._iterations):
            self._canvas.clear(self.background_color)

            self._paint = skia.Paint()
            self._paint.setAntiAlias(True)

            if _iteration % rate == 0:
                print(str(_iteration) + "/" + str(self._iterations))

            self.vars.iteration = _iteration

            self.func(self._canvas, self._paint, self.vars)

            if _iteration % self.vars.skip == 0:
                im = self._surface.makeImageSnapshot()
                filename = self.name + '_{}.png'.format(_iteration)
                self._images.append(filename)
                im.save('out/' + filename, skia.kPNG)

if __name__ == '__main__':
    def func(canvas, paint, vars):
        paint.setStyle(skia.Paint.kStroke_Style)
        paint.setStrokeWidth(4)
        paint.setColor(skia.ColorRED)

        rect = skia.Rect.MakeXYWH(vars.iteration, vars.iteration, 2 * vars.iteration, 3 * vars.iteration)
        canvas.drawRect(rect, paint)

    with Anim(iterations=120) as anim:
        anim.func = func

        anim.vars.c = 2
        anim.vars.x = 3
        
        anim._execute()
# %%
