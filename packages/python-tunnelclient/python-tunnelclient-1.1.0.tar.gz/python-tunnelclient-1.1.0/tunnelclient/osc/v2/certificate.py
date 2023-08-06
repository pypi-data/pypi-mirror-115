#   Copyright 2017 GoDaddy
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

"""Certificate action implementation"""


from cliff import lister
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from oslo_utils import uuidutils

from tunnelclient.osc.v2 import constants as const
from tunnelclient.osc.v2 import utils as v2_utils
from tunnelclient.osc.v2 import validate


class CreateCertificate(command.ShowOne):
    """Create a certificate"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'vpnserver',
            metavar='<vpnserver>',
            help="Vpn server for the certificate (name or ID)."
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help="Set the certificate name."
        )
        parser.add_argument(
            '--client_req',
            metavar='<client_req>',
            required=True,
            help="client_req of the certificate."
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help="Set the description of this certificate."
        )
        return parser

    def take_action(self, parsed_args):
        rows = const.CERTIFICATE_ROWS
        attrs = v2_utils.get_certificate_attrs(self.app.client_manager,
                                            parsed_args)

        body = {"certificate": attrs}
        data = self.app.client_manager.vpn_server.certificate_create(
            json=body)

        formatters = {'vpnservers': v2_utils.format_list}

        return (rows,
                (utils.get_dict_properties(data['certificate'],
                                           rows,
                                           formatters=formatters)))


class DeleteCertificate(command.Command):
    """Delete a certificate"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'certificate',
            metavar="<certificate>",
            help="Certificate to delete (name or ID)"
        )
        return parser

    def take_action(self, parsed_args):
        attrs = v2_utils.get_certificate_attrs(self.app.client_manager,
                                            parsed_args)

        certificate_id = attrs.pop('certificate_id')

        self.app.client_manager.vpn_server.certificate_delete(
            certificate_id=certificate_id)


class ListCertificate(lister.Lister):
    """List certificates"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            '--name',
            metavar='<name>',
            help="List certificates by certificate name."
        )
        parser.add_argument(
            '--vpnserver',
            metavar='<vpnserver>',
            help="Filter by vpn server (name or ID).",
        )

        parser.add_argument(
            '--project',
            metavar='<project>',
            help="List certificates by project ID."
        )
        return parser

    def take_action(self, parsed_args):
        columns = const.CERTIFICATE_COLUMNS
        attrs = v2_utils.get_certificate_attrs(self.app.client_manager,
                                            parsed_args)
        data = self.app.client_manager.vpn_server.certificate_list(**attrs)
        formatters = {'vpnservers': v2_utils.format_list}
        return (columns,
                (utils.get_dict_properties(s, columns, formatters=formatters)
                 for s in data['certificates']))


class ShowCertificate(command.ShowOne):
    """Show the details of a single certificate"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument(
            'certificate',
            metavar='<certificate>',
            help='Name or UUID of the certificate'
        )

        return parser

    def take_action(self, parsed_args):
        rows = const.CERTIFICATE_ROWS
        data = None
        if uuidutils.is_uuid_like(parsed_args.certificate):
            try:
                data = self.app.client_manager.vpn_server.certificate_show(
                    certificate_id=parsed_args.certificate)
            except exceptions.NotFound:
                pass
        if data is None:
            attrs = v2_utils.get_certificate_attrs(self.app.client_manager,
                                                parsed_args)

            certificate_id = attrs.pop('certificate_id')

            data = self.app.client_manager.vpn_server.certificate_show(
                certificate_id=certificate_id,
            )
        formatters = {'vpnservers': v2_utils.format_list}

        return rows, utils.get_dict_properties(data, rows,
                                               formatters=formatters)


