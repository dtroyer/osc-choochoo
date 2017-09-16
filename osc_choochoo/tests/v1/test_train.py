#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import mock
import os

from osc_choochoo.tests import base
from osc_choochoo.tests import fakes
from osc_choochoo.v1 import train

# Load the plugin init module for the plugin list and show commands
plugin_name = 'osc_choochoo'
plugin_client = 'osc_choochoo.plugin'


class FakeTrainV1Client(object):
    def __init__(self, **kwargs):
        self.auth_token = kwargs['token']
        self.management_url = kwargs['endpoint']


class TestTrainV1(base.TestCommand):
    def setUp(self):
        super(TestTrainV1, self).setUp()

        self.app.client_manager.osc_choochoo = FakeTrainV1Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )


class TestTrainList(TestTrainV1):

    def setUp(self):
        super(TestTrainList, self).setUp()

        # Get the command object to test
        self.cmd = train.TrainList(self.app, None)

    def test_plugin_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        collist = ('Name', )
        datalist = ['1.txt', '2.txt']

        with mock.patch('os.listdir') as mock_list:
            mock_list.return_value = datalist

            # DisplayCommandBase.take_action() returns two tuples
            columns, data = self.cmd.take_action(parsed_args)
            self.assertEqual(collist, columns)
            for d in data:
                self.assertTrue(d[0] + '.txt' in datalist)


class TestPluginShow(TestTrainV1):

    def setUp(self):
        super(TestPluginShow, self).setUp()

        # Get the command object to test
        self.cmd = train.TrainShow(self.app, None)

    def test_plugin_show(self):
        arglist = [
            plugin_name,
        ]
        verifylist = [
            ('name', plugin_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        collist = ['name', 'data']
        datalist = [
            plugin_name,
            'dummy',
        ]

        with mock.patch('io.open') as mock_open:
            mock_open.return_value = mock.MagicMock()
            m_file = mock_open.return_value.__enter__.return_value
            m_file.read.return_value = 'dummy'

            columns, data = self.cmd.take_action(parsed_args)

            mock_open.assert_called_once_with(
                os.path.join(
                    train.DATA_PATH,
                    plugin_name + '.txt',
                )
            )
            self.assertEqual(collist, columns)
            self.assertEqual(datalist, data)
