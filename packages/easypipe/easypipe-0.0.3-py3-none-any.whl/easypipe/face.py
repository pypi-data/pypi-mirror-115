import mediapipe
from easypipe.utils import CV


class TrackFace(CV):
    def __init__(self) -> None:
        super().__init__()
        self.face = mediapipe.solutions.face_detection
        self.drawing = mediapipe.solutions.drawing_utils

    def process(self, video, title='easypipe'):
        with self.face.FaceDetection(model_selection=0,
                                     min_detection_confidence=0.5) as face_detection:
            for image in video():
                image = self.precolor(image)
                results = face_detection.process(image)

                image.flags.writeable = False
                image = self.aftcolor(image)

                #image.flags.writeable = True

                if results.detections:
                    for detection in results.detections:
                        yield detection, image
                        self.drawing.draw_detection(image, detection)

                self.show(title, image)
