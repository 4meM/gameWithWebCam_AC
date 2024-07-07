import threading
import cv2
from webCam import ColorDetector
from game import SimpleGame

def run_game():
    game = SimpleGame()
    game.run()

def run_color_detector():
    color_detector = ColorDetector()

    while True:
        img = color_detector.process_frame()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    color_detector.stop()

if __name__ == "__main__":
    game_thread = threading.Thread(target=run_game)
    detector_thread = threading.Thread(target=run_color_detector)

    game_thread.start()
    detector_thread.start()

    game_thread.join()
    detector_thread.join()


