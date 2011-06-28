"""
Management utility to delete users.
"""

import re
import sys
from optparse import make_option
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

RE_VALID_USERNAME = re.compile('[\w.@+-]+$')

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username', default=None,
            help='Specifies the user to delete.'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help=('Tells Django to NOT prompt the user for input of any kind. '
                  'You must use --username.')),
    )
    help = 'Used to delete user.'

    def handle(self, *args, **options):
        username = options.get('username', None)
        interactive = options.get('interactive')
        verbosity = int(options.get('verbosity', 1))
        
        # Do quick and dirty validation if --noinput
        if not interactive:
            if not username:
                raise CommandError("You must use --username with --noinput.")
            if not RE_VALID_USERNAME.match(username):
                raise CommandError("Invalid username. Use only letters, digits, and underscores")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError("That user does not exist.")

        # Prompt for username. Enclose this whole thing in a try/except to trap 
        # for a keyboard interrupt and exit gracefully.
        if interactive:
            try:
                # Get a username
                while 1:
                    if not username:
                        input_msg = 'Username'
                        username = raw_input(input_msg + ': ')
                    if not RE_VALID_USERNAME.match(username):
                        sys.stderr.write("Error: That username is invalid. Use only letters, digits and underscores.\n")
                        username = None
                        continue
                    try:
                        user = User.objects.get(username=username)
			break
                    except User.DoesNotExist:
                        sys.stderr.write("Error: That user does not exist.\n")
                        username = None
                        continue
            except KeyboardInterrupt:
                sys.stderr.write("\nOperation cancelled.\n")
                sys.exit(1)

        user.delete()

        if verbosity >= 1:
            self.stdout.write("User deleted successfully.\n")

