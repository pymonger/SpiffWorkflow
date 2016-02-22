# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division
import os
import sys
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from tests.SpiffWorkflow.util import run_workflow
from .TaskSpecTest import TaskSpecTest
from SpiffWorkflow import Task
from SpiffWorkflow.specs import Hysds


class HysdsTest(TaskSpecTest):
    CORRELATE = Hysds

    def create_instance(self):
        if 'testtask' in self.wf_spec.task_specs:
            del self.wf_spec.task_specs['testtask']
        return Hysds(self.wf_spec,
                       'testtask',
                       description='foo',
                       args=self.cmd_args)

    def setUp(self):
        payload = {
            "job_type": "job:aria-extract_features",
            "payload": {
                "rule": {
                    "rule_name": "test_from_spiffworkflow",
                    "username": "gmanipon",
                },
                "rule_hit": {
                     "_source": {
                         "urls": ["http://test.com/test.hdf"],
                     }
                }
            }
        }
        self.cmd_args = [payload]
        TaskSpecTest.setUp(self)

    def testConstructor(self):
        TaskSpecTest.testConstructor(self)
        self.assertEqual(self.spec.args, self.cmd_args)

    def testPattern(self):
        """
        Tests that we can create a task that executes an shell command
        and that the workflow can be called to complete such tasks.
        """
        self.wf_spec.start.connect(self.spec)
        expected = 'Start\n  testtask\n'
        workflow = run_workflow(self, self.wf_spec, expected, '')
        task = workflow.get_tasks_from_spec_name('testtask')[0]
        self.assertEqual(task.state_history, [Task.FUTURE,
                                              Task.WAITING,
                                              Task.READY,
                                              Task.COMPLETED])
        self.assert_(b'127.0.0.1' in task.results[0])


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(HysdsTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
