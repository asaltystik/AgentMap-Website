# import base command from django
from django.core.management.base import BaseCommand
from AgentMap.models import LicensedState, Agent
import pandas as pd


class Command(BaseCommand):
    help = "load license data from csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The csv file to load data from')
        return 0

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file)

        print(df)

        for index, row in df.iterrows():
            expiration_date = pd.to_datetime(row['Expiration Date'], format='%m/%d/%Y', errors='coerce')
            if pd.isnull(expiration_date):
                expiration_date = '2030-01-01'
            else:
                expiration_date = expiration_date.strftime('%Y-%m-%d')
            print(expiration_date)
            print(row['Agent'])
            LicensedState.objects.get_or_create(
                agent=Agent.objects.get(user__username=row['Agent']),
                state=row['State'],
                licenseNumber=row['License Number'],
                defaults={'expiration': expiration_date}
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))