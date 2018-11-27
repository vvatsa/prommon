__copyright__ = "(c) 2018 RenaissanceRe IP Holdings Ltd.  All rights reserved."

import logging
import json
import importlib
import time

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from tornado import gen

LOG = logging.getLogger(name=__name__)


class ProbeError(Exception):
    pass


class ProbeTool(object):

    def __init__(self, driver, guage=None, counter=None):
        """

        :param driver: file path to json driver
        """
        with open(driver) as fd:
            _data = json.load(fd)

        self.guage = guage
        self.counter = counter

        self.env = _data['env']
        self.name = _data['name']
        LOG.info("Setting up %s", self.name)
        self.probe_args = _data['args']

        self.probe_module = importlib.import_module(_data['module'])
        if not hasattr(self.probe_module, 'run'):
            err = "Module %s does not have fn run", self.probe_module
            LOG.error(err)
            raise ProbeError(err)

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.result = None

    @gen.coroutine
    def run(self):
        now = time.time()
        success = True
        try:
            future = self.executor.submit(self.probe_module.run, *self.probe_args)
            yield future.result()
            self.result = future.result()
            if future.exception():
                raise future.exception()
        except Exception as ex:
            print(ex)
            success = False
        finally:
            run_delta = time.time() - now

        if self.guage:
            self.guage.labels(self.name, self.env, success).set(run_delta)

        # return value




