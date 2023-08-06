import cv2


class CV:
    def __init__(self) -> None:
        self.flip = lambda image: cv2.flip(image, 1)
        self.precolor = lambda image: cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.aftcolor = lambda image: cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.show = lambda title, image: cv2.imshow(title, image)
        self.wait = lambda wait: cv2.waitKey(wait)
        self.source = lambda video_source: cv2.VideoCapture(video_source)
