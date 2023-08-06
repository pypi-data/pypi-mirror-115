from src.utils import CV
from src.source import Video


def test_video_capture():
    webcam = Video()
    cv = CV()

    for image in webcam.stream():
        cv.show('easypipe', image)
