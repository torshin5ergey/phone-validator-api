
import os
import signal
import threading
import logging
import time

from flask import Flask

log = logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(levelname)s %(asctime)s    "
           "%(message)s",
    datefmt="%I:%M:%S"
)
log = logging.getLogger()


app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/shutdown", methods=["POST"])
def shutdown():
    def kill_with_delay():
        time.sleep(1) # time to return respons
        # getpid() get parent process (bash) pid
        os.kill(os.getpid(), signal.SIGTERM) # SIGTERM to parent process (bash)

    # daemon=true thread run as a daemon, stop when the main thread stops
    threading.Thread(target=kill_with_delay, daemon=True).start()

    return "Shutting down...", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)
