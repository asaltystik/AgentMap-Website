from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AgentMap.models import LicensedState


# Creates a custom Django management command
# to delete licenses for a specified agent
class Command(BaseCommand):
    help = ("Deletes all licenses for a specific agent, Helps to clean up "
            "the database when an agent leaves the company")

    # Add the username argument
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the agent to delete licenses for')

    def handle(self, *args, **options):
        # Get the username
        user = User.objects.get(username=options['username'])

        # Query the LicensedState model for any licenses for the agent
        agent_licenses = LicensedState.objects.filter(agent=user.agent)

        # Iterate over the licenses and delete them
        for agent_license in agent_licenses:
            self.stdout.write(f'License {agent_license.licenseNumber} '
                              f'for agent {agent_license.agent.user.username}'
                              f' in state {agent_license.state}'
                              f' has been deleted.')
            agent_license.delete()

        # print the number of licenses deleted
        self.stdout.write(f'{len(agent_licenses)}'
                          f' licenses deleted for {user.username}')
