import time

VIDEO_FORMAT = (".mp4", ".mov")

class FPS(object):
    def __init__(self):
        self.frame = 0
        
    def start(self):
        self.start_time = time.time()
        
    def stop(self):
        self.elapsed_time = time.time() - self.start_time
    
    def update(self):
        self.frame += 1
        
    def fps(self):
        self.fps_value = self.frame / self.elapsed_time
        return self.fps_value