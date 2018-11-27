__copyright__ = "(c) 2018 RenaissanceRe IP Holdings Ltd.  All rights reserved."

import pytest
import mock
import json


from tornado import ioloop, web
from tornado.testing import AsyncTestCase

from prommon.probe_tool import ProbeTool
from prometheus_client import Gauge, generate_latest

def run(x, y):
    return x + y




class TestProbTool(AsyncTestCase):

    
    def test_probe_tool(self):
        driver_data = json.dumps({
            "name": "test",
            "module": "prommon.tests.test_probe_tool",
            "args": [1, 1],
            "env": "test"
        })
        guage = Gauge("TestGuage", "A Test Probe", ["probename", "probenv", "success"])
        with mock.patch('prommon.probe_tool.open', mock.mock_open(read_data=driver_data)):
            tool = ProbeTool('foo', guage=guage)
            tool.run()
            value = tool.result
            self.assertEqual(value, 2)
