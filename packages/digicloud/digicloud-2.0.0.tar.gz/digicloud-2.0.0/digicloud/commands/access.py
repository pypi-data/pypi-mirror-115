"""
    DigiCloud Access Service.
"""

from .base import Lister, ShowOne, Command
from .. import schemas


class ListFloatingIp(Lister):
    """List floating Ips."""
    schema = schemas.FloatingIPList(many=True)

    def get_data(self, parsed_args):
        uri = '/floating-ips'
        return self.app.session.get(uri)


class ShowFloatingIp(ShowOne):
    """Show floating Ip details."""
    schema = schemas.FloatingIPDetails()

    def get_parser(self, prog_name):
        parser = super(ShowFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip',
            metavar='<floating_ip>',
            help=('Floating IP ID'),
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/floating-ips/%s' % parsed_args.floating_ip
        return self.app.session.get(uri)


class CreateFloatingIp(ShowOne):
    """Create Floating Ip."""
    schema = schemas.FloatingIPDetails()

    def get_data(self, parsed_args):
        return self.app.session.post('/floating-ips', {})


class DeleteFloatingIp(Command):
    """Delete Floating Ip."""

    def get_parser(self, prog_name):
        parser = super(DeleteFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip',
            metavar='<floating_ip>',
            help=('Floating IP ID')
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/floating-ips/%s' % parsed_args.floating_ip
        self.app.session.delete(uri)


class AssociateFloatingIp(ShowOne):
    """Associate Floating Ip."""
    schema = schemas.FloatingIPDetails()

    def get_parser(self, prog_name):
        parser = super(AssociateFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip_id',
            metavar='<floating_ip_id>',
            help='Floating IP ID'
        )
        parser.add_argument(
            '--interface-id',
            metavar='<interface_id>',
            required=True,
            help='Interface ID'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'interface_id': parsed_args.interface_id,
        }
        uri = '/floating-ips/%s/associate' % parsed_args.floating_ip_id
        return self.app.session.post(uri, payload)


class RevokeFloatingIp(ShowOne):
    """Revoke Floating Ip."""
    schema = schemas.FloatingIPDetails()

    def get_parser(self, prog_name):
        parser = super(RevokeFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip_id',
            metavar='<floating_ip_id>',
            help='Floating IP ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/floating-ips/%s/revoke' % parsed_args.floating_ip_id
        return self.app.session.post(uri, {})
