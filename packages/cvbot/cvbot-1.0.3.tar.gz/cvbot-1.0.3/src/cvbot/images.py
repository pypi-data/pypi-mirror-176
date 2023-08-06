import cv2 as cv
from cvbot.sift import find, show_features


class Image:
    def __init__(self, img, name="snapshot"):
        self.img  = img
        self.name = name
        self.type = "grey" if len(img.shape) < 3 else "colored"

    def grey(self):
        """
        self -> npimage
        Convert current image to gray and return it as a numpy image/matrix
        """
        return cv.cvtColor(self.img, cv.COLOR_BGR2GRAY) if self.type != "grey" else self.img

    def show(self, pos=None):
        """
        self, [Optional] tuple(x, y) -> None
        Display image in a window on screen
        """
        cv.namedWindow(self.name)
        if not (pos is None):
            x, y = pos
            cv.moveWindow(self.name, x, y)
        cv.imshow(self.name, self.img)
        cv.waitKey(0)

    def sift_find(self, scene, quality):
        """
        self, Image, int -> box
        Find using sift features the current image in 'scene' image and return the location as a rectangle/box
                quality : minimum features to find
        """
        return find(self.grey(),
                    scene.grey(), quality)

    def sift_feats(self):
        """
        self -> None
        Show detected sift feature in the current image in a window on screen
        """
        show_features(self.grey())
