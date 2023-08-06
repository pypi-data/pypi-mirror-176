# modulepy

easily build modular applications

## installation

```shell
pip3 install modulepy
# or
pip3 install git+https://github.com/nbdy/modulepy
```

## features

- [X] process based module baseline
- [X] module loader
  - [X] one-line module loading
  - [X] one-line directory loading
- [X] module manager
  - [X] add module
  - [X] remove module
  - [X] reload module directory
  - [X] module dependency resolution
  - [X] ipc
  - [X] module fault detection 

## example

### main.py
```python
from time import sleep

from modulepy.Manager import Manager
from pathlib import Path


if __name__ == '__main__':
    manager = Manager(Path.cwd() / "modules")
    try:
        manager.start()
        while manager.data.get("do_run"):
            sleep(0.1)
    except KeyboardInterrupt:
        manager.stop()
        manager.join()

```

### modules/GPS.py

```python
from typing import Optional

from gps import gps, WATCH_ENABLE

from modulepy import log
from modulepy.Base import Base, Information, Version


class GPS(Base):
    information = Information("GPS", Version(1, 0, 0))
    client: Optional[gps] = None

    def on_start(self):
        log.debug("Creating GPS client")
        try:
            self.client = gps(mode=WATCH_ENABLE)
            log.debug("Created client")
            self.data.set("error", None)
        except ConnectionRefusedError:
            self.data.set("error", "ConnectionRefusedError")
            log.error("Could not create client")
            pass

    def on_stop(self):
        log.debug("Closing GPS client")
        if self.client:
            self.client.close()

    def work(self):
        if self.client:
            self.client.next()
            self.data.set("latitude", self.client.fix.latitude)
            self.data.set("longitude", self.client.fix.longitude)
            self.data.set("altitude", self.client.fix.altitude)
            self.data.set("speed", self.client.fix.speed)
            self.data.set("track", self.client.fix.track)
            self.data.set("satellites", self.client.satellites)
            self.data.set("timestamp", self.client.utc)

```

### modules/UI.py

```python
from modulepy.Base import Base, Information, Version
from modulepy import log

from pyray import *


class UI(Base):
    information = Information("TestUI", Version(1, 0, 0))
    dependencies = [Information("Manager", Version(1, 0, 0)), Information("GPS", Version(1, 0, 0))]

    def on_start(self):
        log.debug("Initializing window")
        init_window(800, 600, "TestUI")
        set_target_fps(30)
        self.data.text = "init text"

    def on_stop(self):
        log.debug("Closing window")
        close_window()

    def work(self):
        error = self.clients["GPS"].get("error")

        if error is None:
            error = "None"

        begin_drawing()
        clear_background(BLACK)

        draw_text(error, 100, 100, 24, GREEN)
        if not error:
            draw_text("Client is not connected", 100, 120, 18, RED)
        else:
            draw_text("Connected client", 100, 120, 18, GREEN)

        end_drawing()

        tmp = window_should_close()
        self.data.set("do_run", not tmp)
        if tmp:
            print("Setting manager do_run to false")
            self.clients["Manager"].set("do_run", False)

```