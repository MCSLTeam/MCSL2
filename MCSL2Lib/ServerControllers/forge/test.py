import asyncio
import threading
from pathlib import Path
from queue import Queue
from threading import Timer

from installer.actions.progress_callback import TO_STD_OUT
from installer.simple_installer import SimpleInstaller


# def test():
#     from installer.json.util import Util
#     with open("./install_profile.json", "r", encoding="utf-8") as f:
#         text = f.read()
#     profile = Util.loadInstallProfile(text)
#     print(profile)


class InfoConsumer(threading.Thread):
    def __init__(self, infoQueue: Queue):
        super().__init__()
        self.infoQueue = infoQueue

    def run(self):
        while True:
            get = self.infoQueue.get(block=True, timeout=5)
            if get is None:
                print("InfoConsumer: CANCEL detected")
                return
            filename, speed, progress, done, allDone = get
            print(f" - {filename} - {speed}KB/s - {progress}% - {done=} - {allDone=}")
            if allDone:
                return


if __name__ == "__main__":
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #
    # print(os.getcwd())
    # test()
    # art = Artifact.from_("net.minecraftforge:forge:1.20.4-49.0.26:shim")
    # print(art)
    # version = Version.of(json.loads(Path("version.json").read_text()))
    # print(version)

    infoQueue = Queue()

    installer = SimpleInstaller(True, infoQueue)
    watcher = InfoConsumer(infoQueue)
    watcher.start()

    monitor = TO_STD_OUT

    timer = Timer(3, lambda: [print("CANCEL!!!"), monitor.setCancelled(True)])
    timer.start()
    # Forge-1.20.1-47.2.19.jar Forge-1.21-51.0.18.jar
    asyncio.run(
        installer.installServer(
            Path("./Server/Forge-1.20.1-47.2.19.jar"), Path("./Server/"), TO_STD_OUT
        )
    )

    infoQueue.put(None)
    watcher.join()
