from django.core.management.base import BaseCommand
from AgentMap.models import PDF, Carrier


# This command deletes all forms for the given companies
class Command(BaseCommand):
    help = 'Deletes all forms for the given companies. Companies must be inputted as their abbreviations.'

    # Allows the user to input the companies they want to remove from the Form db
    def add_arguments(self, parser):
        parser.add_argument('companies', nargs='+', type=str, help='The companies to delete forms for.')

    # Deletes all forms for the given companies
    def handle(self, *args, **options):
        companies = options['companies']  # Get the companies to delete forms for
        for company in companies:
            carrier_id = Carrier.objects.filter(abbreviation=company).first().id
            # i need carrier_id->carrier_name
            PDF.objects.filter(carrier_id=carrier_id).delete()  # Delete all forms for the given company
            self.stdout.write(f"Deleted all forms for {company}")  # Print that shit quay
        return 0
