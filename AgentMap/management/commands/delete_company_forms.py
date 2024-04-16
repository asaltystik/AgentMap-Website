from django.core.management.base import BaseCommand
from AgentMap.models import Form


class Command(BaseCommand):
    help = 'Deletes all forms for the given companies.'

    def add_arguments(self, parser):
        parser.add_argument('companies', nargs='+', type=str, help='The companies to delete forms for.')

    def handle(self, *args, **options):
        companies = options['companies']
        for company in companies:
            Form.objects.filter(company=company).delete()
            print(f"Deleted all forms for {company}")
        return 0
