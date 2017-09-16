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

import logging

from cliff import lister
from cliff import show


class TrainList(lister.Lister):
    """List trains"""

    auth_required = False
    log = logging.getLogger(__name__ + ".TrainList")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        data = []
        columns = ("Name", )
        return (columns, data)


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

        data = r"""
                                                        \  /
                  __                                     \/
     _   ---===##===---_________________________--------------  _
    [ ~~~=================###=###=###=###=###=================~~ ]
    /  ||  | |~\  ;;;;     DEN    ;;;  SEP-2017  ;;;;  /~| |  ||  \
   /___||__| |  \ ;;;;            [_]            ;;;; /  | |__||___\
   [\        |__| ;;;;  ;;;; ;;;; ;;; ;;;; ;;;;  ;;;; |__|        /]
  (=|    ____[-]_______________________________________[-]____    |=)
  /  /___/|#(__)=o########o=(__)#||___|#(__)=o#########o=(__)#|\___\
 _________-=\__/=--=\__/=--=\__/=-_____-=\__/=--=\__/=--=\__/=-______
"""

        return (["1"], [data])
