"""
Validate Phone Number API
"""

import os
import signal
import threading
import logging
import time
import re
from http import HTTPStatus
from typing import Tuple, Dict, Any

from flask import Flask, request, jsonify

log = logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s %(levelname)s %(asctime)s    "
           "%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger()


class PhoneValidator:
    """Phone number validator"""
    CODES = [982, 986, 912, 934]
    REGEXES = [
        re.compile(r"^\+7 (?P<code>\d{3}) (\d{3}) (\d{4})"), # +7 code ### ####
        re.compile(r"^\+7 \((?P<code>\d{3})\) (\d{3}) (\d{4})"), # +7 (code) ### ####
        re.compile(r"^\+7(?P<code>\d{3})(\d{3})(\d{4})"), # +7code#######/code>
        re.compile(r"^8\((?P<code>\d{3})\)(\d{3})-(\d{4})"), # 8(code)###-####
        re.compile(r"^8(?P<code>\d{3})(\d{3})(\d{4})") # 8code#######
    ]


    def __init__(self, raw: str):
        self.raw = raw.strip()
        log.debug("Initialized PhoneValidator for: %s", self.raw)


    def match(self) -> re.Match | None:
        """Match phone with templates"""
        for regex in self.REGEXES:
            mo = regex.fullmatch(self.raw)
            if mo and int(mo.group("code")) in self.CODES:
                log.debug("Matched pattern: %s", regex.pattern)
                return mo

        log.warning("No patterns matched for phone: %s", self.raw)
        return None


    def validate(self) -> Dict[str, Any]:
        """
        Returns:
        Нормализованное значение вида +7-###-###-####, где # - цифра
        example: "+7-912-123-4567"
        """
        mo = self.match()
        if not mo:
            log.info("Validation failed for phone: %s", self.raw)
            return {"status": False}

        normalized = f"+7-{mo.group('code')}-{mo.group(2)}-{mo.group(3)}"
        log.debug("Successful validation for %s. Normalized: %s", mo.group(0), normalized)
        return {"status": True, "normalized": normalized}

# Flask App

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    """Healthcheck"""
    log.debug("Ping request received")
    return "pong", HTTPStatus.OK.value


@app.route("/shutdown", methods=["GET"])
def shutdown():
    """Shutdown"""
    def kill_with_delay():
        time.sleep(1) # time to return response
        # getpid() get parent process (bash) pid
        os.kill(os.getpid(), signal.SIGTERM) # SIGTERM to parent process (bash)

    log.info("Shutdown request received. Shutting down...")
    # daemon=true thread run as a daemon, stop when the main thread stops
    threading.Thread(target=kill_with_delay, daemon=True).start()

    return "Shutting down...", HTTPStatus.OK.value


@app.route("/validatePhoneNumber", methods=["POST"])
def validate_phone_number() -> Tuple[Dict[str, Any], int]:
    """API для валидации телефонных номеров"""
    phone_number = request.get_json().get("phone_number")
    if not phone_number:
        return "", HTTPStatus.BAD_REQUEST.value

    log.debug("Validation request for phone: %s", phone_number)
    try:
        validator = PhoneValidator(phone_number)
        response = validator.validate()

        if response["status"]: # status: True
            log.info("Successful validation for phone: %s", phone_number)
            return jsonify(response), HTTPStatus.OK.value

        log.info("Failed validation for phone: %s", phone_number)
        return "", HTTPStatus.NOT_FOUND.value

    except Exception as e:
        log.error("Validation error for phone %s: %s", phone_number, e)
        return "", HTTPStatus.INTERNAL_SERVER_ERROR.value


if __name__ == "__main__":
    log.info("Starting phone validation API, on 0.0.0.0:7777")
    app.run(host="0.0.0.0", port=7777)
