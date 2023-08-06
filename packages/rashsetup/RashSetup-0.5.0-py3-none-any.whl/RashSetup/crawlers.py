import queue
from .RashScrappers.RashScrappers.spiders import *
from .shared import *
import multiprocessing
import logging
import logging.handlers
import scrapy.crawler

ALL.extend(
    [
        "Setup",
        "READMERawSetup",
        "SettingsRawSetup",
        "RepoRawSetup"
    ]
)

__all__ = ALL


class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self, queue_):
        super().__init__(queue_)

    def handle(self, record):
        # to make this pickle-able
        # avoiding all lambda functions from scrapy logs

        modified = logging.LogRecord(
            record.name,
            record.levelno,
            record.pathname,
            record.lineno,
            record.getMessage(),
            args=(),
            exc_info=record.exc_info,
            func=record.funcName,
            sinfo=record.stack_info
        )

        return super().handle(modified)


class RawSetup:
    def __init__(self, pipe, log_pipe: queue.Queue = None, *args):
        self.pipe = pipe
        self.pipe.saved = None

        self.cache = {
            "failed": True,
            "exception": "Failed before scrapping",
            "result": ""
        }

        self.logger = logging.getLogger("")

        self.logger.addHandler(
            QueueHandler(log_pipe)
        ) if log_pipe else None

        self.start(*args)

    def start(self, *args):
        process = scrapy.crawler.CrawlerProcess()
        process.crawl(*args)
        process.start(True)

        self.save()

    def save(self):
        handler = JsonHandler(
            TempHandler()(
                suffix=".json"
            )
        )

        handler.dump(self.cache)
        self.pipe.saved = handler

        self.logger.info("saved raw data into %s", handler.file)


class READMERawSetup(RawSetup):
    def start(self, url):
        super().start(READMESpider, self.cache, url)


class SettingsRawSetup(RawSetup):
    def start(self, url):
        super().start(Investigator, self.cache, url)


class RepoRawSetup(RawSetup):
    def start(self, url, path):
        super().start(RepoSpider, url, self.cache, path)


class Setup:
    def __init__(self, target, *args, create=True):
        self._manager = multiprocessing.Manager()
        self.saved = self._manager.Namespace()

        self.url = args[0]  # url

        self._ = multiprocessing.Process(
            target=target, args=(
                self.saved, None, *args
            )
        ) if create else None

    def join(self, timeout=None):
        self._.join(timeout)

    def results(self):
        """
        returns the result of a process that was saved inside "saved" attribute of multiprocessing.Manager().Namespace

        :return: passed[bool], result[typing.Any]
        """

        raw: JsonHandler = getattr(self.saved, "saved") if hasattr(self.saved, "saved") else None

        if not raw:
            return False, "Not a feasible result"

        loaded = raw.load()

        raw.close()
        self.close()

        if not all(("failed" in loaded, "result" in loaded, "exception" in loaded)):
            return False, "Missing Values"

        if loaded["failed"]:
            return False, loaded["exception"]

        return True, loaded["result"]

    def close(self):
        self._.close()

    def start(self):
        self._.start()
