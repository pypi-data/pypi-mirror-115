from easypipe.utils import CV


class Video(CV):
    def __init__(self, video_source: int = 0) -> None:
        super().__init__()
        self.keys = [27, 113]
        self.video_source = self.source(video_source)

    def stream(self, flip=True):
        while self.video_source.isOpened():
            success, image = self.video_source.read()
            if not success:
                print("Ignoring empty frame.")
                continue

            image.flags.writeable = False
            yield self.flip(image) if flip else image

            if self.wait(1) & 0xFF in self.keys:
                break

        self.video_source.release()


class Image:
    def __init__(self) -> None:
        pass
