from src.source import Video
from src.hands import TrackHands


def test_hand_tracking():
    webcam = Video()
    hands = TrackHands()

    for data, hand_landmarks, image in hands.process(webcam.stream):
        print(data, hand_landmarks, image)
