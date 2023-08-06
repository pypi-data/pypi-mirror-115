import concurrent.futures
import os
import json
import queue
import urllib.request
from .LAUNCHER import Launcher
import logging.handlers
import logging
import multiprocessing

ALL = [
    "JsonHandler",
    "Launcher",
    "LogHandler",
    "format_root",
    "DownloadFromJson",
    "ALL",
]

__all__ = ALL


class JsonHandler:
    def __init__(self, file=None):
        self.file = file

    def load(self):
        with open(self.file, 'r') as loaded:
            return json.load(loaded)

    def dump(self, store):
        with open(self.file, 'w') as loaded:
            return json.dump(store, loaded, indent=4)

    def __call__(self, raw: str):
        return json.loads(raw)

    def __str__(self):
        return self.file

    def parse_url(self, raw_link):
        with urllib.request.urlopen(raw_link) as raw:
            return self(raw.read())

    def close(self):
        os.remove(self.file)


class LogHandler(logging.Handler):
    def __init__(self, callable_=None):
        super().__init__(logging.DEBUG)
        self.callback = callable_

        self.setFormatter(logging.Formatter(
            "%(asctime)s:[%(levelname)s]:%(threadName)s :: %(message)s", datefmt="%d-%m-%Y %I:%M:%S"
        ))

    def register_callback(self, callback_):
        self.callback = callback_

    def emit(self, record):
        recorded = self.format(record)

        self.callback(recorded, record)

        return record


def format_root():
    root = logging.getLogger("")
    root.setLevel(logging.DEBUG)

    root.addHandler(logging.StreamHandler(None)) if len(root.handlers) == 0 else None

    handler = root.handlers[0]
    handler.setLevel(logging.DEBUG)

    handler.setFormatter(
        logging.Formatter("%(asctime)s:[%(levelname)s]:%(threadName)s :: %(message)s", datefmt="%d-%m-%Y %I:%M:%S"
                          )
    )

    return root


class DownloadFromJson:
    def __init__(self, json_path, manager=None):
        self.p_callback, self.f_callback = None, None
        self.tree = JsonHandler(json_path)

        self.linear = []

        self.executor = manager if manager else concurrent.futures.ThreadPoolExecutor(
            thread_name_prefix="Downloader"
        )
        self.maintain = set()

    def register_progress_callback(self, callback):
        self.p_callback = callback

    def register_finished_callback(self, callback):
        self.f_callback = callback

    def initiate(self, pointer):
        stack = [
            iter(
                self.tree.load().pop("downloads", {}).items()
            )
        ]

        total_length = 0

        while stack:
            try:
                key, value = next(stack[-1])
                path = pointer / key

                if type(value) == str:
                    None if path.exists() else self.maintain.add(
                        (value, path)
                    )
                else:
                    value = value.items()
                    total_length += len(value)

                    None if path.exists() else os.mkdir(path)

                    stack.append(iter(value))

                    pointer = path

            except StopIteration:
                stack.pop()
                pointer = pointer.parent

        if not self.maintain:
            return self.f_callback()

        self.p_callback(total_length)

        del stack

        for _ in tuple(self.maintain):
            future = self.executor.submit(self.download, *_)
            future.add_done_callback(self.update)

    def download(self, url, path):
        try:
            urllib.request.urlretrieve(url, path)
            return True, ""

        except Exception as _:
            return False, _

        finally:
            self.maintain.remove((url, path))

    def update(self, future: concurrent.futures.Future):
        status, exe = future.result()
        return self.f_callback(status, exe) if len(self.maintain) == 0 else self.p_callback(status, exe)
