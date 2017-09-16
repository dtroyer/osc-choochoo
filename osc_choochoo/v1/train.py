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

"""Plugin action implementation"""

import io
import logging
import os
from pkg_resources import resource_filename

from cliff import command
from cliff import lister
from cliff import show
from osc_lib import exceptions
from openstackclient.i18n import _


DATA_PATH = resource_filename('osc_choochoo.v1.train', 'data/')


class TrainList(lister.Lister):
    """List trains"""

    auth_required = False
    log = logging.getLogger(__name__ + ".TrainList")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        data = []
        # get list of files in DATA_PATH
        for f in os.listdir(DATA_PATH):
            if f.endswith(".txt"):
                data.append([f.replace('.txt', ''), True])

        columns = ("Name", "Whistle")
        return (columns, data)


class TrainSet(command.Command):
    _description = _("Modify train properties")

    auth_required = False
    log = logging.getLogger(__name__ + '.TrainSet')

    def get_parser(self, prog_name):
        parser = super(TrainSet, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<train-name>',
            help='Train to modify',
        )
        whistle_group = parser.add_mutually_exclusive_group()
        whistle_group.add_argument(
            "--disable-whistle",
            action="store_true",
            help=_("Disable the train whistle"),
        )
        whistle_group.add_argument(
            "--enable-whistle",
            action="store_true",
            help=_("Enable the train whistle"),
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        filename = os.path.join(DATA_PATH, parsed_args.name + '.txt')
        try:
            with io.open(filename) as f:
                # Ha!  Nothing to do here, the whistle is always enabled!
                pass
        except IOError as e:
            msg = "Train %(train)s not found: %(exception)s"
            raise exceptions.CommandError(
                msg % {
                    "train": parsed_args.name,
                    "exception": e,
                }
            )
        return


class TrainShow(show.ShowOne):
    """Show train information"""

    auth_required = False
    log = logging.getLogger(__name__ + '.TrainShow')

    def get_parser(self, prog_name):
        parser = super(TrainShow, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<train-name>',
            help='Train to show',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        filename = os.path.join(DATA_PATH, parsed_args.name + '.txt')
        try:
            with io.open(filename) as f:
                ascii_art = f.read()
        except IOError as e:
            msg = "Train %(train)s not found: %(exception)s"
            raise exceptions.CommandError(
                msg % {
                    "train": parsed_args.name,
                    "exception": e,
                }
            )
        return (
            ["name", "whistle", "data"],
            [parsed_args.name, True, ascii_art],
        )
