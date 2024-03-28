from django.core.management.base import BaseCommand
from django.utils import timezone
from AgentMap.models import LicensedState


# Creates a custom Django management command to check the LicensedState model
# for any licenses past their expiration date and deletes them
class Command(BaseCommand):
    help = ('Checks the LicensedState model for any licenses past their'
            ' expiration date and deletes them')

    def handle(self, *args, **kwargs):
        # Get the current date
        current_date = timezone.now().date()

        # Query the LicensedState model for any licenses past their expiration date
        expired_licenses = LicensedState.objects.filter(expiration__lt=current_date)

        # Iterate over the expired licenses and delete them
        for expired_license in expired_licenses:
            # Print the expired license
            self.stdout.write(f'License {expired_license.licenseNumber} '
                              f'for agent {expired_license.agent.user.username}'
                              f' in state {expired_license.state}'
                              f' has expired and will be deleted.')
            # Delete the license
            expired_license.delete()

        # Print the number of expired licenses deleted
        self.stdout.write(f'{len(expired_licenses)} expired licenses deleted.')
