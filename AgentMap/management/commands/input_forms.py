from django.core.management.base import BaseCommand
from AgentMap.models import PDF, Carrier, FormType, State
import os

# Dictionary to map the form type abbreviation to the full form type
FORM_TYPE_DICT = {
    form.form_type: form.full_form_type for form in FormType.objects.all()
}

# Dictionary to map the company abbreviation to the full company name
CompanyDict = {
    agency.abbreviation: agency.carrier_name for agency in Carrier.objects.all()
}

# Dictionary to map the state abbreviation to the full state name
state_dict = {
    state.state_code: state.full_state for state in State.objects.all()
}


# Function to parse the filenames in the given directory
def parse_filenames(directory):
    total = 0
    # Walk through the directory and get the filenames
    for root, dirs, files in os.walk(directory):
        total = total + len(files)  # Get the total number of files
        for file in files:  # iterate over the files
            print(file)
            if file.endswith('.pdf'):  # check if the file is a pdf
                parts = file.split('_', 2)  # Split the filename at the first underscore
                print("Parts: ", parts)  # Print the parts of the filename
                if len(parts) == 3:  # if we have 3 parts we smovin and can parse the data and input it into database
                    company, state, form_type = parts  # Get the company, state, and form type
                    form_type = form_type.replace('.pdf', '')  # Remove the file extension from the form type
                    # If the form_type has an - in it, split it at the - and take the first part for the form_type and
                    # the second part for the date
                    if '-' in form_type:  # Edge case for form types that include a date
                        form_type, date = form_type.split('-')
                        print(f"Form Type: {form_type}, Date: {date}")
                    else:
                        date = "None"

                    # get the file path of the pdf file
                    file_path = os.path.join(root, file)
                    # print(f"Company: {company}, State: {state}, Form Type: {form_type}, File Path: {file_path}")

                    # Get the relative path of the file
                    # This is a temporary implementation for my local machine
                    # Server is going to be running on linux so this will need to be changed closer to prod
                    start_dir: str = ('C:\\Users\\Noricum\\Desktop\\WebApps\\AgentMap_MultiLayer')
                    file_path = os.path.relpath(str(file_path), start_dir)
                    file_path = file_path.replace('\\', '/')  # replace backslashes with forward slashes
                    print(file_path)
                    # Cut off up until the static directory
                    index = file_path.index('static')  # No clue why my small changed required this to be added in
                    file_path = file_path[index:]  # Cut off up until the static dir, the ../../ will cause issues
                    print("relative path: ", file_path)

                    # print("relative path: ", file_path)

                    # Get the full form type from the FORM_TYPE_DICT
                    try:
                        form_type = FormType.objects.get(form_type=form_type)
                    except FormType.DoesNotExist:
                        form_type = None

                    # Get the MedicareSupplementAgencies object for the company
                    carrier = Carrier.objects.filter(abbreviation=company).first()

                    state = State.objects.filter(state_code=state).first()

                    # Create or retrieve the database object
                    form, created = PDF.objects.get_or_create(
                        carrier=carrier,  # Get the company name
                        # full_company=CompanyDict[company],  # Get the full company name
                        state=state,  # Get the state abbreviation
                        form_info=form_type,  # get the form type abbreviation
                        date=date,  # Get the date
                        file_path=file_path  # Get the file path
                    )

                    # Check if the form was created or not
                    if created:
                        print(f"Saved {form}")
                    else:
                        print(f"Skipping {form} because it already exists")
                # Looks like this is an edge case where the filename doesn't have enough parts
                # This is likely due to a filename that has more than 2 underscores
                # We can skip these files for now and probably add them in by hand later
                else:
                    print(f"Skipping {file} because it doesn't have enough parts")
                    print(f"Number of parts: {len(parts)}")
    print(f"Total files: {total}")  # Print the total number of files
    print(f"Total forms Parsed: {PDF.objects.count()}")  # Print the total number of forms in the database


# Command to parse the filenames in a given directory and add to the database.
# This should only be ran with the argument of that static directory
class Command(BaseCommand):
    help = 'Parse filenames in the given directory and add them to the database'

    # Add the directory argument. This is the directory to parse filenames in.
    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='?', type=str, help='The directory to parse filenames in.')
        return 0

    # Handle method that is called when the management command is ran
    def handle(self, *args, **options):
        directory = options['directory']
        parse_filenames(directory)
        return 0
