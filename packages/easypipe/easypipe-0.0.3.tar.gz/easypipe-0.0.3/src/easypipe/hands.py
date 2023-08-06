import mediapipe
from easypipe.utils import CV


class TrackHands(CV):
    def __init__(self, detection_confidence=0.5, tracking_confidence=0.5) -> None:
        super().__init__()
        self.drawing = mediapipe.solutions.drawing_utils
        self.hands = mediapipe.solutions.hands
        self.detection = detection_confidence
        self.tracking = tracking_confidence

    def process(self, video, title='easypipe'):
        with self.hands.Hands(min_detection_confidence=self.detection,
                              min_tracking_confidence=self.tracking) as hands:
            for image in video():
                image = self.precolor(image)
                results = hands.process(image)

                image.flags.writeable = False
                image = self.aftcolor(image)

                if results.multi_handedness:
                    for handedness in results.multi_handedness:
                        data = handedness.classification[0].label

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        yield data, hand_landmarks, image
                        self.drawing.draw_landmarks(
                            image, hand_landmarks, self.hands.HAND_CONNECTIONS)

                self.show(title, image)
