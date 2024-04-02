from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from AgentMap.models import LicensedState


# Creates a custom Django management command to check the LicensedState model
# for any licenses past their expiration date and deletes them
class Command(BaseCommand):
    help = ('Checks the LicensedState model for any licenses past their'
            ' expiration date and deletes them')

    # Handle method that is called when the management command is ran
    def handle(self, *args, **kwargs):
        # Get the current date
        current_date = timezone.now().date()

        # Query the LicensedState model for any licenses past their expiration date
        expired_licenses = LicensedState.objects.filter(expiration__lt=current_date)

        # Dictionary to store the licenses that will be deleted
        agent_licenses = {}

        # Iterate over the expired licenses and delete them
        for expired_license in expired_licenses:
            # Print the expired license
            self.stdout.write(f'License {expired_license.licenseNumber} '
                              f'for agent {expired_license.agent.user.username}'
                              f' in state {expired_license.state}'
                              f' has expired and will be deleted.')

            # Add the license to the dictionary
            agent_email = expired_license.agent.user.email
            if agent_email not in agent_licenses:
                agent_licenses[agent_email] = []
            agent_licenses[agent_email].append(f'License {expired_license.licenseNumber}'
                                               f' in state {expired_license.state}')

            # Delete the license
            expired_license.delete()

        # Print the number of expired licenses deleted
        self.stdout.write(f'{len(expired_licenses)} expired licenses deleted.')

        # Send email to each agent with their deleted licenses
        for agent_email, licenses in agent_licenses.items():
            send_mail(
                'Expired License Deletion Notice',
                f'The following licenses have expired and been deleted:\n'
                f'{", ".join(licenses)}\n'
                f'Please contact Steve or Craig to renew your licenses.',
                'carick@securecare65.com',
                [agent_email],
                fail_silently=False,
            )

        # Print the number of agents notified
        self.stdout.write(f'{len(agent_licenses)} agents notified of expired licenses.')
