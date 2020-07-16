from imutils.video import FPS

class Count_FPS(FPS):
    fps = FPS().start()

    def Update(self):
        self.fps.update()

    def Stop(self):
        self.fps.stop()

    def Resume(self):
        return ( self.fps.elapsed(), self.fps.fps() )
