import time

class PerformanceMonitor:
    def __init__(self):
        self.Frames = 0
        self.LastUpdateTime = time.time()
        self.LastFrameTime = time.time()
        self.LongestFrame = 0

    def Update(self):
        self.LongestFrame = max(self.LongestFrame, time.time() - self.LastFrameTime)
        self.LastFrameTime = time.time()
        self.Frames += 1
        dt = time.time() - self.LastUpdateTime
        if dt > 1:
            print int(self.Frames / dt), "FPS, Average =", dt * 1000.0 / self.Frames, "ms, Longest =", self.LongestFrame * 1000, "ms"
            self.Frames = 0
            self.LongestFrame = 0
            self.LastUpdateTime = time.time()
