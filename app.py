# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import signal
import sys
from types import FrameType

from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image

import imageget

import requests

from utils.logging import logger

app = Flask(__name__)
app.secret_key = "YC_seckey-4086567967" #秘密鍵

CLOUD_RUN_URL = "https://asia-northeast1-metal-bonus-446214-g5.cloudfunctions.net/search-chat"

# リクエストデータ
request_data = {
    "query": "きた"  # 検索文字列をここで指定
}

@app.route("/")
def htmlView():
    html = render_template("index.html")
    return html

def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")

    from utils.logging import flush

    flush()

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)

#参考URL：https://note.com/luuluu3311/n/n25b642838786
