#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading
import websocket


class WebSocket():

    message = []

    error = []

    def __init__(self, url, header=None):
        subThread = threading.Thread(
            target=self.connect, args=(url, header), name='websocket-thread')
        subThread.start()

    def connect(self, url, header):
        self.ws = websocket.WebSocketApp(
            url,
            header=header,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)

        self.ws.run_forever()

    def send(self, msg):
        self.message.clear()
        self.ws.send(msg)

    def close(self):
        self.ws.close()

    def on_close(self):
        self.close()

    def on_message(self, message):
        self.message.append(message)

    def on_error(self, error):
        self.error.append(error)

    def getMsg(self):
        return self.message


if __name__ == '__main__':
    header = {
        'Accept-Encoding':
        'gzip, deflate',
        'Connection':
        'Upgrade',
        'Origin':
        'http://testing-www.intranet.szjys.com',
        'Sec-WebSocket-Extensions':
        'permessage-deflate; client_max_window_bits',
        'Sec-WebSocket-Key':
        'pz9V4veoQXPf9PBbdnHzkQ==',
        'Sec-WebSocket-Version':
        13,
        'Upgrade':
        'websocket',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    websocket = WebSocket(
        'ws://testing-api.intranet.szjys.com/public', header=header)
