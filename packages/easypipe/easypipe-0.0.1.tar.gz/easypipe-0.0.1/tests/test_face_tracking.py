from src.source import Video
from src.face import TrackFace


def test_hand_tracking():
    webcam = Video()
    face = TrackFace()

    for data, image in face.process(webcam.stream):
        print(data, image)
