
import os
import signal
import threading
import logging
import time
import re
import json

from flask import Flask, request

log = logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(levelname)s %(asctime)s    "
           "%(message)s",
    datefmt="%I:%M:%S"
)
log = logging.getLogger()


class PhoneValidator:
    CODES = [982, 986, 912, 934]
    REGEXES = [
        re.compile(r"^\+7 (?P<code>\d{3}) (\d{3}) (\d{4})"), # +7 code ### ####
        re.compile(r"^\+7 \((?P<code>\d{3})\) (\d{3}) (\d{4})"), # +7 (code) ### ####
        re.compile(r"^\+7(?P<code>\d{3})(\d{3})(\d{4})\/(?P=code)"), # +7code#######/code>
        re.compile(r"^8\((?P<code>\d{3})\)(\d{3})-(\d{4})"), # 8(code)###-####
        re.compile(r"^8(?P<code>\d{3})(\d{3})(\d{4})") # 8code#######
    ]

    def __init__(self, raw):
        self.raw = raw

    def match(self):
        for regex in self.REGEXES:
            mo = regex.fullmatch(self.raw)
            if mo and int(mo.group("code")) in self.CODES:
                return mo
        return None

    def validate(self):
        """
        Returns:
        Нормализованное значение вида +7-###-###-####, где # - цифра
        example: "+7-912-123-4567"
        """
        mo = self.match()
        if not mo:
            response = {
                "status": False,
            }
            return json.dumps(response, indent=4)
        normalized = f"+7-{mo.group('code')}-{mo.group(2)}-{mo.group(3)}"
        response = {
            "status": True,
            "normalized": normalized
        }
        return json.dumps(response, indent=4), 200


app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/shutdown", methods=["GET"])
def shutdown():
    def kill_with_delay():
        time.sleep(1) # time to return response
        # getpid() get parent process (bash) pid
        os.kill(os.getpid(), signal.SIGTERM) # SIGTERM to parent process (bash)

    # daemon=true thread run as a daemon, stop when the main thread stops
    threading.Thread(target=kill_with_delay, daemon=True).start()

    return "Shutting down...", 200

@app.route("/validatePhoneNumber", methods=["POST"])
def validate_phone_number():
    request_body = request.get_data(as_text=True)

    validator = PhoneValidator(request_body)
    return validator.validate()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)
