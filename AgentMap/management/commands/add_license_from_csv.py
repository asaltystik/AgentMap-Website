# import base command from django
from django.core.management.base import BaseCommand
from AgentMap.models import LicensedState, Agent, State
import pandas as pd


class Command(BaseCommand):
    help = "load license data from csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The csv file to load data from')
        return 0

    def handle(self, *args, **kwargs):
        # Open the csv file
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file)

        print(df)

        # Loop through the rows in the dataframe
        for index, row in df.iterrows():
            # Make sure the expiration date is in the correct format
            expiration_date = pd.to_datetime(row['Expiration Date'], format='%m/%d/%Y', errors='coerce')
            # If the expiration date is null, set it to 2030-01-01
            if pd.isnull(expiration_date):
                expiration_date = '2030-01-01'
            else:
                # Convert the expiration date to the correct format
                expiration_date = expiration_date.strftime('%Y-%m-%d')
            print(expiration_date)
            print(row['Agent'])
            # Get the state object
            state = State.objects.get(state_code=row['State'])
            # Create or get the LicensedState object
            LicensedState.objects.get_or_create(
                agent=Agent.objects.get(user__username=row['Agent']),
                state=state,
                licenseNumber=row['License Number'],
                defaults={'expiration': expiration_date}
            )
        # Print a success message
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))