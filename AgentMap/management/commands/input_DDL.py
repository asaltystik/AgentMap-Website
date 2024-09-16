# This script will add in the data for the DDL table in the database
from django.core.management.base import BaseCommand
from AgentMap.models import Drug, MedicalCondition, Carrier, AcceptanceRule
import pandas


# This class will handle the command, which is responsible for inputting the rows
# from the DDL csv file into the database
class Command(BaseCommand):
    help = 'Input the DDL data into the database'

    # Function to handle the command
    def handle(self, *args, **kwargs):
        # Read the data from the csv file
        data = pandas.read_csv('static/Combined_DDL.csv')

        # Delete all rows in the AcceptanceRuleTable (This is just a development thing)
        AcceptanceRule.objects.all().delete()
        Drug.objects.all().delete()
        MedicalCondition.objects.all().delete()

        # We want to populate the Drug Table with any unique rows in the Drug column
        for drug in data['Drug Name'].unique():
            Drug.objects.get_or_create(drug_name=drug)

        # We want to populate the MedicalCondition Table with any unique rows in the Condition column
        for condition in data['Condition'].unique():
            MedicalCondition.objects.get_or_create(condition_name=condition)

        # Now we want to populate the AcceptanceRule Table with the data from the csv file
        for index, row in data.iterrows():

            # Get the drug object
            drug = Drug.objects.get(drug_name=row['Drug Name'])
            # Get the condition object
            condition = MedicalCondition.objects.get(condition_name=row['Condition'])
            # Get the company object
            try:
                company = Carrier.objects.get(abbreviation=row['Company'])
            except Carrier.DoesNotExist:
                company = None
                print('Error with getting the company object')
                print(f'Company: {row["Company"]}')
            # Get the is_accepted value
            is_accepted = row['Is_Allowed']
            # Create the AcceptanceRule object
            try:
                AcceptanceRule.objects.get_or_create(drug=drug, condition=condition, carrier=company,
                                                     is_accepted=is_accepted)
            except Carrier.DoesNotExist:
                print('Error with creating the AcceptanceRule object')
                print(f'Drug: {drug.drug_name}\n'
                      f'Condition: {condition.condition_name}\n'
                      f'Company: {company.abbreviation}\n'
                      f'Is_Accepted: {is_accepted}\n')
