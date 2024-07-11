class DownloadProgressInfo:
    __slots__ = (
        "fileName",
        "speed",
        "percent",
        "done",
        "all_done"
    )

    def __init__(self, fileName, speed, percent, done):
        self.fileName = fileName
        self.speed = speed
        self.percent = percent
        self.done = done
        self.all_done = False


class ActionCanceledException(Exception):
    def __init__(self):
        super().__init__()
